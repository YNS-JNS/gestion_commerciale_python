# business_logic.py
import uuid
import datetime
from models import Produit, Client, Commande # Importer les classes du fichier models.py
import data_manager # Importer les fonctions de data_manager.py

class GestionCommercialeApp:
    def __init__(self):
        # Charger les données en utilisant les fonctions de data_manager
        # et convertir les dictionnaires en objets de nos classes
        self.produits = [Produit.from_dict(p) for p in data_manager.charger_donnees_json(data_manager.PRODUITS_FILE)]
        self.clients = [Client.from_dict(c) for c in data_manager.charger_donnees_json(data_manager.CLIENTS_FILE)]
        self.commandes = [Commande.from_dict(cmd) for cmd in data_manager.charger_donnees_json(data_manager.COMMANDES_FILE)]

    def sauvegarder_tout(self):
        data_manager.sauvegarder_donnees_json(data_manager.PRODUITS_FILE, [p.to_dict() for p in self.produits])
        data_manager.sauvegarder_donnees_json(data_manager.CLIENTS_FILE, [c.to_dict() for c in self.clients])
        data_manager.sauvegarder_donnees_json(data_manager.COMMANDES_FILE, [cmd.to_dict() for cmd in self.commandes])
        print("Données sauvegardées.")

    # --- Gestion des Produits ---
    def ajouter_produit(self):
        print("\n--- Ajouter un Produit ---")
        reference = "PROD-" + str(uuid.uuid4())[:8].upper()
        nom = input("Nom du produit : ")
        while not nom:
            nom = input("Le nom ne peut pas être vide. Nom du produit : ")
        
        prix = -1.0
        while prix <= 0:
            try:
                prix_str = input("Prix unitaire (MAD) : ")
                prix = float(prix_str)
                if prix <= 0: print("Le prix doit être positif.")
            except ValueError:
                print("Veuillez entrer un nombre valide pour le prix.")
                prix = -1.0
        
        stock = -1
        while stock < 0:
            try:
                stock_str = input("Stock initial : ")
                stock = int(stock_str)
                if stock < 0: print("Le stock ne peut pas être négatif.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide pour le stock.")
                stock = -1

        if any(p.reference == reference for p in self.produits):
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
        
        n_prix_str = input(f"Nouveau prix (MAD) (actuel: {produit.prix_unitaire:.2f}) [Entrée pour ignorer] : ")
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
        for cmd in self.commandes:
            if cmd.statut != "Annulée":
                for item_cmd in cmd.produits_commandes:
                    if item_cmd['ref_produit'] == ref:
                        print(f"Erreur: Produit {ref} est dans la commande {cmd.numero_commande}. Suppression annulée.")
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
                quantite_str = input(f"Quantité pour {produit.nom} (Stock: {produit.stock}) : ")
                quantite = int(quantite_str)
                if quantite <= 0: print("La quantité doit être positive.")
            except ValueError:
                print("Veuillez entrer un nombre entier.")
                quantite = 0
        
        if produit.stock < quantite:
            print("Stock insuffisant.")
            return

        if commande.ajouter_produit(ref_prod, quantite, produit.prix_unitaire):
            print(f"{quantite} x {produit.nom} ajouté(s) à la commande {num_cmd}.")
        else:
            print(f"Échec de l'ajout du produit à la commande {num_cmd}.")

    def afficher_commandes(self):
        print("\n--- Liste des Commandes ---")
        if not self.commandes:
            print("Aucune commande enregistrée.")
            return
        for cmd in self.commandes:
            # Passer les listes de clients et produits actuelles pour l'affichage
            print(cmd.afficher_commande(self.clients, self.produits))
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

        stocks_ok = True
        produits_affectes_stock = [] # Garder une trace pour rollback si un item échoue

        for item_cmd in commande.produits_commandes:
            produit = next((p for p in self.produits if p.reference == item_cmd['ref_produit']), None)
            if not produit:
                print(f"Erreur: Produit {item_cmd['ref_produit']} de la commande n'existe plus.")
                stocks_ok = False
                break # Sortir de la boucle des items
            
            # Vérifier le stock avant de tenter la mise à jour
            if produit.stock < item_cmd['quantite']:
                print(f"Stock insuffisant pour {produit.nom} (demandé: {item_cmd['quantite']}, dispo: {produit.stock}).")
                stocks_ok = False
                break # Sortir de la boucle des items
            
            # Ajouter à la liste des produits dont le stock sera mis à jour
            produits_affectes_stock.append({'objet_produit': produit, 'quantite_retiree': item_cmd['quantite']})

        if stocks_ok:
            # Si tous les stocks sont OK, alors on procède aux mises à jour
            for maj_stock_info in produits_affectes_stock:
                try:
                    maj_stock_info['objet_produit'].mettre_a_jour_stock(-maj_stock_info['quantite_retiree'])
                except ValueError as e: # Au cas où la mise à jour du stock elle-même échoue (ne devrait pas si vérif avant)
                    print(f"Erreur interne lors de la mise à jour du stock pour {maj_stock_info['objet_produit'].nom}: {e}")
                    # Ici, il faudrait une logique de rollback pour les produits déjà mis à jour,
                    # ce qui est complexe pour une version junior. On s'arrête et on signale.
                    print("Arrêt de la validation. Certains stocks pourraient être incohérents.")
                    return # Quitter la fonction de validation

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

        if statut_precedent == "Validée":
            for item_cmd in commande.produits_commandes:
                produit = next((p for p in self.produits if p.reference == item_cmd['ref_produit']), None)
                if produit:
                    try:
                        produit.mettre_a_jour_stock(item_cmd['quantite']) # Rajouter au stock
                    except ValueError as e: # Si la restauration du stock échoue (ne devrait pas arriver)
                         print(f"Avertissement: Erreur lors de la restauration du stock pour {produit.nom}: {e}")
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
            contenu_recu += f"  - {nom_produit} x {item['quantite']} @ {item['prix_vente']:.2f} MAD\n"
        contenu_recu += f"TOTAL: {commande.total:.2f} MAD\n"
        contenu_recu += "-----------------------\n"
        
        nom_fichier = f"recu_{commande.numero_commande.replace('-', '_')}.txt"
        data_manager.sauvegarder_recu_txt(nom_fichier, contenu_recu)