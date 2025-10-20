"""
Utilitaire de journalisation.
"""

import logging
from datetime import datetime

class Logger:
    """Gestionnaire de logs pour l'application."""
    
    def __init__(self, name=__name__, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Format du log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Handler pour console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log un message d'information."""
        self.logger.info(message)
    
    def error(self, message):
        """Log une erreur."""
        self.logger.error(message)
    
    def warning(self, message):
        """Log un avertissement."""
        self.logger.warning(message)
    
    def debug(self, message):
        """Log un message de débogage."""
        self.logger.debug(message)
