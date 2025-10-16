# Échecs game logic

from datetime import datetime
import random
from typing import List, Optional, Dict, Any
from tinydb import TinyDB
import os

# Création du dossier data s'il n'existe pas
if not os.path.exists('data'):
    os.makedirs('data')

# Initialisation de la base de données
db = TinyDB('data/chess_tournament.json')
joueurs_table = db.table('joueurs')
tournois_table = db.table('tournois')


class Joueur:
    def __init__(self, nom_famille: str, prenom: str, date_naissance: str, sexe: str, classement: int,
                 id: Optional[int] = None):
        self.nom_famille = nom_famille
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.classement = max(1, classement)  # Assure que le classement est positif
        self.points = 0
        self.id = id

    def to_dict(self) -> Dict[str, Any]:
        """Convertit le joueur en dictionnaire pour stockage"""
        return {
            'nom_famille': self.nom_famille,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance,
            'sexe': self.sexe,
            'classement': self.classement
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], id: Optional[int] = None) -> 'Joueur':
        """Crée une instance de Joueur à partir d'un dictionnaire"""
        joueur = cls(
            nom_famille=data['nom_famille'],
            prenom=data['prenom'],
            date_naissance=data['date_naissance'],
            sexe=data['sexe'],
            classement=data['classement'],
            id=id
        )
        return joueur

    def save(self) -> int:
        """Sauvegarde le joueur dans la base de données"""
        if self.id is None:
            self.id = joueurs_table.insert(self.to_dict())
        else:
            joueurs_table.update(self.to_dict(), doc_ids=[self.id])
        return self.id

    @classmethod
    def get_all(cls) -> List['Joueur']:
        """Récupère tous les joueurs de la base de données"""
        return [cls.from_dict(item, id=item.doc_id) for item in joueurs_table.all()]

    def __str__(self):
        return f"{self.prenom} {self.nom_famille} (Classement: {self.classement})"


class Match:
    def __init__(self, joueur1: 'Joueur', joueur2: 'Joueur'):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.resultat = None  # (1, 0) victoire j1, (0, 1) victoire j2, (0.5, 0.5) nul

    def __str__(self):
        score = "vs"
        if self.resultat:
            score = f"{self.resultat[0]}-{self.resultat[1]}"
        return f"{self.joueur1.prenom} {self.joueur1.nom_famille} {score} " \
               f"{self.joueur2.prenom} {self.joueur2.nom_famille}"


class Tour:
    def __init__(self, nom: str):
        self.nom = nom
        self.debut = datetime.now()
        self.fin: Optional[datetime] = None
        self.matches: List[Match] = []

    def ajouter_match(self, match: Match):
        self.matches.append(match)

    def terminer_tour(self):
        self.fin = datetime.now()

    def __str__(self):
        return f"{self.nom} - {len(self.matches)} matches"


