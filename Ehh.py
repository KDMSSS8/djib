# Échecs game logic
from datetime import datetime
import random
from typing import List, Optional, Dict, Any
from tinydb import TinyDB
import os

# Création du dossier data et initialisation de la baseh,  de données
os.makedirs('data', exist_ok=True)
db = TinyDB('data/chess_tournament.json')
joueurs_table, tournois_table = db.table('joueurs'), db.table('tournois')


class Joueur:
    def __init__(self, nom_famille: str, prenom: str, date_naissance: str, sexe: str, classement: int,
                 id: Optional[int] = None):
        self.nom_famille, self.prenom = nom_famille, prenom
        self.date_naissance, self.sexe = date_naissance, sexe
        self.classement, self.points, self.id = max(1, classement), 0, id

    def to_dict(self) -> Dict[str, Any]:
        return {'nom_famille': self.nom_famille, 'prenom': self.prenom, 'date_naissance': self.date_naissance,
                'sexe': self.sexe, 'classement': self.classement}

    @classmethod
    def from_dict(cls, data: Dict[str, Any], id: Optional[int] = None) -> 'Joueur':
        return cls(data['nom_famille'], data['prenom'], data['date_naissance'], data['sexe'],
                   data['classement'], id)

    def save(self) -> int:
        self.id = joueurs_table.insert(self.to_dict()) if self.id is None else (
            joueurs_table.update(self.to_dict(), doc_ids=[self.id]), self.id)[1]
        return self.id

    @classmethod
    def get_all(cls) -> List['Joueur']:
        return [cls.from_dict(item, id=item.doc_id) for item in joueurs_table.all()]

    def __str__(self):
        return f"{self.prenom} {self.nom_famille} (Classement: {self.classement})"


class Match:
    def __init__(self, joueur1: 'Joueur', joueur2: 'Joueur'):
        self.joueur1, self.joueur2, self.resultat = joueur1, joueur2, None

    def __str__(self):
        score = f"{self.resultat[0]}-{self.resultat[1]}" if self.resultat else "vs"
        return f"{self.joueur1.prenom} {self.joueur1.nom_famille} {score} " \
               f"{self.joueur2.prenom} {self.joueur2.nom_famille}"


