"""Menu interactif pour tester les algorithmes"""
import sys
sys.path.insert(0, 'MOI')

from utils.data_loader import DataLoader
from controllers.brute_force_resolver import BruteForceResolver
from controllers.dynamic_programming_resolver import DynamicProgrammingResolver
from utils.results_manager import ResultsManager


def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*70)
    print("🎯 OPTIMISATION DE PORTEFEUILLE D'INVESTISSEMENT")
    print("="*70)
    print("\n📋 MENU PRINCIPAL:\n")
    print("  1. Tester FORCE BRUTE sur data_test.csv (20 actions)")
    print("  2. Tester PROGRAMMATION DYNAMIQUE sur data_test.csv (20 actions)")
    print("  3. Comparer les DEUX algorithmes sur data_test.csv")
    print("  4. Tester DP sur dataset1_Python+P3.csv (25 actions)")
    print("  5. Tester DP sur dataset2_Python+P3.csv (541 actions)")
    print("  6. Comparer tous les datasets avec DP")
    print("  7. Quitter")
    print("\n" + "="*70)


def charger_donnees(filepath):
    """Charge les données et retourne les actions"""
    print(f"\n📂 Chargement de {filepath.split('/')[-1]}...")
    actions = DataLoader.load_from_csv(filepath)
    if not actions:
        print("❌ Erreur: Aucune action chargée")
        return None
    return actions


def test_force_brute(filepath):
    """Teste Force Brute"""
    actions = charger_donnees(filepath)
    if not actions:
        return
    
    print(f"\n⏳ Résolution avec FORCE BRUTE (O(2^n))...\n")
    bf = BruteForceResolver(actions, max_budget=500000)
    portfolio = bf.solve()
    
    afficher_resultats_bf(bf, portfolio)


def test_dp(filepath):
    """Teste Programmation Dynamique"""
    actions = charger_donnees(filepath)
    if not actions:
        return
    
    print(f"\n⚡ Résolution avec PROGRAMMATION DYNAMIQUE (O(n×W))...\n")
    dp = DynamicProgrammingResolver(actions, max_budget=500000)
    portfolio = dp.solve()
    
    afficher_resultats_dp(dp, portfolio)


def comparer_deux_algos(filepath):
    """Compare Force Brute vs DP"""
    actions = charger_donnees(filepath)
    if not actions:
        return
    
    results = ResultsManager()
    
    # Force Brute
    print(f"\n⏳ FORCE BRUTE...")
    bf = BruteForceResolver(actions, max_budget=500000)
    bf_portfolio = bf.solve()
    results.set_brute_force_result(bf)
    print(f"   ✓ Temps: {bf.execution_time:.3f}s ({bf.iterations:,} itérations)")
    
    # DP
    print(f"\n⚡ PROGRAMMATION DYNAMIQUE...")
    dp = DynamicProgrammingResolver(actions, max_budget=500000)
    dp_portfolio = dp.solve()
    results.set_dp_result(dp)
    print(f"   ✓ Temps: {dp.execution_time:.3f}s")
    
    # Comparaison
    results.compare()
    results.display_results()


def afficher_resultats_bf(bf, portfolio):
    """Affiche les résultats Force Brute"""
    stats = bf.get_stats()
    print("="*70)
    print("✅ RÉSULTATS - FORCE BRUTE")
    print("="*70)
    print(f"\nCoût total: {stats['total_cost']:,.0f} F CFA")
    print(f"Profit total: {stats['total_profit']:,.0f} F CFA")
    print(f"Nombre d'actions: {stats['actions_count']}")
    print(f"Itérations: {stats['iterations']:,}")
    print(f"Temps: {stats['execution_time']:.6f}s")
    print(f"Ratio profit: {portfolio.get_profit_ratio():.4f}")
    
    print(f"\n📋 Actions ({len(portfolio.actions)}):")
    print("-"*70)
    print(f"{'Action':<15} {'Coût':<15} {'Profit %':<15} {'Profit':<15}")
    print("-"*70)
    
    for action in sorted(portfolio.actions, key=lambda a: a.cost, reverse=True):
        print(f"{action.name:<15} {action.cost:>12,.0f} {action.profit_pct*100:>13.2f}% {action.get_profit():>12,.0f}")
    
    print("-"*70)
    print(f"{'TOTAL':<15} {portfolio.get_total_cost():>12,.0f} {portfolio.get_profit_ratio()*100:>13.2f}% {portfolio.get_total_profit():>12,.0f}")
    print("="*70)


