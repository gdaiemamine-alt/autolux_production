# 🚗 AutoLux — Site de Location de Voitures
### Application web Django · Design Luxury Dark Gold · Prêt pour la production

---

## 📋 Table des matières

1. [Aperçu du projet](#aperçu)
2. [Structure des fichiers](#structure)
3. [Installation locale (développement)](#dev)
4. [Mise en production](#production)
   - [Option A — Railway / Render (gratuit, 5 min)](#railway)
   - [Option B — VPS Ubuntu avec Nginx](#vps)
   - [Option C — Heroku](#heroku)
5. [Variables d'environnement](#env)
6. [Fonctionnalités](#fonctionnalités)
7. [Modèles de données](#modèles)
8. [URLs du site](#urls)
9. [Personnalisation](#perso)

---

## Aperçu du projet <a name="aperçu"></a>

AutoLux est un site complet de location de voitures développé avec **Django 4.2**.  
Il comprend un catalogue filtrable, un système de réservation, un espace client, et un dashboard d'administration personnalisé. Le design est en dark luxury gold avec les polices Cormorant Garamond et DM Sans.

**Technologies :**
- Backend : Django 4.2, Python 3.11
- Base de données : SQLite (dev) / PostgreSQL (prod)
- Serveur prod : Gunicorn + Nginx (ou Railway/Render/Heroku)
- Static files : WhiteNoise
- Upload images : Pillow

---

## Structure des fichiers <a name="structure"></a>

```
car_rental/
├── manage.py
├── requirements.txt
├── setup.sh              ← Démarrage local en 1 commande
├── deploy.sh             ← Déploiement VPS Ubuntu automatique
├── Procfile              ← Pour Railway / Render / Heroku
├── runtime.txt           ← Version Python
├── .env.example          ← Template de configuration
├── .gitignore
├── README.md
│
├── car_rental/           ← Configuration Django
│   ├── settings.py       (DEV + PROD selon DJANGO_ENV)
│   ├── urls.py
│   └── wsgi.py
│
├── cars/                 ← Catalogue véhicules
│   ├── models.py         (Car, Category)
│   ├── views.py
│   ├── admin.py
│   └── fixtures/
│       └── initial_data.json  ← 6 voitures + 4 catégories
│
├── bookings/             ← Réservations
│   ├── models.py         (Booking avec calcul prix auto)
│   ├── views.py
│   └── forms.py
│
├── accounts/             ← Authentification
│   ├── views.py          (register, login, logout, profile)
│   └── forms.py
│
├── dashboard/            ← Admin personnalisé (staff only)
│   ├── views.py          (KPIs, CRUD voitures, gestion résa)
│   └── forms.py
│
├── static/
│   ├── css/style.css     ← Design complet dark luxury
│   └── js/main.js
│
└── templates/            ← 17 templates HTML
    ├── base.html
    ├── home.html
    ├── contact.html
    ├── 404.html
    ├── cars/
    ├── bookings/
    ├── accounts/
    └── dashboard/
```

---

## Installation locale (développement) <a name="dev"></a>

### Prérequis
- Python 3.10 ou supérieur
- pip

### Méthode rapide (1 commande)

```bash
cd car_rental
chmod +x setup.sh
./setup.sh
```

Le script fait automatiquement :
1. Crée un environnement virtuel Python
2. Installe les dépendances
3. Applique les migrations
4. Charge 6 voitures de démo
5. Crée le compte admin (`admin` / `admin123`)
6. Lance le serveur sur http://127.0.0.1:8000

### Méthode manuelle

```bash
cd car_rental
python3 -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows PowerShell

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata cars/fixtures/initial_data.json
python manage.py createsuperuser
python manage.py runserver
```

---

## Mise en production <a name="production"></a>

### Option A — Railway ou Render (recommandé, gratuit, 5 minutes) <a name="railway"></a>

**Railway.app** et **Render.com** sont les plateformes les plus simples pour déployer Django gratuitement.

#### Étapes Railway

1. **Créer un compte** sur https://railway.app (login avec GitHub)

2. **Pousser le code sur GitHub**
   ```bash
   cd car_rental
   git init
   git add .
   git commit -m "Initial commit AutoLux"
   # Créez un repo sur github.com puis :
   git remote add origin https://github.com/VOTRE_USER/autolux.git
   git push -u origin main
   ```

3. **Créer un projet Railway**
   - Cliquez "New Project" → "Deploy from GitHub repo"
   - Sélectionnez votre repo `autolux`

4. **Ajouter les variables d'environnement** dans Railway → Settings → Variables :
   ```
   DJANGO_ENV=production
   SECRET_KEY=votre_cle_secrete_generee
   ALLOWED_HOSTS=votre-app.railway.app
   ```

5. **Railway détecte automatiquement** le `Procfile` et lance Gunicorn.

6. **Après le déploiement**, ouvrir le terminal Railway et exécuter :
   ```bash
   python manage.py migrate
   python manage.py loaddata cars/fixtures/initial_data.json
   python manage.py createsuperuser
   ```

7. Votre site est en ligne sur `https://votre-app.railway.app` ✅

#### Étapes Render.com

1. Créez un compte sur https://render.com
2. "New Web Service" → connectez votre repo GitHub
3. Paramètres :
   - **Build Command** : `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command** : `gunicorn car_rental.wsgi:application`
4. Variables d'environnement : même qu'au-dessus
5. Cliquez "Create Web Service" → déploiement automatique ✅

---

### Option B — VPS Ubuntu avec Nginx + Gunicorn <a name="vps"></a>

Pour un VPS OVH, DigitalOcean, Hetzner, etc. tournant Ubuntu 20.04/22.04.

#### Prérequis
- VPS avec Ubuntu 20.04 ou 22.04
- Accès root SSH
- Un nom de domaine pointant vers l'IP du serveur

#### Déploiement automatique

```bash
# 1. Connectez-vous au VPS
ssh root@IP_DE_VOTRE_VPS

# 2. Uploadez le projet (depuis votre machine locale)
scp autolux_car_rental_final.zip root@IP_VPS:/tmp/

# 3. Sur le VPS : décompressez
cd /tmp && unzip autolux_car_rental_final.zip
cd car_rental

# 4. Éditez le domaine dans deploy.sh
nano deploy.sh
# Changez : DOMAIN="votre-domaine.com"

# 5. Lancez le script
chmod +x deploy.sh && sudo ./deploy.sh
```

Le script configure automatiquement :
- Nginx comme reverse proxy
- Gunicorn comme serveur WSGI (service systemd)
- Certificat SSL Let's Encrypt (HTTPS gratuit)
- Logs dans `/var/www/autolux/logs/`

#### Après le déploiement — créer l'admin

```bash
cd /var/www/autolux
sudo -u autolux DJANGO_ENV=production venv/bin/python manage.py createsuperuser
```

#### Commandes utiles VPS

```bash
# État du service
sudo systemctl status autolux

# Redémarrer après modification du code
sudo systemctl restart autolux

# Voir les logs en direct
sudo journalctl -u autolux -f

# Logs Nginx
sudo tail -f /var/log/nginx/autolux_error.log

# Mettre à jour le code
cd /var/www/autolux
git pull origin main
sudo -u autolux DJANGO_ENV=production venv/bin/python manage.py migrate
sudo -u autolux DJANGO_ENV=production venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart autolux
```

#### Configuration PostgreSQL (optionnel, recommandé en prod)

```bash
# Installer PostgreSQL
sudo apt install postgresql postgresql-contrib

# Créer la base de données
sudo -u postgres psql << SQL
CREATE DATABASE autolux_db;
CREATE USER autolux_user WITH PASSWORD 'mot_de_passe_fort';
GRANT ALL PRIVILEGES ON DATABASE autolux_db TO autolux_user;
\q
SQL

# Ajouter dans .env
DB_NAME=autolux_db
DB_USER=autolux_user
DB_PASSWORD=mot_de_passe_fort
DB_HOST=localhost
DB_PORT=5432

# Installer psycopg2 (décommentez dans requirements.txt d'abord)
sudo -u autolux /var/www/autolux/venv/bin/pip install psycopg2-binary
sudo systemctl restart autolux
```

---

### Option C — Heroku <a name="heroku"></a>

```bash
# Installer Heroku CLI, puis :
heroku login
heroku create autolux-app

# Variables d'environnement
heroku config:set DJANGO_ENV=production
heroku config:set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
heroku config:set ALLOWED_HOSTS=autolux-app.herokuapp.com

# Déployer
git push heroku main

# Migrations et admin
heroku run python manage.py migrate
heroku run python manage.py loaddata cars/fixtures/initial_data.json
heroku run python manage.py createsuperuser
```

---

## Variables d'environnement <a name="env"></a>

Copiez `.env.example` en `.env` et remplissez les valeurs :

```bash
cp .env.example .env
nano .env
```

| Variable | Obligatoire | Description |
|----------|-------------|-------------|
| `DJANGO_ENV` | Oui | `development` ou `production` |
| `SECRET_KEY` | Oui en prod | Clé secrète Django (longue et aléatoire) |
| `ALLOWED_HOSTS` | Oui en prod | Votre domaine, ex: `autolux.tn,www.autolux.tn` |
| `DB_NAME` | Non | Nom de la base PostgreSQL |
| `DB_USER` | Non | Utilisateur PostgreSQL |
| `DB_PASSWORD` | Non | Mot de passe PostgreSQL |
| `DB_HOST` | Non | Hôte PostgreSQL (défaut: localhost) |
| `EMAIL_HOST` | Non | Serveur SMTP pour les emails |
| `EMAIL_HOST_USER` | Non | Adresse email SMTP |
| `EMAIL_HOST_PASSWORD` | Non | Mot de passe SMTP |

**Générer une SECRET_KEY :**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Fonctionnalités <a name="fonctionnalités"></a>

### Visiteurs / clients
| Page | URL | Description |
|------|-----|-------------|
| Accueil | `/` | Hero animé, stats, voitures vedettes |
| Catalogue | `/cars/` | Filtres : catégorie, transmission, carburant, prix, dispo |
| Détail voiture | `/cars/<id>/` | Specs, prix, véhicules similaires |
| Inscription | `/accounts/register/` | Création de compte |
| Connexion | `/accounts/login/` | Authentification |
| Profil | `/accounts/profile/` | Modifier nom, email |
| Réserver | `/bookings/book/<id>/` | Formulaire avec calcul prix auto |
| Mes réservations | `/bookings/mes-reservations/` | Historique + annulation |
| Contact | `/contact/` | Formulaire de contact |

### Administrateurs (staff/superuser)
| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/dashboard/` | KPIs : revenus, réservations, utilisateurs |
| Véhicules | `/dashboard/voitures/` | Liste + CRUD complet |
| Ajouter voiture | `/dashboard/voitures/ajouter/` | Formulaire avec upload photo |
| Modifier voiture | `/dashboard/voitures/<id>/modifier/` | Édition |
| Réservations | `/dashboard/reservations/` | Toutes les réservations + filtre statut |
| Changer statut | `/dashboard/reservations/<id>/statut/` | pending/confirmed/active/completed/cancelled |
| Django Admin | `/admin/` | Interface admin complète |

---

## Modèles de données <a name="modèles"></a>

### Car (Voiture)
| Champ | Type | Description |
|-------|------|-------------|
| `brand` | CharField | Marque (Toyota, BMW…) |
| `model` | CharField | Modèle (Corolla, X5…) |
| `year` | IntegerField | Année |
| `category` | ForeignKey | Citadine / Berline / SUV / Prestige |
| `price_per_day` | DecimalField | Tarif en DT/jour |
| `transmission` | CharField | `manual` / `automatic` |
| `fuel_type` | CharField | `gasoline` / `diesel` / `electric` / `hybrid` |
| `seats` / `doors` | IntegerField | Places / portes |
| `air_conditioning` | BooleanField | Climatisation |
| `gps` | BooleanField | GPS intégré |
| `image` | ImageField | Photo du véhicule |
| `is_available` | BooleanField | Disponible à la location |

### Booking (Réservation)
| Champ | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | Client |
| `car` | ForeignKey | Véhicule |
| `start_date` / `end_date` | DateField | Période |
| `total_price` | DecimalField | Calculé automatiquement |
| `status` | CharField | pending / confirmed / active / completed / cancelled |
| `pickup_location` | CharField | Lieu de prise en charge |
| `return_location` | CharField | Lieu de retour |

---

## Personnalisation <a name="perso"></a>

### Changer le nom du site
Cherchez `AutoLux` dans `templates/base.html` et `templates/home.html`.

### Changer la devise
Cherchez `DT` dans tous les templates HTML, remplacez par `€`, `$`, `MAD`, etc.

### Changer les couleurs
Dans `static/css/style.css`, modifiez les variables CSS :
```css
:root {
  --bg: #0a0a0c;           /* Fond principal */
  --gold: #d4af37;          /* Couleur accent */
  --gold-light: #e8c96a;    /* Accent clair */
  --text: #f0ece4;          /* Texte principal */
}
```

### Ajouter un véhicule
- Via le dashboard : `/dashboard/voitures/ajouter/`
- Via Django Admin : `/admin/cars/car/add/`
- Via fixture JSON dans `cars/fixtures/`

### Activer PostgreSQL
1. Décommentez `psycopg2-binary` dans `requirements.txt`
2. Ajoutez les variables `DB_*` dans `.env`
3. Réappliquez `python manage.py migrate`

### Domaine personnalisé
Sur Railway/Render : Settings → Custom Domain → suivez les instructions DNS.  
Sur VPS : modifiez `DOMAIN` dans `deploy.sh` et relancez.

---

## Licence

Projet libre pour usage personnel et commercial.

---

*AutoLux · Django 4.2 · Python 3.11 · Déployé avec ❤️*
