from models.base_model import BaseModel


class Portfolio(BaseModel):
    """Représente un portefeuille d'actions."""
    
    def __init__(self, actions=None):
        super().__init__()
        self.actions = actions if actions else []
    
    def add_action(self, action):
        """Ajoute une action au portefeuille."""
        self.actions.append(action)
    
    def get_total_cost(self):
        return sum(action.cost for action in self.actions)
    
    def get_total_profit(self):
        return sum(action.get_profit() for action in self.actions)
    
    def get_profit_ratio(self):
        total_cost = self.get_total_cost()
        return self.get_total_profit() / total_cost if total_cost > 0 else 0
    
    def is_valid(self, max_budget):
        return self.get_total_cost() <= max_budget
    
    def __repr__(self):
        return (f"Portfolio(Actions: {len(self.actions)}, "
                f"Cost: {self.get_total_cost():,.0f}, "
                f"Profit: {self.get_total_profit():,.0f})")
