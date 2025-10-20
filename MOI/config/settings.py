"""
Configuration de l'application.
"""

# Configuration générale
APP_NAME = "Mon Application MVC"
APP_VERSION = "1.0.0"
DEBUG = True

# Configuration de la base de données (exemple)
DATABASE = {
    "type": "sqlite",
    "path": "./data/app.db"
}

# Configuration des logs
LOGGING = {
    "level": "INFO",
    "file": "./logs/app.log"
}
