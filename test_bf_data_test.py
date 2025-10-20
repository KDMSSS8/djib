"""Test rapide de l'algorithme Force Brute sur data_test.csv"""
import sys
sys.path.insert(0, 'MOI')

from utils.data_loader import DataLoader
from controllers.brute_force_resolver import BruteForceResolver

# Charger les données
print("📂 Chargement du data_test.csv...")
actions = DataLoader.load_from_csv('data_test.csv')

if not actions:
    print("❌ Erreur: Aucune action chargée")
    sys.exit(1)

# Résoudre avec Force Brute
print("\n⏳ Résolution avec Force Brute (O(2^n))...\n")
bf = BruteForceResolver(actions, max_budget=500000)
portfolio = bf.solve()

# Afficher les résultats
stats = bf.get_stats()
print("="*70)
print("✅ RÉSULTAT - FORCE BRUTE")
print("="*70)
print(f"\nMéthode: {stats['method']}")
print(f"Coût total: {stats['total_cost']:,.0f} F CFA")
print(f"Profit total: {stats['total_profit']:,.0f} F CFA")
print(f"Nombre d'actions: {stats['actions_count']}")
print(f"Itérations testées: {stats['iterations']:,}")
print(f"Temps d'exécution: {stats['execution_time']:.6f} secondes")
print(f"Complexité: O(2^n) = 2^{len(actions)} = {stats['iterations']:,} combinaisons")

print("\n📋 Actions sélectionnées:")
print("-"*70)
print(f"{'Action':<15} {'Coût':<15} {'Profit %':<15} {'Profit':<15}")
print("-"*70)

for action in sorted(portfolio.actions, key=lambda a: a.cost, reverse=True):
    print(f"{action.name:<15} {action.cost:>12,.0f} {action.profit_pct*100:>13.2f}% {action.get_profit():>12,.0f}")

print("-"*70)
print(f"{'TOTAL':<15} {portfolio.get_total_cost():>12,.0f} {portfolio.get_profit_ratio()*100:>13.2f}% {portfolio.get_total_profit():>12,.0f}")
print("="*70)

print(f"\n💡 Note: Testé {len(actions)} actions = {2**len(actions):,} combinaisons possibles")