class Tournoi:
    CONTROLES_TEMPS = ["bullet", "blitz", "rapide"]

    def __init__(self, nom: str, lieu: str, date_debut: str, date_fin: str, nb_tours: int = 4,
                 controle_temps: str = "bullet", description: str = "", id: Optional[int] = None):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_tours = nb_tours
        self.tours: List[Tour] = []
        self.joueurs: List[int] = []  # Liste des IDs des joueurs
        self.id = id

        if controle_temps.lower() not in self.CONTROLES_TEMPS:
            raise ValueError(f"Le contrôle du temps doit être parmi : {', '.join(self.CONTROLES_TEMPS)}")
        self.controle_temps = controle_temps.lower()

        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """Convertit le tournoi en dictionnaire pour stockage"""
        return {
            'nom': self.nom,
            'lieu': self.lieu,
            'date_debut': self.date_debut,
            'date_fin': self.date_fin,
            'nb_tours': self.nb_tours,
            'controle_temps': self.controle_temps,
            'description': self.description,
            'joueurs': self.joueurs,
            'tours': [
                {
                    'nom': tour.nom,
                    'debut': tour.debut.isoformat() if tour.debut else None,
                    'fin': tour.fin.isoformat() if tour.fin else None,
                    'matches': [
                        {
                            'joueur1_id': match.joueur1.id,
                            'joueur2_id': match.joueur2.id,
                            'resultat': match.resultat
                        } for match in tour.matches
                    ]
                } for tour in self.tours
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], id: Optional[int] = None) -> 'Tournoi':
        """Crée une instance de Tournoi à partir d'un dictionnaire"""
        tournoi = cls(
            nom=data['nom'],
            lieu=data['lieu'],
            date_debut=data['date_debut'],
            date_fin=data['date_fin'],
            nb_tours=data['nb_tours'],
            controle_temps=data['controle_temps'],
            description=data['description'],
            id=id
        )
        tournoi.joueurs = data['joueurs']

        # Récupération des joueurs
        joueurs_dict = {j.doc_id: j for j in joueurs_table.all()}

        # Reconstruction des tours et matches
        for tour_data in data.get('tours', []):
            tour = Tour(tour_data['nom'])
            if tour_data['debut']:
                tour.debut = datetime.fromisoformat(tour_data['debut'])
            if tour_data['fin']:
                tour.fin = datetime.fromisoformat(tour_data['fin'])

            for match_data in tour_data['matches']:
                joueur1_data = joueurs_dict[match_data['joueur1_id']]
                joueur2_data = joueurs_dict[match_data['joueur2_id']]
                joueur1 = Joueur.from_dict(joueur1_data, match_data['joueur1_id'])
                joueur2 = Joueur.from_dict(joueur2_data, match_data['joueur2_id'])
                match = Match(joueur1, joueur2)
                match.resultat = match_data['resultat']
                tour.matches.append(match)

            tournoi.tours.append(tour)

        return tournoi

    def save(self) -> int:
        """Sauvegarde le tournoi dans la base de données"""
        if self.id is None:
            self.id = tournois_table.insert(self.to_dict())
        else:
            tournois_table.update(self.to_dict(), doc_ids=[self.id])
        return self.id

    @classmethod
    def get_all(cls) -> List['Tournoi']:
        """Récupère tous les tournois de la base de données"""
        return [cls.from_dict(item, id=item.doc_id) for item in tournois_table.all()]

    def get_joueurs_objets(self) -> List[Joueur]:
        """Récupère les objets Joueur à partir des IDs stockés"""
        joueurs_objets = []
        all_joueurs = {j.doc_id: j for j in joueurs_table.all()}
        for joueur_id in self.joueurs:
            if joueur_id in all_joueurs:
                joueur_data = all_joueurs[joueur_id]
                joueurs_objets.append(Joueur.from_dict(joueur_data, id=joueur_id))
        return joueurs_objets

    def liste_joueurs_alphabetique(self) -> List[Joueur]:
        """Retourne la liste des joueurs du tournoi par ordre alphabétique"""
        joueurs = self.get_joueurs_objets()
        return sorted(joueurs, key=lambda j: (j.nom_famille.lower(), j.prenom.lower()))

    def liste_joueurs_classement(self) -> List[Joueur]:
        """Retourne la liste des joueurs du tournoi par classement"""
        joueurs = self.get_joueurs_objets()
        return sorted(joueurs, key=lambda j: j.classement, reverse=True)

    def liste_tours(self) -> List[Tour]:
        """Retourne la liste de tous les tours du tournoi"""
        return self.tours

    def liste_matches(self) -> List[Match]:
        """Retourne la liste de tous les matches du tournoi"""
        matches = []
        for tour in self.tours:
            matches.extend(tour.matches)
        return matches

    def __str__(self):
        return f"Tournoi {self.nom} à {self.lieu} ({self.date_debut} - {self.date_fin})"

    def ajouter_joueur(self, joueur: Joueur):
        """Ajoute un joueur au tournoi"""
        if len(self.joueurs) < 8:
            if joueur.id not in self.joueurs:
                self.joueurs.append(joueur.id)
                self.save()
                print(f"✅ Joueur ajouté au tournoi : {joueur}")
        else:
            print("⚠️ Maximum de 8 joueurs atteint.")

    def generer_paires(self) -> List[tuple]:
        """Génère les paires de joueurs pour un tour"""
        joueurs = self.get_joueurs_objets()
        
        if len(joueurs) < 2:
            return []
        
        joueurs_tries = sorted(joueurs, key=lambda j: j.points, reverse=True)
        random.shuffle(joueurs_tries)
        
        # Générer les paires en prenant 2 joueurs à la fois
        paires = []
        for i in range(0, len(joueurs_tries) - 1, 2):
            paires.append((joueurs_tries[i], joueurs_tries[i + 1]))
        
        return paires

    def jouer_tour(self):
        """Lance un tour de tournoi"""
        tour_num = len(self.tours) + 1
        print(f"\n=== Tour {tour_num} ===")

        joueurs = self.get_joueurs_objets()
        
        if len(joueurs) < 2:
            print("⚠️ Le tournoi doit avoir au moins 2 joueurs.")
            return

        tour = Tour(f"Tour {tour_num}")
        paires = self.generer_paires()

        if not paires:
            print("⚠️ Impossible de générer des paires de joueurs.")
            return

        for j1, j2 in paires:
            print(f"\nPartie : {j1.prenom} {j1.nom_famille} vs {j2.prenom} {j2.nom_famille}")
            print("Résultat : 1 = victoire du 1er | 2 = victoire du 2e | 0 = nul")
            res = input("→ Entrez le résultat : ")

            match = Match(j1, j2)

            if res == "1":
                j1.points += 1
                match.resultat = (1, 0)
            elif res == "2":
                j2.points += 1
                match.resultat = (0, 1)
            elif res == "0":
                j1.points += 0.5
                j2.points += 0.5
                match.resultat = (0.5, 0.5)
            else:
                print("Résultat invalide, partie comptée nulle.")
                j1.points += 0.5
                j2.points += 0.5
                match.resultat = (0.5, 0.5)

            tour.ajouter_match(match)

        tour.terminer_tour()
        self.tours.append(tour)
        self.save()
        self.afficher_classement()

    def afficher_classement(self):
        """Affiche le classement actuel du tournoi"""
        print("\n🏁 Classement actuel :")
        joueurs = self.get_joueurs_objets()
        classement = sorted(joueurs, key=lambda j: j.points, reverse=True)
        for i, j in enumerate(classement, 1):
            print(f"{i}. {j.prenom} {j.nom_famille} - {j.points} pts")

    def tournoi_termine(self):
        """Termine le tournoi et affiche le classement final"""
        print("\n🎉 Tournoi terminé ! Classement final :")
        self.afficher_classement()
        self.save()