def afficher_resultats_dp(dp, portfolio):
    """Affiche les résultats DP"""
    stats = dp.get_stats()
    print("="*70)
    print("✅ RÉSULTATS - PROGRAMMATION DYNAMIQUE")
    print("="*70)
    print(f"\nCoût total: {stats['total_cost']:,.0f} F CFA")
    print(f"Profit total: {stats['total_profit']:,.0f} F CFA")
    print(f"Nombre d'actions: {stats['actions_count']}")
    print(f"Temps: {stats['execution_time']:.6f}s")
    print(f"Ratio profit: {portfolio.get_profit_ratio():.4f}")
    
    print(f"\n📋 Actions ({len(portfolio.actions)}):")
    print("-"*70)
    print(f"{'Action':<15} {'Coût':<15} {'Profit %':<15} {'Profit':<15}")
    print("-"*70)
    
    for action in sorted(portfolio.actions, key=lambda a: a.cost, reverse=True):
        print(f"{action.name:<15} {action.cost:>12,.0f} {action.profit_pct*100:>13.2f}% {action.get_profit():>12,.0f}")
    
    print("-"*70)
    print(f"{'TOTAL':<15} {portfolio.get_total_cost():>12,.0f} {portfolio.get_profit_ratio()*100:>13.2f}% {portfolio.get_total_profit():>12,.0f}")
    print("="*70)


def comparer_tous_datasets():
    """Compare les trois datasets avec DP"""
    datasets = [
        ('data_test.csv', 'Data Test (20 actions)'),
        ('dataset1_Python+P3.csv', 'Dataset 1 (25 actions)'),
        ('dataset2_Python+P3.csv', 'Dataset 2 (541 actions)')
    ]
    
    resultats = []
    
    for filepath, nom in datasets:
        actions = charger_donnees(filepath)
        if not actions:
            continue
        
        print(f"\n⚡ Test DP sur {nom}...")
        dp = DynamicProgrammingResolver(actions, max_budget=500000)
        portfolio = dp.solve()
        
        resultats.append({
            'dataset': nom,
            'actions': len(actions),
            'temps': dp.execution_time,
            'profit': portfolio.get_total_profit(),
            'cout': portfolio.get_total_cost(),
            'selected': len(portfolio.actions)
        })
        
        print(f"   ✓ {len(portfolio.actions)} actions, Profit: {portfolio.get_total_profit():,.0f} F CFA, Temps: {dp.execution_time:.3f}s")
    
    # Afficher le résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ COMPARATIF - PROGRAMMATION DYNAMIQUE")
    print("="*70)
    print(f"\n{'Dataset':<25} {'Actions':<10} {'Sélect.':<10} {'Profit':<20} {'Temps':<15}")
    print("-"*70)
    
    for r in resultats:
        print(f"{r['dataset']:<25} {r['actions']:<10} {r['selected']:<10} {r['profit']:>18,.0f} {r['temps']:>13.3f}s")
    
    print("="*70)


def main():
    """Fonction principale"""
    while True:
        afficher_menu()
        choix = input("\n👉 Choisir une option (1-7): ").strip()
        
        if choix == '1':
            test_force_brute('data_test.csv')
        
        elif choix == '2':
            test_dp('data_test.csv')
        
        elif choix == '3':
            comparer_deux_algos('data_test.csv')
        
        elif choix == '4':
            test_dp('dataset1_Python+P3.csv')
        
        elif choix == '5':
            test_dp('dataset2_Python+P3.csv')
        
        elif choix == '6':
            comparer_tous_datasets()
        
        elif choix == '7':
            print("\n👋 Au revoir!\n")
            break
        
        else:
            print("\n❌ Option invalide. Essayer encore.")
        
        input("\n✋ Appuyer sur ENTER pour continuer...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
