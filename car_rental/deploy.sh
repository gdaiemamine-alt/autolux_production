#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║   AutoLux — Script de déploiement VPS (Ubuntu 20/22)        ║
# ║   Lance ce script sur votre serveur en tant que root ou      ║
# ║   utilisateur avec sudo.                                     ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Usage :
#   chmod +x deploy.sh
#   sudo ./deploy.sh
#
# Ce script installe et configure :
#   - Python 3, pip, venv
#   - Nginx
#   - Gunicorn (service systemd)
#   - Le projet AutoLux

set -e
GREEN='\033[0;32m'; GOLD='\033[0;33m'; BLUE='\033[0;34m'; RED='\033[0;31m'; NC='\033[0m'

# ── CONFIG — modifiez ces variables ─────────────────────────────────
APP_USER="autolux"
APP_DIR="/var/www/autolux"
DOMAIN="votre-domaine.com"         # <-- CHANGEZ ICI
# ────────────────────────────────────────────────────────────────────

echo ""
echo -e "${GOLD}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GOLD}║     🚗  AutoLux — Déploiement VPS Ubuntu            ║${NC}"
echo -e "${GOLD}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Mise à jour système
echo -e "${BLUE}[1/9]${NC} Mise à jour des paquets système..."
apt-get update -qq && apt-get upgrade -y -qq
apt-get install -y -qq python3 python3-pip python3-venv nginx git curl

# 2. Créer l'utilisateur applicatif
echo -e "${BLUE}[2/9]${NC} Création de l'utilisateur $APP_USER..."
if ! id "$APP_USER" &>/dev/null; then
    useradd --system --shell /bin/bash --home $APP_DIR $APP_USER
    echo -e "      ${GREEN}✓ Utilisateur créé${NC}"
else
    echo -e "      ${GREEN}✓ Utilisateur existe déjà${NC}"
fi

# 3. Créer le dossier projet
echo -e "${BLUE}[3/9]${NC} Préparation du dossier projet..."
mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/media

# Copier les fichiers du projet (supposé que le zip est extrait à côté)
if [ -d "./car_rental" ]; then
    cp -r ./car_rental/. $APP_DIR/
    echo -e "      ${GREEN}✓ Fichiers copiés vers $APP_DIR${NC}"
else
    echo -e "      ${RED}⚠ Dossier car_rental introuvable. Copiez manuellement les fichiers.${NC}"
fi

chown -R $APP_USER:$APP_USER $APP_DIR

# 4. Environnement virtuel et dépendances
echo -e "${BLUE}[4/9]${NC} Installation des dépendances Python..."
cd $APP_DIR
sudo -u $APP_USER python3 -m venv venv
sudo -u $APP_USER venv/bin/pip install -r requirements.txt --quiet
echo -e "      ${GREEN}✓ Dépendances installées${NC}"

