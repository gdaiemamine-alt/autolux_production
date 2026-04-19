#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║   AutoLux — Installation locale (développement)         ║
# ╚══════════════════════════════════════════════════════════╝
set -e
GREEN='\033[0;32m'; GOLD='\033[0;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo ""
echo -e "${GOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GOLD}║   🚗  AutoLux — Démarrage local (DEV)       ║${NC}"
echo -e "${GOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}[1/6]${NC} Environnement virtuel..."
[ ! -d "venv" ] && python3 -m venv venv
source venv/bin/activate
echo -e "      ${GREEN}✓ Prêt${NC}"

echo -e "${BLUE}[2/6]${NC} Dépendances..."
pip install -r requirements.txt --quiet
echo -e "      ${GREEN}✓ Installées${NC}"

echo -e "${BLUE}[3/6]${NC} Base de données..."
python manage.py makemigrations --verbosity=0
python manage.py migrate --verbosity=0
echo -e "      ${GREEN}✓ Prête${NC}"

echo -e "${BLUE}[4/6]${NC} Données de démonstration..."
python manage.py loaddata cars/fixtures/initial_data.json --verbosity=0 2>/dev/null || true
echo -e "      ${GREEN}✓ 6 voitures chargées${NC}"

echo -e "${BLUE}[5/6]${NC} Fichiers statiques..."
python manage.py collectstatic --noinput --verbosity=0 2>/dev/null || true
echo -e "      ${GREEN}✓ OK${NC}"

echo -e "${BLUE}[6/6]${NC} Compte admin..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@autolux.tn', 'admin123')
    print('      admin / admin123 cree')
else:
    print('      admin deja existant')
"

echo ""
echo -e "${GOLD}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GOLD}║  ✅  Prêt !                                              ║${NC}"
echo -e "${GOLD}╠══════════════════════════════════════════════════════════╣${NC}"
echo -e "${GOLD}║  🌐  http://127.0.0.1:8000                               ║${NC}"
echo -e "${GOLD}║  ⚙️   http://127.0.0.1:8000/dashboard  (admin/admin123)  ║${NC}"
echo -e "${GOLD}║  🔧  http://127.0.0.1:8000/admin                         ║${NC}"
echo -e "${GOLD}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🚀 Serveur en cours... (Ctrl+C pour arrêter)${NC}"
python manage.py runserver
