"""Gestionnaire de résultats et comparaisons"""
import json
import os


class ResultsManager:
    """Gère et compare les résultats des algorithmes"""
    
    def __init__(self):
        """Initialise le gestionnaire"""
        self.brute_force_result = None
        self.dp_result = None
    
    def set_brute_force_result(self, resolver):
        """Enregistre le résultat Brute Force"""
        self.brute_force_result = resolver
    
    def set_dp_result(self, resolver):
        """Enregistre le résultat DP"""
        self.dp_result = resolver
    
    def compare(self):
        """Compare les deux résultats"""
        if not self.brute_force_result or not self.dp_result:
            return None
        
        bf_stats = self.brute_force_result.get_stats()
        dp_stats = self.dp_result.get_stats()
        
        speedup = bf_stats['execution_time'] / dp_stats['execution_time']
        
        return {
            'brute_force': bf_stats,
            'dynamic_programming': dp_stats,
            'speedup': speedup,
            'same_solution': bf_stats['total_profit'] == dp_stats['total_profit']
        }
    
    def export_to_json(self, filename='resultats.json'):
        """Exporte les résultats en JSON"""
        comparison = self.compare()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)
        
        return f"✓ Résultats exportés vers {filename}"