class Tour:
    def __init__(self, nom: str):
        self.nom, self.debut, self.fin, self.matches = nom, datetime.now(), None, []

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
        if controle_temps.lower() not in self.CONTROLES_TEMPS:
            raise ValueError(f"Le contrôle du temps doit être parmi : {', '.join(self.CONTROLES_TEMPS)}")
        self.nom, self.lieu = nom, lieu
        self.date_debut, self.date_fin, self.nb_tours = date_debut, date_fin, nb_tours
        self.controle_temps, self.description, self.id = controle_temps.lower(), description, id
        self.tours, self.joueurs = [], []

    def to_dict(self) -> Dict[str, Any]:
        return {
            'nom': self.nom, 'lieu': self.lieu, 'date_debut': self.date_debut, 'date_fin': self.date_fin,
            'nb_tours': self.nb_tours, 'controle_temps': self.controle_temps, 'description': self.description,
            'joueurs': self.joueurs,
            'tours': [{'nom': t.nom, 'debut': t.debut.isoformat() if t.debut else None,
                       'fin': t.fin.isoformat() if t.fin else None,
                       'matches': [{'joueur1_id': m.joueur1.id, 'joueur2_id': m.joueur2.id,
                                    'resultat': m.resultat} for m in t.matches]} for t in self.tours]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], id: Optional[int] = None) -> 'Tournoi':
        tournoi = cls(data['nom'], data['lieu'], data['date_debut'], data['date_fin'], data['nb_tours'],
                      data['controle_temps'], data['description'], id)
        tournoi.joueurs = data['joueurs']
        joueurs_dict = {j.doc_id: j for j in joueurs_table.all()}
        for tour_data in data.get('tours', []):
            tour = Tour(tour_data['nom'])
            tour.debut = datetime.fromisoformat(tour_data['debut']) if tour_data['debut'] else None
            tour.fin = datetime.fromisoformat(tour_data['fin']) if tour_data['fin'] else None
            for match_data in tour_data['matches']:
                j1 = Joueur.from_dict(joueurs_dict[match_data['joueur1_id']], match_data['joueur1_id'])
                j2 = Joueur.from_dict(joueurs_dict[match_data['joueur2_id']], match_data['joueur2_id'])
                match = Match(j1, j2)
                match.resultat = match_data['resultat']
                tour.matches.append(match)
            tournoi.tours.append(tour)
        return tournoi

    def save(self) -> int:
        self.id = tournois_table.insert(self.to_dict()) if self.id is None else (
            tournois_table.update(self.to_dict(), doc_ids=[self.id]), self.id)[1]
        return self.id

    @classmethod
    def get_all(cls) -> List['Tournoi']:
        return [cls.from_dict(item, id=item.doc_id) for item in tournois_table.all()]

    def get_joueurs_objets(self) -> List[Joueur]:
        return [Joueur.from_dict(joueurs_table.get(doc_id=jid), id=jid) for jid in self.joueurs
                if joueurs_table.get(doc_id=jid)]

    def liste_joueurs_alphabetique(self) -> List[Joueur]:
        return sorted(self.get_joueurs_objets(), key=lambda j: (j.nom_famille.lower(), j.prenom.lower()))

    def liste_joueurs_classement(self) -> List[Joueur]:
        return sorted(self.get_joueurs_objets(), key=lambda j: j.classement, reverse=True)

    def liste_tours(self) -> List[Tour]:
        return self.tours

    def liste_matches(self) -> List[Match]:
        return [match for tour in self.tours for match in tour.matches]

    def __str__(self):
        return f"Tournoi {self.nom} à {self.lieu} ({self.date_debut} - {self.date_fin})"

    def ajouter_joueur(self, joueur: Joueur):
        if len(self.joueurs) < 8 and joueur.id not in self.joueurs:
            self.joueurs.append(joueur.id)
            self.save()
            print(f"✅ Joueur ajouté au tournoi : {joueur}")
        elif len(self.joueurs) >= 8:
            print("⚠️ Maximum de 8 joueurs atteint.")

    def generer_paires(self) -> List[tuple]:
        joueurs = sorted(self.get_joueurs_objets(), key=lambda j: j.points, reverse=True)
        random.shuffle(joueurs)
        return [(joueurs[i], joueurs[i + 1]) for i in range(0, len(joueurs), 2)]

    def jouer_tour(self):
        tour_num = len(self.tours) + 1
        print(f"\n=== Tour {tour_num} ===")
        tour = Tour(f"Tour {tour_num}")
        for j1, j2 in self.generer_paires():
            print(f"\nPartie : {j1.prenom} {j1.nom_famille} vs {j2.prenom} {j2.nom_famille}")
            print("Résultat : 1 = victoire du 1er | 2 = victoire du 2e | 0 = nul")
            res, match = input("→ Entrez le résultat : "), Match(j1, j2)
            if res == "1":
                j1.points, match.resultat = j1.points + 1, (1, 0)
            elif res == "2":
                j2.points, match.resultat = j2.points + 1, (0, 1)
            else:
                j1.points, j2.points, match.resultat = j1.points + 0.5, j2.points + 0.5, (0.5, 0.5)
                if res != "0":
                    print("Résultat invalide, partie comptée nulle.")
            tour.ajouter_match(match)
        tour.terminer_tour()
        self.tours.append(tour)
        self.save()
        self.afficher_classement()

    def afficher_classement(self):
        print("\n🏁 Classement actuel :")
        for i, j in enumerate(sorted(self.get_joueurs_objets(), key=lambda j: j.points, reverse=True), 1):
            print(f"{i}. {j.prenom} {j.nom_famille} - {j.points} pts")

    def tournoi_termine(self):
        print("\n🎉 Tournoi terminé ! Classement final :")
        self.afficher_classement()
        self.save()


