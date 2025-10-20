import json
from datetime import datetime


class ResultsManager:
    """Gère et compare les résultats des deux méthodes."""
    
    def __init__(self):
        self.brute_force_result = None
        self.dp_result = None
        self.comparison = None
    
    def set_brute_force_result(self, resolver):
        self.brute_force_result = resolver.get_stats()
    
    def set_dp_result(self, resolver):
        self.dp_result = resolver.get_stats()
    
    def compare(self):
        if not self.brute_force_result or not self.dp_result:
            return None
        
        bf = self.brute_force_result
        dp = self.dp_result
        
        self.comparison = {
            'brute_force': bf,
            'dynamic_programming': dp,
            'speedup': bf.get('execution_time', 1) / dp.get('execution_time', 1),
            'same_profit': abs(bf['total_profit'] - dp['total_profit']) < 0.01,
            'same_cost': abs(bf['total_cost'] - dp['total_cost']) < 0.01,
        }
        return self.comparison
    
    def display_results(self):
        print("\n" + "="*70)
        print("RÉSULTATS COMPARATIFS")
        print("="*70)
        
        print("\n📊 FORCE BRUTE (O(2^n))")
        self._print_dict(self.brute_force_result)
        
        print("\n⚡ PROGRAMMATION DYNAMIQUE (O(n×W))")
        self._print_dict(self.dp_result)
        
        if self.comparison:
            speedup = self.comparison['speedup']
            print(f"\n🚀 SPEEDUP: {speedup:.1f}x plus rapide")
            print(f"✅ Même solution : {'OUI' if self.comparison['same_profit'] and self.comparison['same_cost'] else 'NON'}")
        print("="*70 + "\n")
    
    def export_to_json(self, filepath):
        data = {
            'timestamp': datetime.now().isoformat(),
            'brute_force': self.brute_force_result,
            'dynamic_programming': self.dp_result,
            'comparison': self.comparison
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Exporté : {filepath}")
    
    @staticmethod
    def _print_dict(data):
        if not data:
            return
        for key, value in data.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.3f}" if 'time' in key else f"  {key}: {value:,.2f}")
            else:
                print(f"  {key}: {value}")
