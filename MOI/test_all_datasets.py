"""
Script de test pour exécuter l'application avec les différents datasets.
"""

import os
import sys
import io
from utils.data_loader import DataLoader
from utils.results_manager import ResultsManager
from controllers.brute_force_resolver import BruteForceResolver
from controllers.dynamic_programming_resolver import DynamicProgrammingResolver

# Forcer l'encodage UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_dataset(filepath, dataset_name, max_budget=500000):
    """Teste un dataset avec les deux méthodes."""
    
    print(f"\n{'='*80}")
    print(f"TEST : {dataset_name}")
    print(f"{'='*80}\n")
    
    # Charger les données
    actions = DataLoader.load_from_csv(filepath)
    
    if not actions:
        print(f"ERROR : Impossible de charger {filepath}")
        return None
    
    if not DataLoader.validate_actions(actions):
        print(f"ERROR : Données invalides dans {filepath}")
        return None
    
    print(f"\n📈 Statistiques :")
    print(f"  - Actions : {len(actions)}")
    print(f"  - Coût min : {min(a.cost for a in actions):,.0f} F CFA")
    print(f"  - Coût max : {max(a.cost for a in actions):,.0f} F CFA")
    print(f"  - Budget : {max_budget:,.0f} F CFA")
    
    results_manager = ResultsManager()
    
    # Force Brute
    print(f"\n[...] Résolution par FORCE BRUTE...")
    bf_resolver = BruteForceResolver(actions, max_budget)
    bf_portfolio = bf_resolver.solve()
    results_manager.set_brute_force_result(bf_resolver)
    print(f"   OK - Terminée en {bf_resolver.execution_time:.6f} sec ({bf_resolver.iterations:,} itérations)")
    
    # Programmation Dynamique
    print(f"\n[*] Résolution par PROGRAMMATION DYNAMIQUE...")
    dp_resolver = DynamicProgrammingResolver(actions, max_budget)
    dp_portfolio = dp_resolver.solve()
    results_manager.set_dp_result(dp_resolver)
    print(f"   OK - Terminée en {dp_resolver.execution_time:.6f} sec")
    
    # Comparaison
    results_manager.compare()
    results_manager.display_results()
    
    # Détails du meilleur portefeuille
    print(f"\n[OK] MEILLEUR PORTEFEUILLE (Force Brute)")
    print(f"   Coût : {bf_portfolio.get_total_cost():,.0f} F CFA")
    print(f"   Profit : {bf_portfolio.get_total_profit():,.0f} F CFA")
    print(f"   Actions : {len(bf_portfolio.actions)}")
    
    return {
        'dataset': dataset_name,
        'bf_result': results_manager.brute_force_result,
        'dp_result': results_manager.dp_result,
        'comparison': results_manager.comparison
    }


def main():
    """Lance les tests."""
    
    print("\n" + "="*80)
    print("[TEST] TESTS D'OPTIMISATION D'INVESTISSEMENT")
    print("="*80)
    
    # Lister les fichiers CSV disponibles
    csv_files = [
        ('data_test.csv', 'Dataset Test'),
        ('dataset1_Python+P3.csv', 'Dataset 1 - Reference'),
        ('dataset2_Python+P3.csv', 'Dataset 2 - Reference'),
    ]
    
    results = []
    
    for filepath, name in csv_files:
        if os.path.exists(filepath):
            result = test_dataset(filepath, name)
            if result:
                results.append(result)
        else:
            print(f"\n[WARN] {filepath} non trouvé")
    
    # Résumé final
    if results:
        print(f"\n{'='*80}")
        print("[SUMMARY] RESUME DES TESTS")
        print(f"{'='*80}\n")
        
        print(f"{'Dataset':<25} {'Coût BF':<15} {'Profit BF':<15} {'Temps BF':<12} {'Temps DP':<12} {'Speedup':<10}")
        print("-"*90)
        
        for r in results:
            bf = r['bf_result']
            dp = r['dp_result']
            comp = r['comparison']
            
            speedup = comp.get('speedup', 0)
            
            print(f"{r['dataset']:<25} "
                  f"{bf['total_cost']:>12,.0f} {bf['total_profit']:>13,.0f} "
                  f"{bf['execution_time']:>10.6f}s {dp['execution_time']:>10.6f}s "
                  f"{speedup:>8.1f}x")
        
        print("-"*90)


if __name__ == "__main__":
    main()
