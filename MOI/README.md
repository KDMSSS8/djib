# 🎯 Investment Portfolio Optimizer# Investment Portfolio Optimizer# Structure MVC - Application



## 📝 Description

Application pour optimiser un portefeuille d'investissement avec **deux algorithmes**:

1. **Force Brute** (O(2^n)) - Teste toutes les combinaisons## 🎯 Problème## Architecture

2. **Programmation Dynamique** (O(n×W)) - Algorithme optimal et scalable

Sélectionner les meilleures actions dans un budget limité (500,000 F CFA) pour **maximiser le profit**.

## 🚀 Lancement Rapide

```

```bash

python app.py## 📊 DonnéesMOI/

```

- **Format:** CSV (actions avec coût et profit %)├── models/              # Modèles de données

Puis choisir une option du menu (1-7).

- **Budget:** 500,000 F CFA│   ├── __init__.py

## 📋 Menu Principal

- **Horizon:** 2 ans│   └── base_model.py

```

1. Tester FORCE BRUTE sur data_test.csv (20 actions)- **Profit = coût × profit_pct**├── views/               # Vues et affichage

2. Tester PROGRAMMATION DYNAMIQUE sur data_test.csv (20 actions)

3. Comparer les DEUX algorithmes sur data_test.csv│   ├── __init__.py

4. Tester DP sur dataset1_Python+P3.csv (25 actions)

5. Tester DP sur dataset2_Python+P3.csv (541 actions)## 🚀 Deux Algorithmes│   └── base_view.py

6. Comparer tous les datasets avec DP

7. Quitter├── controllers/         # Contrôleurs - Logique métier

```

### 1. **Force Brute** (O(2^n))│   ├── __init__.py

## 📊 Résumé des Tests

```│   └── base_controller.py

### Data Test (20 actions)

- **Force Brute:** 2.87s → Profit 111,340 F CFAcontrollers/brute_force_resolver.py├── config/              # Configuration

- **DP:** 3.13s → Profit 111,340 F CFA ✅

```│   ├── __init__.py

### Dataset 1 (25 actions)

- **Force Brute:** 109s → Profit 126,206 F CFA- Teste toutes les 2^n combinaisons possibles│   └── settings.py

- **DP:** 3.7s → Profit 126,206 F CFA ✅

- **Speedup:** 29.5× plus rapide- **Garantit** la solution optimale├── utils/               # Utilitaires



### Dataset 2 (541 actions)- ❌ Très lent pour n > 25│   ├── __init__.py

- **DP:** 99s → Profit 287,202 F CFA

- **DP meilleur** pour gros datasets│   └── logger.py



## 🔑 Algorithmes**Performance (25 actions):** 109 secondes├── app.py               # Application principale



### Force Brute├── requirements.txt     # Dépendances

**Fichier:** `controllers/brute_force_resolver.py` (41 lignes)

**Complexité:** O(2^n)### 2. **Programmation Dynamique** (O(n×W))└── README.md            # Documentation

- n=20: 2.8s ✅

- n=25: 109s ⚠️``````



### Programmation Dynamiquecontrollers/dynamic_programming_resolver.py

**Fichier:** `controllers/dynamic_programming_resolver.py` (51 lignes)

**Complexité:** O(n × W)```## Description des couches

- n=20: 3.1s ✅

- n=25: 3.7s ✅- Table DP [n+1][W+1]

- n=541: 99s ✅

- Backtracking pour reconstruire solution### Models (models/)

## 📂 Structure

- **Garantit** la solution optimaleReprésente la logique métier et les données de l'application.

```

MOI/- ✅ Rapide et scalable- `BaseModel`: Classe de base pour tous les modèles

├── app.py                              # Menu interactif

├── models/

│   ├── action.py                       # Stock/Action

│   └── portfolio.py                    # Portefeuille**Performance (25 actions):** 3.7 secondes### Views (views/)

├── controllers/

│   ├── brute_force_resolver.py         # Algorithme 1Gère l'affichage et la présentation des données.

│   └── dynamic_programming_resolver.py # Algorithme 2

└── utils/**Speedup:** 29.5× plus rapide!- `BaseView`: Classe de base pour toutes les vues

    ├── data_loader.py                  # Charge CSV

    └── results_manager.py              # Compare résultats

```

## 📁 Structure### Controllers (controllers/)

## ✅ Résultats Validés

✅ Optimal: Même solution trouvée par les deux algosGère la communication entre Model et View.

✅ Scalable: Teste jusqu'à 541 actions

✅ Rapide: DP 29.5× plus rapide que BF```- `BaseController`: Classe de base pour tous les contrôleurs

✅ Testé: 3 datasets différents

MOI/

├── app.py                              # Application principale### Config (config/)

├── models/Centralise la configuration de l'application.

│   ├── action.py                       # Classe Action- `settings.py`: Paramètres globaux

│   └── portfolio.py                    # Classe Portfolio

├── controllers/### Utils (utils/)

│   ├── brute_force_resolver.py         # Algorithme 1Contient les utilitaires réutilisables.

│   └── dynamic_programming_resolver.py # Algorithme 2- `logger.py`: Gestion des logs

└── utils/

    ├── data_loader.py                  # Charge CSV## Utilisation

    └── results_manager.py              # Compare les résultats

```1. **Créer un modèle** :

   ```python

## 🏃 Utilisation   from models.base_model import BaseModel

   

```bash   class User(BaseModel):

python app.py       def __init__(self, name, email):

```           super().__init__()

           self.name = name

Puis choisir le fichier de données (1, 2 ou 3).           self.email = email

   ```

## 📋 Résultats

2. **Créer une vue** :

```python   ```python

# Force Brute   from views.base_view import BaseView

bf = BruteForceResolver(actions, max_budget=500000)   

portfolio = bf.solve()   class UserView(BaseView):

print(bf.get_stats())       def display_user(self, user):

           self.display(f"Utilisateur: {user.name} ({user.email})")

# Programmation Dynamique   ```

dp = DynamicProgrammingResolver(actions, max_budget=500000)

portfolio = dp.solve()3. **Créer un contrôleur** :

print(dp.get_stats())   ```python

```   from controllers.base_controller import BaseController

   

## ✅ Validation   class UserController(BaseController):

Les deux algorithmes donnent **exactement la même solution optimale** ✔️       def process(self):

           # Logique métier ici

## 📚 Fichiers de Test           pass

- `data_test.csv` (20 actions)   ```

- `dataset1_Python+P3.csv` (25 actions)

- `dataset2_Python+P3.csv` (25 actions)4. **Lancer l'application** :

   ```bash
   python app.py
   ```

## Next Steps

- Étendre les modèles de base
- Implémenter des vues spécifiques
- Créer des contrôleurs pour votre domaine métier
- Ajouter une base de données
- Configurer les routes (si applicable)