class GestionnaireTournois:
    def __init__(self):
        self.load_data()

    def load_data(self):
        """Charge les données depuis la base de données"""
        self.tournois = Tournoi.get_all()
        self.joueurs = Joueur.get_all()

    def ajouter_joueur(self, joueur: Joueur):
        """Ajoute un joueur à la base de données"""
        joueur.save()
        self.joueurs.append(joueur)

    def ajouter_tournoi(self, tournoi: 'Tournoi'):
        """Ajoute un tournoi à la base de données"""
        tournoi.save()
        self.tournois.append(tournoi)

    def liste_joueurs_alphabetique(self) -> List[Joueur]:
        """Retourne la liste de tous les joueurs par ordre alphabétique"""
        return sorted(self.joueurs, key=lambda j: (j.nom_famille.lower(), j.prenom.lower()))

    def liste_joueurs_classement(self) -> List[Joueur]:
        """Retourne la liste de tous les joueurs par classement"""
        return sorted(self.joueurs, key=lambda j: j.classement, reverse=True)

    def liste_tournois(self) -> List['Tournoi']:
        """Retourne la liste de tous les tournois"""
        return self.tournois


def afficher_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Créer un nouveau tournoi")
    print("2. Ajouter un joueur global")
    print("3. Ajouter un joueur à un tournoi")
    print("4. Lancer une partie")
    print("5. Afficher les rapports")
    print("6. Quitter")
    return input("Choix : ")


