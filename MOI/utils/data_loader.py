import csv
from models.action import Action


class DataLoader:
    """Charge les données d'actions depuis un fichier CSV."""
    
    @staticmethod
    def load_from_csv(filepath):
        actions = []
        try:
            # Déterminer le séparateur
            with open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                delimiter = ';' if ';' in first_line else ','
            
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                for row in reader:
                    name = row.get('id') or row.get('name') or row.get('Actions')
                    
                    # Cherche le coût (price, cost, etc.)
                    cost = None
                    for col in ['price', 'cost', 'Cost par action', 'B', 'A']:
                        val = row.get(col)
                        if val and val.strip():
                            try:
                                cost_float = float(val)
                                if cost_float > 0:  # Ignore valeurs négatives
                                    cost = str(cost_float)
                                    break
                            except:
                                pass
                    
                    # Cherche le profit (profit_pct, Bénéfice, etc.)
                    profit_pct = None
                    for col in ['profit_pct', 'Bénéfice après 2 ans', 'C', 'B']:
                        val = row.get(col)
                        if val and val.strip() and (col != 'B' or cost != val):
                            profit_pct = val
                            break
                    
                    if name and cost and profit_pct:
                        try:
                            profit_str = str(profit_pct).strip().replace('%', '')
                            profit_val = float(profit_str)
                            profit_normalized = profit_val / 100 if profit_val > 1 else profit_val
                            cost_val = float(cost)
                            
                            if cost_val > 0:
                                action = Action(name=str(name).strip(), cost=cost_val, profit_pct=profit_normalized)
                                actions.append(action)
                        except ValueError:
                            pass
            
            print(f"✓ {len(actions)} actions chargées depuis {filepath}")
            return actions
        
        except FileNotFoundError:
            print(f"✗ Fichier non trouvé : {filepath}")
            return []
        except Exception as e:
            print(f"✗ Erreur : {e}")
            return []
