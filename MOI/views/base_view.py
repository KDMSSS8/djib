"""
Vue de base pour l'affichage des données.
"""

class BaseView:
    """Classe de base pour toutes les vues."""
    
    def __init__(self):
        pass
    
    def display(self, message):
        """Affiche un message."""
        print(message)
    
    def display_error(self, error):
        """Affiche une erreur."""
        print(f"❌ Erreur: {error}")
    
    def display_success(self, message):
        """Affiche un message de succès."""
        print(f"✅ {message}")
    
    def display_info(self, message):
        """Affiche un message informatif."""
        print(f"ℹ️  {message}")