# 5. Variables d'environnement
echo -e "${BLUE}[5/9]${NC} Configuration des variables d'environnement..."
if [ ! -f "$APP_DIR/.env" ]; then
    cp $APP_DIR/.env.example $APP_DIR/.env
    # Générer une SECRET_KEY aléatoire
    SECRET=$(sudo -u $APP_USER venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    sed -i "s|REMPLACEZ-PAR-UNE-VRAIE-CLE-SECRETE-LONGUE-ET-ALEATOIRE|$SECRET|g" $APP_DIR/.env
    sed -i "s|votre-domaine.com,www.votre-domaine.com|$DOMAIN,www.$DOMAIN|g" $APP_DIR/.env
    chown $APP_USER:$APP_USER $APP_DIR/.env
    chmod 600 $APP_DIR/.env
    echo -e "      ${GREEN}✓ .env créé avec SECRET_KEY générée${NC}"
    echo -e "      ${GOLD}⚠ Éditez $APP_DIR/.env pour compléter la config${NC}"
else
    echo -e "      ${GREEN}✓ .env existant conservé${NC}"
fi

# Charger .env pour les commandes suivantes
export $(grep -v '^#' $APP_DIR/.env | xargs) 2>/dev/null || true
export DJANGO_ENV=production

# 6. Migrations + static + fixtures
echo -e "${BLUE}[6/9]${NC} Migrations et fichiers statiques..."
cd $APP_DIR
sudo -u $APP_USER DJANGO_ENV=production venv/bin/python manage.py migrate --verbosity=0
sudo -u $APP_USER DJANGO_ENV=production venv/bin/python manage.py collectstatic --noinput --verbosity=0
# Charger les données de démo si la DB est vide
sudo -u $APP_USER DJANGO_ENV=production venv/bin/python manage.py loaddata cars/fixtures/initial_data.json --verbosity=0 2>/dev/null || true
echo -e "      ${GREEN}✓ OK${NC}"

# 7. Service Gunicorn (systemd)
echo -e "${BLUE}[7/9]${NC} Configuration du service Gunicorn..."
cat > /etc/systemd/system/autolux.service << SYSTEMD
[Unit]
Description=AutoLux Gunicorn Daemon
After=network.target

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
Environment="DJANGO_ENV=production"
ExecStart=$APP_DIR/venv/bin/gunicorn \\
    car_rental.wsgi:application \\
    --bind unix:$APP_DIR/autolux.sock \\
    --workers 3 \\
    --timeout 120 \\
    --access-logfile $APP_DIR/logs/gunicorn-access.log \\
    --error-logfile $APP_DIR/logs/gunicorn-error.log
Restart=on-failure

[Install]
WantedBy=multi-user.target
SYSTEMD

systemctl daemon-reload
systemctl enable autolux
systemctl start autolux
echo -e "      ${GREEN}✓ Service Gunicorn actif${NC}"

# 8. Nginx
echo -e "${BLUE}[8/9]${NC} Configuration Nginx..."
cat > /etc/nginx/sites-available/autolux << NGINX
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Logs
    access_log /var/log/nginx/autolux_access.log;
    error_log  /var/log/nginx/autolux_error.log;

    # Fichiers statiques servis directement par Nginx
    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Uploads médias
    location /media/ {
        alias $APP_DIR/media/;
        expires 7d;
    }

    # Proxy vers Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/autolux.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;

        # Upload max (photos voitures)
        client_max_body_size 10M;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/autolux /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
echo -e "      ${GREEN}✓ Nginx configuré${NC}"

# 9. Certificat SSL avec Certbot (optionnel)
echo -e "${BLUE}[9/9]${NC} HTTPS avec Let's Encrypt..."
if command -v certbot &>/dev/null; then
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || true
    echo -e "      ${GREEN}✓ SSL configuré${NC}"
else
    apt-get install -y -qq certbot python3-certbot-nginx
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || true
    echo -e "      ${GREEN}✓ Certbot installé + SSL${NC}"
fi

# ── Résumé ────────────────────────────────────────────────────────
echo ""
echo -e "${GOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GOLD}║  ✅  Déploiement terminé !                                   ║${NC}"
echo -e "${GOLD}╠══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${GOLD}║  🌐  https://$DOMAIN                                         ║${NC}"
echo -e "${GOLD}║                                                              ║${NC}"
echo -e "${GOLD}║  Commandes utiles :                                          ║${NC}"
echo -e "${GOLD}║  sudo systemctl status autolux    # état du service          ║${NC}"
echo -e "${GOLD}║  sudo systemctl restart autolux   # redémarrer              ║${NC}"
echo -e "${GOLD}║  sudo journalctl -u autolux -f    # logs en direct          ║${NC}"
echo -e "${GOLD}║                                                              ║${NC}"
echo -e "${GOLD}║  ⚠  Créez un superuser admin :                               ║${NC}"
echo -e "${GOLD}║  cd $APP_DIR && sudo -u $APP_USER DJANGO_ENV=production      ║${NC}"
echo -e "${GOLD}║     venv/bin/python manage.py createsuperuser                ║${NC}"
echo -e "${GOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