def menu_rapports(gestionnaire: GestionnaireTournois):
    while True:
        print("\n=== MENU RAPPORTS ===")
        print("1. Liste des joueurs par ordre alphabétique")
        print("2. Liste des joueurs par classement")
        print("3. Liste de tous les tournois")
        print("4. Détails d'un tournoi spécifique")
        print("5. Retour au menu principal")

        choix = input("Choix : ")

        if choix == "1":
            print("\nListe des joueurs par ordre alphabétique:")
            for joueur in gestionnaire.liste_joueurs_alphabetique():
                print(f"- {joueur}")

        elif choix == "2":
            print("\nListe des joueurs par classement:")
            for joueur in gestionnaire.liste_joueurs_classement():
                print(f"- {joueur}")

        elif choix == "3":
            print("\nListe des tournois:")
            for tournoi in gestionnaire.liste_tournois():
                print(f"- {tournoi}")

        elif choix == "4":
            if not gestionnaire.tournois:
                print("Aucun tournoi disponible.")
                continue

            print("\nTournois disponibles:")
            for i, tournoi in enumerate(gestionnaire.tournois, 1):
                print(f"{i}. {tournoi.nom}")

            try:
                choix_tournoi = int(input("Numéro du tournoi : ")) - 1
                tournoi = gestionnaire.tournois[choix_tournoi]

                print(f"\nDétails du tournoi {tournoi.nom}:")
                print("\nJoueurs par ordre alphabétique:")
                for joueur in tournoi.liste_joueurs_alphabetique():
                    print(f"- {joueur}")

                print("\nJoueurs par classement:")
                for joueur in tournoi.liste_joueurs_classement():
                    print(f"- {joueur}")

                print("\nTours:")
                for tour in tournoi.liste_tours():
                    print(f"\n{tour}")
                    for match in tour.matches:
                        print(f"  - {match}")

            except (ValueError, IndexError):
                print("Choix invalide.")

        elif choix == "5":
            break


def ajouter_joueur_au_tournoi(gestionnaire: GestionnaireTournois):
    """Ajoute un joueur existant à un tournoi"""
    if not gestionnaire.joueurs:
        print("\n⚠️ Aucun joueur dans la base de données.")
        return

    if not gestionnaire.tournois:
        print("\n⚠️ Aucun tournoi disponible.")
        return

    print("\nJoueurs disponibles:")
    for i, joueur in enumerate(gestionnaire.joueurs, 1):
        print(f"{i}. {joueur}")

    try:
        choix_joueur = int(input("Numéro du joueur : ")) - 1
        joueur = gestionnaire.joueurs[choix_joueur]

        print("\nTournois disponibles:")
        for i, tournoi in enumerate(gestionnaire.tournois, 1):
            print(f"{i}. {tournoi.nom} ({len(tournoi.joueurs)}/8 joueurs)")

        choix_tournoi = int(input("Numéro du tournoi : ")) - 1
        tournoi = gestionnaire.tournois[choix_tournoi]

        if len(tournoi.joueurs) >= 8:
            print("⚠️ Ce tournoi a atteint le maximum de 8 joueurs.")
            return

        if joueur.id in tournoi.joueurs:
            print("⚠️ Ce joueur est déjà dans ce tournoi.")
            return

        tournoi.ajouter_joueur(joueur)
        print(f"\n✅ {joueur} a été ajouté au tournoi {tournoi.nom}!")

    except (ValueError, IndexError):
        print("\n⚠️ Choix invalide.")
    except KeyboardInterrupt:
        print("\n⚠️ Opération annulée.")


