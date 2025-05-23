# gestion_app.py

import json
import os
import datetime
import uuid # Pour des IDs uniques plus facilement

# --- Configuration ---
DATA_DIR = "data"
PRODUITS_FILE = os.path.join(DATA_DIR, "produits.json")
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
COMMANDES_FILE = os.path.join(DATA_DIR, "commandes.json")
RECUS_DIR = os.path.join(DATA_DIR, "recus")

# S'assurer que les dossiers existent
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RECUS_DIR, exist_ok=True)


# --- Fonctions Utilitaires pour la Persistance ---

def charger_donnees(fichier_path):
    """Charge les données depuis un fichier JSON."""
    try:
        with open(fichier_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Si le fichier n'existe pas, retourne une liste vide
    except json.JSONDecodeError:
        print(f"Erreur: Le fichier {fichier_path} est corrompu ou mal formaté.")
        return [] # Retourne une liste vide en cas d'erreur de décodage

def sauvegarder_donnees(fichier_path, donnees):
    """Sauvegarde les données dans un fichier JSON."""
    try:
        with open(fichier_path, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
    except IOError:
        print(f"Erreur: Impossible d'écrire dans le fichier {fichier_path}.")


# --- Classes Métier ---

class Produit:
    def __init__(self, reference, nom, prix_unitaire, stock):
        self.reference = reference # Doit être unique
        self.nom = nom
        # On s'assure que le prix est un nombre positif
        try:
            self.prix_unitaire = float(prix_unitaire)
            if self.prix_unitaire <= 0:
                raise ValueError("Le prix doit être positif.")
        except ValueError:
            raise ValueError("Le prix doit être un nombre valide.")
        # On s'assure que le stock est un entier non-négatif
        try:
            self.stock = int(stock)
            if self.stock < 0:
                raise ValueError("Le stock ne peut pas être négatif.")
        except ValueError:
            raise ValueError("Le stock doit être un nombre entier.")

    def afficher_details(self):
        return f"Réf: {self.reference}, Nom: {self.nom}, Prix: {self.prix_unitaire:.2f}€, Stock: {self.stock}"

    def modifier_produit(self, nom=None, prix_unitaire=None):
        if nom:
            self.nom = nom
        if prix_unitaire is not None:
            try:
                nouveau_prix = float(prix_unitaire)
                if nouveau_prix <= 0:
                    print("Erreur: Le nouveau prix doit être positif.")
                else:
                    self.prix_unitaire = nouveau_prix
            except ValueError:
                print("Erreur: Le nouveau prix est invalide.")
                
    def mettre_a_jour_stock(self, quantite_ajoutee):
        try:
            ajout = int(quantite_ajoutee)
            if self.stock + ajout < 0:
                print(f"Erreur: Stock insuffisant. Stock actuel: {self.stock}, Tentative de retrait: {-ajout}")
            else:
                self.stock += ajout
        except ValueError:
            print("Erreur: La quantité pour la mise à jour du stock doit être un nombre entier.")
            
    def to_dict(self):
        """Convertit l'objet Produit en dictionnaire pour la sauvegarde JSON."""
        return {
            "reference": self.reference,
            "nom": self.nom,
            "prix_unitaire": self.prix_unitaire,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data):
        """Crée un objet Produit à partir d'un dictionnaire."""
        return cls(data['reference'], data['nom'], data['prix_unitaire'], data['stock'])


class Client:
    def __init__(self, id_client, nom, prenom, adresse, telephone=None, email=None):
        self.id_client = id_client # Doit être unique
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.telephone = telephone
        self.email = email # Simple validation de format à la saisie si besoin

    def afficher_details(self):
        return (f"ID: {self.id_client}, Nom: {self.prenom} {self.nom}\n"
                f"  Adresse: {self.adresse}\n"
                f"  Tel: {self.telephone or 'N/A'}\n"
                f"  Email: {self.email or 'N/A'}")

    def modifier_client(self, nom=None, prenom=None, adresse=None, telephone=None, email=None):
        if nom: self.nom = nom
        if prenom: self.prenom = prenom
        if adresse is not None : self.adresse = adresse # Permet de mettre une adresse vide
        # Pour tel/email, si la nouvelle valeur est explicitement None, on efface.
        # Si la nouvelle valeur est une chaîne vide, on peut choisir de l'ignorer ou de l'effacer.
        # Ici, on met à jour si une valeur est fournie (même vide), ou si c'est None pour effacer.
        if telephone is not None: self.telephone = telephone
        if email is not None: self.email = email
            
    def to_dict(self):
        return {
            "id_client": self.id_client,
            "nom": self.nom,
            "prenom": self.prenom,
            "adresse": self.adresse,
            "telephone": self.telephone,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['id_client'], data['nom'], data['prenom'], data['adresse'],
                   data.get('telephone'), data.get('email'))


class Commande:
    def __init__(self, numero_commande, date_creation, id_client, produits_commandes=None, total=0.0, statut="En Cours"):
        self.numero_commande = numero_commande # Doit être unique
        self.date_creation = date_creation
        self.id_client = id_client # Référence à un client
        self.produits_commandes = produits_commandes if produits_commandes is not None else [] # Liste de dicts: {'ref_produit': str, 'quantite': int, 'prix_vente': float}
        self.total = float(total)
        self.statut = statut # Ex: "En Cours", "Validée", "Annulée"

    def ajouter_produit(self, ref_produit, quantite, prix_vente):
        if self.statut != "En Cours":
            print("Erreur: Impossible d'ajouter un produit. La commande n'est pas 'En Cours'.")
            return False
        
        # Vérifier si produit déjà présent pour mettre à jour quantité
        for item in self.produits_commandes:
            if item['ref_produit'] == ref_produit:
                item['quantite'] += quantite
                self.calculer_total()
                return True # Produit mis à jour

        self.produits_commandes.append({
            "ref_produit": ref_produit,
            "quantite": quantite,
            "prix_vente": float(prix_vente)
        })
        self.calculer_total()
        return True # Produit ajouté

    def calculer_total(self):
        self.total = 0.0
        for item in self.produits_commandes:
            self.total += item['prix_vente'] * item['quantite']

    def afficher_commande(self, app_data): # app_data contient les listes produits/clients
        client = next((c for c in app_data['clients'] if c.id_client == self.id_client), None)
        client_nom = f"{client.prenom} {client.nom}" if client else "Client Inconnu"
        
        details = (f"Commande N°: {self.numero_commande} ({self.statut})\n"
                   f"Date: {self.date_creation}\n"
                   f"Client: {client_nom} (ID: {self.id_client})\n"
                   f"Produits:\n")
        if not self.produits_commandes:
            details += "  Aucun produit.\n"
        else:
            for item in self.produits_commandes:
                produit = next((p for p in app_data['produits'] if p.reference == item['ref_produit']), None)
                nom_produit = produit.nom if produit else "Produit Inconnu"
                details += (f"  - {nom_produit} (Réf: {item['ref_produit']}) "
                            f"x {item['quantite']} @ {item['prix_vente']:.2f}€\n")
        details += f"Total: {self.total:.2f}€\n"
        return details
        
    def to_dict(self):
        return {
            "numero_commande": self.numero_commande,
            "date_creation": self.date_creation, # Sauvegarde en string simple
            "id_client": self.id_client,
            "produits_commandes": self.produits_commandes,
            "total": self.total,
            "statut": self.statut
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['numero_commande'], data['date_creation'], data['id_client'],
                   data.get('produits_commandes', []), data.get('total', 0.0), data.get('statut', "En Cours"))


# --- Logique de l'Application (Gestionnaires Simplifiés) ---

class GestionCommercialeApp:
    def __init__(self):
        self.produits = [Produit.from_dict(p) for p in charger_donnees(PRODUITS_FILE)]
        self.clients = [Client.from_dict(c) for c in charger_donnees(CLIENTS_FILE)]
        self.commandes = [Commande.from_dict(cmd) for cmd in charger_donnees(COMMANDES_FILE)]

    def sauvegarder_tout(self):
        sauvegarder_donnees(PRODUITS_FILE, [p.to_dict() for p in self.produits])
        sauvegarder_donnees(CLIENTS_FILE, [c.to_dict() for c in self.clients])
        sauvegarder_donnees(COMMANDES_FILE, [cmd.to_dict() for cmd in self.commandes])
        print("Données sauvegardées.")

    # --- Gestion des Produits ---
    def ajouter_produit(self):
        print("\n--- Ajouter un Produit ---")
        # Générer une référence unique simple (pourrait être amélioré)
        # Pour un junior, un UUID est plus simple à gérer pour l'unicité
        reference = "PROD-" + str(uuid.uuid4())[:8].upper()
        nom = input("Nom du produit : ")
        while not nom:
            nom = input("Le nom ne peut pas être vide. Nom du produit : ")
        
        prix = -1
        while prix <= 0:
            try:
                prix = float(input("Prix unitaire : "))
                if prix <= 0: print("Le prix doit être positif.")
            except ValueError:
                print("Veuillez entrer un nombre valide pour le prix.")
                prix = -1 # Pour que la boucle continue
        
        stock = -1
        while stock < 0:
            try:
                stock = int(input("Stock initial : "))
                if stock < 0: print("Le stock ne peut pas être négatif.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide pour le stock.")
                stock = -1

        if any(p.reference == reference for p in self.produits): # Vérif unicité ref
             print(f"Erreur : Un produit avec la référence {reference} existe déjà.")
             return

        try:
            nouveau_produit = Produit(reference, nom, prix, stock)
            self.produits.append(nouveau_produit)
            print(f"Produit '{nom}' ajouté avec succès (Réf: {reference}).")
        except ValueError as e:
            print(f"Erreur lors de la création du produit: {e}")


    def afficher_produits(self):
        print("\n--- Liste des Produits ---")
        if not self.produits:
            print("Aucun produit disponible.")
            return
        for p in self.produits:
            print(p.afficher_details())

    def rechercher_produit(self):
        terme = input("Rechercher produit par nom ou référence : ").lower()
        trouves = [p for p in self.produits if terme in p.nom.lower() or terme == p.reference.lower()]
        if not trouves:
            print("Aucun produit trouvé.")
        else:
            for p in trouves:
                print(p.afficher_details())
    
    def modifier_produit_menu(self):
        ref = input("Référence du produit à modifier : ")
        produit = next((p for p in self.produits if p.reference == ref), None)
        if not produit:
            print("Produit non trouvé.")
            return

        print(f"Modification de : {produit.afficher_details()}")
        n_nom = input(f"Nouveau nom (actuel: {produit.nom}) [Entrée pour ignorer] : ") or None
        
        n_prix_str = input(f"Nouveau prix (actuel: {produit.prix_unitaire}) [Entrée pour ignorer] : ")
        n_prix = None
        if n_prix_str:
            try:
                n_prix = float(n_prix_str)
                if n_prix <= 0:
                    print("Le prix doit être positif. Modification du prix annulée.")
                    n_prix = None 
            except ValueError:
                print("Prix invalide. Modification du prix annulée.")
                n_prix = None
        
        produit.modifier_produit(nom=n_nom, prix_unitaire=n_prix)
        print("Produit modifié.")

    def supprimer_produit(self):
        ref = input("Référence du produit à supprimer : ")
        # Vérifier si le produit est dans une commande non annulée
        for cmd in self.commandes:
            if cmd.statut != "Annulée":
                for item_cmd in cmd.produits_commandes:
                    if item_cmd['ref_produit'] == ref:
                        print(f"Erreur: Impossible de supprimer. Produit {ref} est dans la commande {cmd.numero_commande}.")
                        return
        
        produit_index = -1
        for i, p in enumerate(self.produits):
            if p.reference == ref:
                produit_index = i
                break
        
        if produit_index != -1:
            del self.produits[produit_index]
            print(f"Produit {ref} supprimé.")
        else:
            print("Produit non trouvé.")

    # --- Gestion des Clients ---
    def ajouter_client(self):
        print("\n--- Ajouter un Client ---")
        id_client = "CLI-" + str(uuid.uuid4())[:8].upper()
        nom = input("Nom de famille : ")
        prenom = input("Prénom : ")
        adresse = input("Adresse : ")
        telephone = input("Téléphone (optionnel) : ")
        email = input("Email (optionnel) : ")
        # Des validations plus poussées (format email/tel) peuvent être ajoutées ici

        if any(c.id_client == id_client for c in self.clients):
            print(f"Erreur: Un client avec l'ID {id_client} existe déjà.")
            return

        nouveau_client = Client(id_client, nom, prenom, adresse, telephone, email)
        self.clients.append(nouveau_client)
        print(f"Client '{prenom} {nom}' ajouté (ID: {id_client}).")

    def afficher_clients(self):
        print("\n--- Liste des Clients ---")
        if not self.clients:
            print("Aucun client enregistré.")
            return
        for c in self.clients:
            print(c.afficher_details())
            print("-" * 20)

    def supprimer_client(self):
        id_cli = input("ID du client à supprimer : ")
        # Vérifier si le client a des commandes non annulées
        for cmd in self.commandes:
            if cmd.id_client == id_cli and cmd.statut != "Annulée":
                print(f"Erreur: Client {id_cli} a des commandes actives (ex: {cmd.numero_commande}). Suppression annulée.")
                return

        client_index = -1
        for i, c in enumerate(self.clients):
            if c.id_client == id_cli:
                client_index = i
                break
        
        if client_index != -1:
            del self.clients[client_index]
            print(f"Client {id_cli} supprimé.")
        else:
            print("Client non trouvé.")
            
    # --- Gestion des Commandes ---
    def creer_commande(self):
        print("\n--- Créer une Commande ---")
        id_client = input("ID du client pour la commande : ")
        client_existe = any(c.id_client == id_client for c in self.clients)
        if not client_existe:
            print("Client non trouvé. Veuillez d'abord ajouter le client.")
            return

        num_commande = "CMD-" + datetime.datetime.now().strftime("%Y%m%d") + "-" + str(uuid.uuid4())[:4].upper()
        date_creation = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        nouvelle_commande = Commande(num_commande, date_creation, id_client)
        self.commandes.append(nouvelle_commande)
        print(f"Commande {num_commande} créée. Ajoutez des produits.")

    def ajouter_produit_commande(self):
        num_cmd = input("Numéro de la commande (doit être 'En Cours') : ")
        commande = next((cmd for cmd in self.commandes if cmd.numero_commande == num_cmd and cmd.statut == "En Cours"), None)
        if not commande:
            print("Commande non trouvée ou n'est pas 'En Cours'.")
            return

        ref_prod = input("Référence du produit à ajouter : ")
        produit = next((p for p in self.produits if p.reference == ref_prod), None)
        if not produit:
            print("Produit non trouvé.")
            return

        quantite = 0
        while quantite <= 0:
            try:
                quantite = int(input(f"Quantité pour {produit.nom} (Stock: {produit.stock}) : "))
                if quantite <= 0: print("La quantité doit être positive.")
            except ValueError:
                print("Veuillez entrer un nombre entier.")
                quantite = 0 # Pour continuer la boucle
        
        if produit.stock < quantite:
            print("Stock insuffisant.")
            return

        if commande.ajouter_produit(ref_prod, quantite, produit.prix_unitaire):
             # Pas besoin de mettre à jour stock ici, seulement à la validation
            print(f"{quantite} x {produit.nom} ajouté(s) à la commande {num_cmd}.")
        else:
            print(f"Échec de l'ajout du produit à la commande {num_cmd}.")


    def afficher_commandes(self):
        print("\n--- Liste des Commandes ---")
        if not self.commandes:
            print("Aucune commande enregistrée.")
            return
        app_data_for_display = {'produits': self.produits, 'clients': self.clients}
        for cmd in self.commandes:
            print(cmd.afficher_commande(app_data_for_display))
            print("-" * 20)

    def valider_commande(self):
        num_cmd = input("Numéro de la commande à valider : ")
        commande = next((cmd for cmd in self.commandes if cmd.numero_commande == num_cmd), None)
        if not commande:
            print("Commande non trouvée.")
            return
        if commande.statut != "En Cours":
            print(f"La commande est déjà '{commande.statut}'.")
            return
        if not commande.produits_commandes:
            print("Impossible de valider une commande vide.")
            return

        # Vérification du stock et décrémentation
        stocks_ok = True
        produits_a_maj_stock = [] # Pour rollback si un produit manque
        for item_cmd in commande.produits_commandes:
            produit = next((p for p in self.produits if p.reference == item_cmd['ref_produit']), None)
            if not produit:
                print(f"Erreur: Produit {item_cmd['ref_produit']} de la commande n'existe plus.")
                stocks_ok = False
                break
            if produit.stock < item_cmd['quantite']:
                print(f"Stock insuffisant pour {produit.nom} (demandé: {item_cmd['quantite']}, dispo: {produit.stock}).")
                stocks_ok = False
                break
            produits_a_maj_stock.append({'produit_obj': produit, 'quantite_a_retirer': item_cmd['quantite']})

        if stocks_ok:
            for maj in produits_a_maj_stock:
                maj['produit_obj'].mettre_a_jour_stock(-maj['quantite_a_retirer']) # Retirer du stock
            commande.statut = "Validée"
            print(f"Commande {num_cmd} validée. Stocks mis à jour.")
        else:
            print(f"Validation de la commande {num_cmd} annulée en raison de problèmes de stock ou de produit.")

    def annuler_commande(self):
        num_cmd = input("Numéro de la commande à annuler : ")
        commande = next((cmd for cmd in self.commandes if cmd.numero_commande == num_cmd), None)
        if not commande:
            print("Commande non trouvée.")
            return
        
        statut_precedent = commande.statut
        commande.statut = "Annulée"

        # Si la commande était validée, restaurer le stock
        if statut_precedent == "Validée":
            for item_cmd in commande.produits_commandes:
                produit = next((p for p in self.produits if p.reference == item_cmd['ref_produit']), None)
                if produit:
                    produit.mettre_a_jour_stock(item_cmd['quantite']) # Rajouter au stock
            print(f"Commande {num_cmd} annulée. Stocks restaurés.")
        else:
            print(f"Commande {num_cmd} annulée.")
            
    def generer_recu_commande(self):
        num_cmd = input("Numéro de la commande pour le reçu : ")
        commande = next((cmd for cmd in self.commandes if cmd.numero_commande == num_cmd), None)
        if not commande:
            print("Commande non trouvée.")
            return

        client = next((c for c in self.clients if c.id_client == commande.id_client), None)
        client_nom = f"{client.prenom} {client.nom}" if client else "Client Inconnu"
        
        contenu_recu = f"--- REÇU COMMANDE ---\n"
        contenu_recu += f"Numéro: {commande.numero_commande}\n"
        contenu_recu += f"Date: {commande.date_creation}\n"
        contenu_recu += f"Client: {client_nom} (ID: {commande.id_client})\n"
        contenu_recu += f"Statut: {commande.statut}\n"
        contenu_recu += "Produits:\n"
        for item in commande.produits_commandes:
            produit = next((p for p in self.produits if p.reference == item['ref_produit']), None)
            nom_produit = produit.nom if produit else "Produit Inconnu"
            contenu_recu += f"  - {nom_produit} x {item['quantite']} @ {item['prix_vente']:.2f}€\n"
        contenu_recu += f"TOTAL: {commande.total:.2f}€\n"
        contenu_recu += "-----------------------\n"
        
        nom_fichier_recu = os.path.join(RECUS_DIR, f"recu_{commande.numero_commande.replace('-', '_')}.txt")
        try:
            with open(nom_fichier_recu, 'w', encoding='utf-8') as f:
                f.write(contenu_recu)
            print(f"Reçu généré et sauvegardé : {nom_fichier_recu}")
        except IOError:
            print(f"Erreur lors de la sauvegarde du reçu pour la commande {num_cmd}.")


    # --- Menu Principal ---
    def run(self):
        while True:
            print("\n--- Menu Principal (Version Junior) ---")
            print("1. Gestion des Produits")
            print("2. Gestion des Clients")
            print("3. Gestion des Commandes")
            print("4. Sauvegarder les données")
            print("0. Quitter")

            choix_principal = input("Votre choix : ")

            if choix_principal == '1':
                self.menu_produits()
            elif choix_principal == '2':
                self.menu_clients()
            elif choix_principal == '3':
                self.menu_commandes()
            elif choix_principal == '4':
                self.sauvegarder_tout()
            elif choix_principal == '0':
                self.sauvegarder_tout() # Sauvegarde avant de quitter
                print("Au revoir !")
                break
            else:
                print("Choix invalide.")

    def menu_produits(self):
        while True:
            print("\n--- Menu Produits ---")
            print("1. Ajouter un produit")
            print("2. Afficher les produits")
            print("3. Rechercher un produit")
            print("4. Modifier un produit")
            print("5. Supprimer un produit")
            print("0. Retour")
            choix = input("Choix produits : ")
            if choix == '1': self.ajouter_produit()
            elif choix == '2': self.afficher_produits()
            elif choix == '3': self.rechercher_produit()
            elif choix == '4': self.modifier_produit_menu()
            elif choix == '5': self.supprimer_produit()
            elif choix == '0': break
            else: print("Choix invalide.")

    def menu_clients(self):
        while True:
            print("\n--- Menu Clients ---")
            print("1. Ajouter un client")
            print("2. Afficher les clients")
            # Ajouter "Modifier un client", "Rechercher un client" comme exercice
            print("3. Supprimer un client")
            print("0. Retour")
            choix = input("Choix clients : ")
            if choix == '1': self.ajouter_client()
            elif choix == '2': self.afficher_clients()
            elif choix == '3': self.supprimer_client()
            elif choix == '0': break
            else: print("Choix invalide.")
            
    def menu_commandes(self):
        while True:
            print("\n--- Menu Commandes ---")
            print("1. Créer une commande")
            print("2. Ajouter un produit à une commande")
            print("3. Afficher toutes les commandes")
            print("4. Valider une commande")
            print("5. Annuler une commande")
            print("6. Générer un reçu de commande")
            # Ajouter "Modifier une commande", "Supprimer une commande" comme exercice
            print("0. Retour")
            choix = input("Choix commandes : ")
            if choix == '1': self.creer_commande()
            elif choix == '2': self.ajouter_produit_commande()
            elif choix == '3': self.afficher_commandes()
            elif choix == '4': self.valider_commande()
            elif choix == '5': self.annuler_commande()
            elif choix == '6': self.generer_recu_commande()
            elif choix == '0': break
            else: print("Choix invalide.")

# --- Point d'entrée de l'application ---
if __name__ == "__main__":
    app = GestionCommercialeApp()
    app.run()