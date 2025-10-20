# Investment Portfolio Optimizer

> Optimisation de portefeuille d'investissement avec deux algorithmes: Force Brute et Programmation Dynamique

## 🎯 Objectif

Sélectionner les meilleures actions à acheter dans un budget limité (500,000 F CFA) pour **maximiser le profit** sur 2 ans.

**Problème:** 0/1 Knapsack Problem

## 📊 Deux Algorithmes Implémentés

### 1. **Force Brute** (O(2^n))
- Teste TOUTES les 2^n combinaisons possibles
- ✅ Garantit la solution optimale
- ❌ Très lent pour n > 25
- Temps: 109 secondes pour 25 actions

### 2. **Programmation Dynamique** (O(n×W))
- Construit une table DP [n+1][W+1]
- ✅ Garantit la solution optimale
- ✅ Rapide et scalable
- Temps: 3.7 secondes pour 25 actions
- **Speedup: 29.5× plus rapide** 🚀

## 📈 Résultats Mesurés

| Dataset | Algo | Actions | Temps | Profit | Note |
|---------|------|---------|-------|--------|------|
| data_test.csv | Force Brute | 20 | 2.87s | 111,340 F | ✅ |
| data_test.csv | DP | 20 | 3.13s | 111,340 F | ✅ |
| dataset1 | Force Brute | 25 | 109s | 126,206 F | ⚠️ Lent |
| dataset1 | DP | 25 | 3.7s | 126,206 F | ✅ Rapide |
| dataset2 | DP | 541 | 99s | 287,202 F | ✅ Huge dataset |

**Conclusion:** Les deux algorithmes trouvent la **même solution optimale**, mais **DP est drastiquement plus rapide**!

## 🚀 Démarrage Rapide

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/investment-portfolio-optimizer.git
cd investment-portfolio-optimizer/MOI
```

### Lancement
```bash
python app.py
```

### Menu Interactif (7 Options)
```
1. Tester FORCE BRUTE sur data_test.csv (20 actions)
2. Tester PROGRAMMATION DYNAMIQUE sur data_test.csv (20 actions)
3. Comparer les DEUX algorithmes sur data_test.csv
4. Tester DP sur dataset1_Python+P3.csv (25 actions)
5. Tester DP sur dataset2_Python+P3.csv (541 actions)
6. Comparer tous les datasets avec DP
7. Quitter
```

## 📁 Structure du Projet

```
investment-portfolio-optimizer/
│
├── MOI/
│   ├── app.py                          # Menu interactif (point d'entrée)
│   ├── README.md                       # Documentation
│   ├── LOCALISATION_ALGORITHMES.txt    # Guide de localisation du code
│   │
│   ├── models/
│   │   ├── action.py                   # Classe Action (stock)
│   │   ├── portfolio.py                # Classe Portfolio
│   │   └── base_model.py               # Classe de base
│   │
│   ├── controllers/
│   │   ├── brute_force_resolver.py     # Algorithme Force Brute (O(2^n))
│   │   ├── dynamic_programming_resolver.py  # Algorithme DP (O(n×W))
│   │   └── base_controller.py          # Classe de base
│   │
│   ├── utils/
│   │   ├── data_loader.py              # Charge CSV (flexible)
│   │   ├── results_manager.py          # Compare résultats
│   │   └── logger.py                   # Logging
│   │
│   └── views/
│       └── base_view.py                # Classe de base
│
├── data_test.csv                       # 20 actions (test)
├── dataset1_Python+P3.csv              # 25 actions (benchmark)
├── dataset2_Python+P3.csv              # 541 actions (gros dataset)
│
├── test_bf_data_test.py                # Test Force Brute standalone
├── test_dp_dataset2.py                 # Test DP standalone
├── menu.py                             # Menu (copie de app.py)
│
├── PRESENTATION.md                     # Présentation du projet
├── RESULTATS_FINAUX.md                 # Résultats détaillés
├── NETTOYAGE_OPTIMISATION.txt          # Historique des optimisations
│
├── README.md                           # Ce fichier
├── .gitignore                          # Fichiers à ignorer
└── LICENSE                             # Licence MIT
```

## 🔑 Points Clés du Code

### Force Brute (41 lignes)
```python
# controllers/brute_force_resolver.py
for r in range(len(self.actions) + 1):
    for combination in combinations(self.actions, r):  # 2^n itérations
        portfolio = Portfolio(list(combination))
        if portfolio.is_valid(self.max_budget):
            if current_profit > best_profit:
                best_profit = current_profit
```

### Programmation Dynamique (51 lignes)
```python
# controllers/dynamic_programming_resolver.py
# Étape 1: Table DP
dp = [[0 for _ in range(max_budget + 1)] for _ in range(n + 1)]

# Étape 2: Remplissage
for i in range(1, n + 1):
    for w in range(max_budget + 1):
        dp[i][w] = dp[i - 1][w]  # Ne pas prendre
        if cost <= w:
            dp[i][w] = max(dp[i][w], dp[i - 1][w - cost] + profit)  # Ou prendre

# Étape 3: Backtracking
for i in range(n, 0, -1):
    if dp[i][w] != dp[i - 1][w]:
        selected_actions.append(self.actions[i - 1])
```

## 📚 Apprentissages

### Concepts Couverts
- ✅ Problème 0/1 Knapsack
- ✅ Programmation Dynamique
- ✅ Analyse de Complexité (Big O)
- ✅ Pattern Strategy (deux algos)
- ✅ Architecture MVC
- ✅ Gestion des données CSV

### Performance
- Force Brute: O(2^n) temps, O(n) espace
- DP: O(n×W) temps, O(n×W) espace
- Speedup real world: 29.5× sur 25 actions

## ✅ Validation

✅ **Correctness:** Les deux algos trouvent la même solution  
✅ **Optimality:** Solution respecte le budget 500,000 F CFA  
✅ **Testing:** Testé sur 3 datasets différents  
✅ **Performance:** DP scalable à 541+ actions  
✅ **Code Quality:** Optimisé, commenté, maintenable  

## 🎓 Comment Utiliser pour Présentation

1. Lancer `python app.py` dans MOI/
2. Option 3: Comparer BF vs DP sur petit dataset (20 actions)
3. Option 5: Montrer DP sur gros dataset (541 actions)
4. Option 6: Résumé comparatif de tous les datasets
5. Consulter `MOI/LOCALISATION_ALGORITHMES.txt` pour localiser le code exact

## 📊 Statistiques du Projet

- **Lignes de code Python:** ~350 (optimisé)
- **Fichiers:** 18
- **Dépendances:** Python stdlib uniquement
- **Tests:** 3 fichiers test
- **Datasets:** 3
- **Documentation:** 5 fichiers

## 🔄 Historique des Optimisations

- Réduit de 40% les lignes inutiles
- Supprimé 15+ fichiers de documentation redondante
- Remplacé app.py limité par menu.py flexible
- Fixé DataLoader pour supporter formats multiples
- Validé sur datasets jusqu'à 541 actions

## 📖 Fichiers de Documentation

- **MOI/README.md** - Documentation technique
- **MOI/LOCALISATION_ALGORITHMES.txt** - Localisation précise du code
- **PRESENTATION.md** - Contenu pour présentation (15 min)
- **RESULTATS_FINAUX.md** - Résultats détaillés
- **NETTOYAGE_OPTIMISATION.txt** - Historique des changements

## 📄 License

MIT License - Voir LICENSE file

## 👤 Auteur

Djibril
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: votre_email@example.com

## 🙏 Remerciements

Merci pour ce projet intéressant de Programmation Dynamique!

---

**Prêt pour présentation/défense! 🎉**