def lancer_partie(gestionnaire: GestionnaireTournois):
    """Permet de lancer un tour d'un tournoi"""
    if not gestionnaire.tournois:
        print("\n⚠️ Aucun tournoi disponible.")
        return

    print("\nTournois disponibles:")
    for i, tournoi in enumerate(gestionnaire.tournois, 1):
        print(f"{i}. {tournoi.nom} ({len(tournoi.joueurs)} joueurs)")

    try:
        choix_tournoi = int(input("Numéro du tournoi : ")) - 1
        tournoi = gestionnaire.tournois[choix_tournoi]

        if len(tournoi.joueurs) < 2:
            print("⚠️ Le tournoi doit avoir au moins 2 joueurs pour lancer une partie.")
            return

        print(f"\n{tournoi.nom} - Tours: {len(tournoi.tours)}/{tournoi.nb_tours}")

        if len(tournoi.tours) >= tournoi.nb_tours:
            print("⚠️ Ce tournoi a déjà atteint le nombre de tours maximum.")
            return

        print(f"\nLancement du tour suivant...\n")
        try:
            tournoi.jouer_tour()
            gestionnaire.ajouter_tournoi(tournoi)
            print("\n✅ Tour enregistré avec succès!")
        except KeyboardInterrupt:
            print("\n⚠️ Tour annulé.")
        except ValueError:
            print("\n⚠️ Erreur lors de la saisie.")

    except (ValueError, IndexError):
        print("⚠️ Choix invalide.")


def main():
    print("♟️  Bienvenue dans le gestionnaire de tournoi d'échecs ♟️")
    gestionnaire = GestionnaireTournois()

    while True:
        choix = afficher_menu()

        if choix == "1":
            # Création du tournoi
            nom_tournoi = input("Nom du tournoi : ")
            lieu = input("Lieu du tournoi : ")
            date_debut = input("Date de début (YYYY-MM-DD) : ")
            date_fin = input("Date de fin (YYYY-MM-DD) : ")
            controle_temps = input("Contrôle du temps (bullet/blitz/rapide) : ")
            description = input("Description du tournoi : ")

            tournoi = Tournoi(nom_tournoi, lieu, date_debut, date_fin,
                              controle_temps=controle_temps, description=description)
            gestionnaire.ajouter_tournoi(tournoi)

            print("\nAjoutez jusqu'à 8 joueurs :")
            try:
                while len(tournoi.joueurs) < 8:
                    print(f"\nJoueur {len(tournoi.joueurs) + 1} :")
                    print("(ou tapez 'stop' pour terminer)")
                    nom_famille = input("Nom de famille : ")
                    if nom_famille.lower() == "stop":
                        break

                    prenom = input("Prénom : ")
                    date_naissance = input("Date de naissance (YYYY-MM-DD) : ")
                    sexe = input("Sexe (M/F) : ")
                    classement = int(input("Classement : "))

                    joueur = Joueur(nom_famille, prenom, date_naissance, sexe, classement)
                    tournoi.ajouter_joueur(joueur)
                    gestionnaire.ajouter_joueur(joueur)
                    print(f"✅ Joueur ajouté : {joueur}")

                print(f"\n✅ Tournoi '{tournoi.nom}' créé avec succès!")
                print(f"   Joueurs: {len(tournoi.joueurs)}/8")
                print(f"   Tours à jouer: {tournoi.nb_tours}")
            except KeyboardInterrupt:
                print("\n\n⚠️ Création de tournoi annulée.")
            except ValueError:
                print("\n⚠️ Erreur : Veuillez entrer des données valides.")

        elif choix == "2":
            print("\nAjout d'un nouveau joueur:")
            try:
                nom_famille = input("Nom de famille : ")
                prenom = input("Prénom : ")
                date_naissance = input("Date de naissance (YYYY-MM-DD) : ")
                sexe = input("Sexe (M/F) : ")
                classement = int(input("Classement : "))

                joueur = Joueur(nom_famille, prenom, date_naissance, sexe, classement)
                gestionnaire.ajouter_joueur(joueur)
                print(f"✅ Joueur ajouté : {joueur}")
            except KeyboardInterrupt:
                print("\n\n⚠️ Ajout de joueur annulé.")
            except ValueError:
                print("\n⚠️ Erreur : Veuillez entrer des données valides.")

        elif choix == "3":
            ajouter_joueur_au_tournoi(gestionnaire)

        elif choix == "4":
            lancer_partie(gestionnaire)

        elif choix == "5":
            menu_rapports(gestionnaire)

        elif choix == "6":
            print("Au revoir!")
            break

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()
