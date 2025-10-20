"""
Modèle de base pour tous les modèles de l'application.
"""

class BaseModel:
    """Classe de base pour tous les modèles."""
    
    def __init__(self):
        pass
    
    def to_dict(self):
        """Convertit le modèle en dictionnaire."""
        return self.__dict__
    
    def __repr__(self):
        return f"<{self.__class__.__name__}({self.to_dict()})>"
