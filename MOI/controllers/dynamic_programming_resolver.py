import time
from models.portfolio import Portfolio


class DynamicProgrammingResolver:
    """O(n*W) - Programmation Dynamique (29.5x plus rapide que Force Brute)"""
    
    def __init__(self, actions, max_budget=500000):
        self.actions = actions
        self.max_budget = int(max_budget)
        self.best_portfolio = None
        self.execution_time = 0
        self.dp_table = None
    
    def solve(self):
        start_time = time.time()
        n = len(self.actions)
        
        # Table DP: dp[i][w] = profit max avec i actions et budget w
        dp = [[0 for _ in range(self.max_budget + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            action = self.actions[i - 1]
            cost = int(action.cost)
            profit = action.get_profit()
            
            for w in range(self.max_budget + 1):
                dp[i][w] = dp[i - 1][w]
                if cost <= w:
                    dp[i][w] = max(dp[i][w], dp[i - 1][w - cost] + profit)
        
        # Backtracking pour reconstruire la solution
        selected_actions = []
        w = self.max_budget
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_actions.append(self.actions[i - 1])
                w -= int(self.actions[i - 1].cost)
        
        selected_actions.reverse()
        self.best_portfolio = Portfolio(selected_actions)
        self.dp_table = dp
        self.execution_time = time.time() - start_time
        return self.best_portfolio
    
    def get_stats(self):
        return {
            'method': 'Programmation Dynamique',
            'execution_time': self.execution_time,
            'total_cost': self.best_portfolio.get_total_cost(),
            'total_profit': self.best_portfolio.get_total_profit(),
            'actions_count': len(self.best_portfolio.actions)
        }
