from itertools import combinations
import time
from models.portfolio import Portfolio


class BruteForceResolver:
    """O(2^n) - Teste toutes les 2^n combinaisons possibles"""
    
    def __init__(self, actions, max_budget=500000):
        self.actions = actions
        self.max_budget = max_budget
        self.best_portfolio = None
        self.iterations = 0
        self.execution_time = 0
    
    def solve(self):
        start_time = time.time()
        best_profit = 0
        best_portfolio = Portfolio([])
        
        for r in range(len(self.actions) + 1):
            for combination in combinations(self.actions, r):
                self.iterations += 1
                portfolio = Portfolio(list(combination))
                if portfolio.is_valid(self.max_budget):
                    current_profit = portfolio.get_total_profit()
                    if current_profit > best_profit:
                        best_profit = current_profit
                        best_portfolio = portfolio
        
        self.execution_time = time.time() - start_time
        self.best_portfolio = best_portfolio
        return best_portfolio
    
    def get_stats(self):
        return {
            'method': 'Brute Force',
            'iterations': self.iterations,
            'execution_time': self.execution_time,
            'total_cost': self.best_portfolio.get_total_cost(),
            'total_profit': self.best_portfolio.get_total_profit(),
            'actions_count': len(self.best_portfolio.actions)
        }
