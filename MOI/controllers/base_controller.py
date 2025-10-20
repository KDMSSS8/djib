"""
Contrôleur de base pour gérer la logique métier.
"""

class BaseController:
    """Classe de base pour tous les contrôleurs."""
    
    def __init__(self, model, view):
        """
        Initialise le contrôleur.
        
        Args:
            model: Le modèle de données
            view: La vue pour l'affichage
        """
        self.model = model
        self.view = view
    
    def process(self):
        """Traite les données. À implémenter dans les sous-classes."""
        raise NotImplementedError("La méthode process doit être implémentée.")
