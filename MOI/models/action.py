from models.base_model import BaseModel


class Action(BaseModel):
    """Représente une action à acheter."""
    
    def __init__(self, name, cost, profit_pct):
        super().__init__()
        self.name = name
        self.cost = float(cost)
        self.profit_pct = float(profit_pct)
    
    def get_profit(self):
        """Profit total = cost * profit_pct"""
        return self.cost * self.profit_pct
    
    def __repr__(self):
        return f"Action({self.name}, cost={self.cost:.0f}, profit%={self.profit_pct*100:.1f}%)"
