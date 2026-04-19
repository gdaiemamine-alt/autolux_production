import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Charger le fichier .env si présent
env_file = Path(__file__).resolve().parent.parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, val = line.partition('=')
                os.environ.setdefault(key.strip(), val.strip())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental.settings')
application = get_wsgi_application()
