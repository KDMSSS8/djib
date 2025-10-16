# ♟️ Gestionnaire de Tournoi d'Échecs

Un gestionnaire de tournoi d'échecs complet développé en Python, permettant de gérer des joueurs, créer des tournois, et suivre les résultats des parties.

## Fonctionnalités

- ✅ **Gestion des joueurs** : Créer et gérer une base de données de joueurs avec classement
- ✅ **Gestion des tournois** : Créer des tournois avec plusieurs types de contrôle du temps
- ✅ **Système de tours** : Lancer des tours de match et suivre les scores
- ✅ **Rapports** : Afficher les listes de joueurs (par ordre alphabétique ou classement)
- ✅ **Persistance** : Sauvegarde des données en base de données TinyDB
- ✅ **Interface interactive** : Menu principal convivial

## Architecture

```
PJ2 BASE/
├── bpm.py                 # Logique principale du jeu
├── data/
│   └── chess_tournament.json  # Base de données TinyDB
├── models/                # Modèles de données (MVC)
├── views/                 # Vues (MVC)
├── controllers/           # Contrôleurs (MVC)
├── setup.cfg             # Configuration Flake8
└── README.md             # Ce fichier
```

## Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-username/pj2-chess-tournament.git
cd pj2-chess-tournament
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
```

3. Activer l'environnement virtuel :

**Windows :**
```bash
venv\Scripts\activate
```

**Mac/Linux :**
```bash
source venv/bin/activate
```

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Lancer le programme :
```bash
python bpm.py
```

### Menu Principal

1. **Créer un nouveau tournoi** : Créer un tournoi avec des joueurs
2. **Ajouter un joueur global** : Ajouter un joueur à la base de données
3. **Ajouter un joueur à un tournoi** : Ajouter un joueur existant à un tournoi
4. **Lancer une partie** : Jouer un tour d'un tournoi
5. **Afficher les rapports** : Voir les statistiques et rapports
6. **Quitter** : Quitter l'application

## Spécifications des données

### Joueur
- Nom de famille
- Prénom
- Date de naissance (YYYY-MM-DD)
- Sexe (M/F)
- Classement (nombre positif)

### Tournoi
- Nom
- Lieu
- Date de début
- Date de fin
- Nombre de tours (défaut: 4)
- Type de contrôle du temps (bullet/blitz/rapide)
- Description
- Liste des joueurs
- Liste des tours

## Conformité

✅ **Flake8** : Code conforme avec max-line-length=119
- Pas d'erreurs de style
- Imports organisés
- Nommage PEP 8

## Technologies utilisées

- **Python 3.12**
- **TinyDB** : Base de données JSON légère
- **Standard Library** : datetime, random, typing, os, json

## Auteur

Développé en octobre 2025

## Licence

Ce projet est open source et disponible sous la licence MIT.

## Notes de développement

- Le code respecte les normes PEP 8
- Architecture MVC pour la scalabilité future
- Gestion complète des erreurs avec try-except
- Base de données persistante avec TinyDB
