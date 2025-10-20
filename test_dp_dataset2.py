"""Test rapide de l'algorithme Programmation Dynamique sur dataset2"""
import sys
sys.path.insert(0, 'MOI')

from utils.data_loader import DataLoader
from controllers.dynamic_programming_resolver import DynamicProgrammingResolver

# Charger les données
print("📂 Chargement du dataset2...")
actions = DataLoader.load_from_csv('dataset2_Python+P3.csv')

if not actions:
    print("❌ Erreur: Aucune action chargée")
    sys.exit(1)

# Résoudre avec DP
print("\n⚡ Résolution avec Programmation Dynamique (O(n×W))...\n")
dp = DynamicProgrammingResolver(actions, max_budget=500000)
portfolio = dp.solve()

# Afficher les résultats
stats = dp.get_stats()
print("="*70)
print("✅ RÉSULTAT - PROGRAMMATION DYNAMIQUE")
print("="*70)
print(f"\nMéthode: {stats['method']}")
print(f"Coût total: {stats['total_cost']:,.0f} F CFA")
print(f"Profit total: {stats['total_profit']:,.0f} F CFA")
print(f"Nombre d'actions: {stats['actions_count']}")
print(f"Temps d'exécution: {stats['execution_time']:.6f} secondes")
print(f"Complexité: O(n × W) = O({len(actions)} × 500000)")

print("\n📋 Actions sélectionnées:")
print("-"*70)
print(f"{'Action':<15} {'Coût':<15} {'Profit %':<15} {'Profit':<15}")
print("-"*70)

for action in sorted(portfolio.actions, key=lambda a: a.cost, reverse=True):
    print(f"{action.name:<15} {action.cost:>12,.0f} {action.profit_pct*100:>13.2f}% {action.get_profit():>12,.0f}")

print("-"*70)
print(f"{'TOTAL':<15} {portfolio.get_total_cost():>12,.0f} {portfolio.get_profit_ratio()*100:>13.2f}% {portfolio.get_total_profit():>12,.0f}")
print("="*70)