class GestionnaireTournois:
    def __init__(self):
        self.tournois, self.joueurs = Tournoi.get_all(), Joueur.get_all()

    def ajouter_joueur(self, joueur: Joueur):
        joueur.save()
        self.joueurs.append(joueur)

    def ajouter_tournoi(self, tournoi: Tournoi):
        tournoi.save()
        self.tournois.append(tournoi)

    def liste_joueurs_alphabetique(self) -> List[Joueur]:
        return sorted(self.joueurs, key=lambda j: (j.nom_famille.lower(), j.prenom.lower()))

    def liste_joueurs_classement(self) -> List[Joueur]:
        return sorted(self.joueurs, key=lambda j: j.classement, reverse=True)


def menu_rapports(gestionnaire: GestionnaireTournois):
    while True:
        print("\n=== MENU RAPPORTS ===\n1. Liste des joueurs par ordre alphabétique")
        print("2. Liste des joueurs par classement\n3. Liste de tous les tournois")
        print("4. Détails d'un tournoi spécifique\n5. Retour au menu principal")
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
            for tournoi in gestionnaire.tournois:
                print(f"- {tournoi}")
        elif choix == "4":
            if not gestionnaire.tournois:
                print("Aucun tournoi disponible.")
                continue
            print("\nTournois disponibles:")
            for i, t in enumerate(gestionnaire.tournois, 1):
                print(f"{i}. {t.nom}")
            try:
                tournoi = gestionnaire.tournois[int(input("Numéro du tournoi : ")) - 1]
                print(f"\nDétails du tournoi {tournoi.nom}:\n\nJoueurs par ordre alphabétique:")
                for j in tournoi.liste_joueurs_alphabetique():
                    print(f"- {j}")
                print("\nJoueurs par classement:")
                for j in tournoi.liste_joueurs_classement():
                    print(f"- {j}")
                print("\nTours:")
                for tour in tournoi.liste_tours():
                    print(f"\n{tour}")
                    for match in tour.matches:
                        print(f"  - {match}")
            except (ValueError, IndexError):
                print("Choix invalide.")
        elif choix == "5":
            break


def main():
    print("♟️  Bienvenue dans le gestionnaire de tournoi d'échecs ♟️")
    gestionnaire = GestionnaireTournois()
    while True:
        print("\n=== MENU PRINCIPAL ===\n1. Créer un nouveau tournoi\n2. Ajouter un joueur")
        print("3. Afficher les rapports\n4. Quitter")
        choix = input("Choix : ")
        if choix == "1":
            tournoi = Tournoi(input("Nom du tournoi : "), input("Lieu du tournoi : "),
                              input("Date de début (YYYY-MM-DD) : "), input("Date de fin (YYYY-MM-DD) : "),
                              controle_temps=input("Contrôle du temps (bullet/blitz/rapide) : "),
                              description=input("Description du tournoi : "))
            gestionnaire.ajouter_tournoi(tournoi)
            print("\nAjoutez jusqu'à 8 joueurs :")
            while len(tournoi.joueurs) < 8:
                print(f"\nJoueur {len(tournoi.joueurs) + 1} : (ou tapez 'stop' pour terminer)")
                nom_famille = input("Nom de famille : ")
                if nom_famille.lower() == "stop":
                    break
                joueur = Joueur(nom_famille, input("Prénom : "), input("Date de naissance (YYYY-MM-DD) : "),
                                input("Sexe (M/F) : "), int(input("Classement : ")))
                tournoi.ajouter_joueur(joueur)
                gestionnaire.ajouter_joueur(joueur)
                print(f"✅ Joueur ajouté : {joueur}")
            for _ in range(tournoi.nb_tours):
                tournoi.jouer_tour()
            tournoi.tournoi_termine()
        elif choix == "2":
            print("\nAjout d'un nouveau joueur:")
            joueur = Joueur(input("Nom de famille : "), input("Prénom : "),
                            input("Date de naissance (YYYY-MM-DD) : "), input("Sexe (M/F) : "),
                            int(input("Classement : ")))
            gestionnaire.ajouter_joueur(joueur)
            print(f"✅ Joueur ajouté : {joueur}")
        elif choix == "3":
            menu_rapports(gestionnaire)
        elif choix == "4":
            print("Au revoir!")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()