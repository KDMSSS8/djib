"""Chargeur de données depuis fichiers CSV"""
import csv
import os
from models.action import Action


class DataLoader:
    """Charge des actions depuis des fichiers CSV"""

    @staticmethod
    def load_from_csv(filepath):
        """
        Charge les actions depuis un fichier CSV
        Détecte automatiquement le délimiteur (virgule ou point-virgule)
        Gère différents noms de colonnes
        
        Args:
            filepath: Chemin du fichier CSV
            
        Returns:
            Liste d'Action ou liste vide si erreur
        """
        if not os.path.exists(filepath):
            print(f"✗ Fichier non trouvé : {filepath}")
            return []
        
        try:
            # Lire la première ligne pour détecter le délimiteur
            with open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()
            
            delimiter = ';' if ';' in first_line else ','
            
            # Lire le CSV avec le bon délimiteur
            actions = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                
                for row in reader:
                    # Chercher les colonnes
                    name = None
                    cost = None
                    profit_pct = None
                    
                    # Chercher le nom de l'action
                    for col in ['name', 'id', 'Actions', 'Name', 'ID', 'ACTIONS']:
                        if col in row:
                            name = row[col]
                            break
                    
                    if not name:
                        continue
                    
                    # Chercher le coût
                    for col in ['price', 'cost', 'B', 'A', 'Price', 'Cost', 'PRICE', 'COST']:
                        if col in row:
                            try:
                                cost = float(row[col].replace(',', '.'))
                                break
                            except (ValueError, AttributeError):
                                pass
                    
                    # Chercher le profit %
                    for col in ['profit_pct', 'Bénéfice après 2 ans', 'C', 'Profit_pct', 'PROFIT_PCT', 'profit%', 'PROFIT%']:
                        if col in row:
                            try:
                                profit_value = row[col].replace(',', '.').replace('%', '')
                                profit_pct = float(profit_value) / 100 if float(profit_value) > 1 else float(profit_value)
                                break
                            except (ValueError, AttributeError):
                                pass
                    
                    # Valider les données
                    if name and cost and profit_pct and cost > 0:
                        action = Action(name=name, cost=cost, profit_pct=profit_pct)
                        actions.append(action)
            
            print(f"✓ {len(actions)} actions chargées")
            return actions
            
        except Exception as e:
            print(f"✗ Erreur: {str(e)}")
            return []
