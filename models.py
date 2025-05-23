# models.py
import uuid
import datetime

class Produit:
    def __init__(self, reference, nom, prix_unitaire, stock):
        self.reference = reference
        self.nom = nom
        try:
            self.prix_unitaire = float(prix_unitaire)
            if self.prix_unitaire <= 0:
                raise ValueError("Le prix doit être positif.")
        except ValueError:
            raise ValueError("Le prix doit être un nombre valide.")
        try:
            self.stock = int(stock)
            if self.stock < 0:
                raise ValueError("Le stock ne peut pas être négatif.")
        except ValueError:
            raise ValueError("Le stock doit être un nombre entier.")

    def afficher_details(self):
        return f"Réf: {self.reference}, Nom: {self.nom}, Prix: {self.prix_unitaire:.2f} MAD, Stock: {self.stock}"

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
                # On lève une exception pour que l'appelant puisse la gérer
                raise ValueError(f"Stock insuffisant. Stock actuel: {self.stock}, Tentative de retrait: {-ajout}")
            else:
                self.stock += ajout
        except ValueError as e:
            # Propage l'erreur si c'est déjà une ValueError (de l'insuffisance de stock)
            # ou convertit une erreur de type en ValueError
            if "Stock insuffisant" in str(e):
                raise e
            raise ValueError("La quantité pour la mise à jour du stock doit être un nombre entier.")
            
    def to_dict(self):
        return {
            "reference": self.reference,
            "nom": self.nom,
            "prix_unitaire": self.prix_unitaire,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['reference'], data['nom'], data['prix_unitaire'], data['stock'])


class Client:
    def __init__(self, id_client, nom, prenom, adresse, telephone=None, email=None):
        self.id_client = id_client
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.telephone = telephone
        self.email = email

    def afficher_details(self):
        return (f"ID: {self.id_client}, Nom: {self.prenom} {self.nom}\n"
                f"  Adresse: {self.adresse}\n"
                f"  Tel: {self.telephone or 'N/A'}\n"
                f"  Email: {self.email or 'N/A'}")

    def modifier_client(self, nom=None, prenom=None, adresse=None, telephone=None, email=None):
        if nom: self.nom = nom
        if prenom: self.prenom = prenom
        if adresse is not None: self.adresse = adresse
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
        self.numero_commande = numero_commande
        self.date_creation = date_creation
        self.id_client = id_client
        self.produits_commandes = produits_commandes if produits_commandes is not None else []
        self.total = float(total)
        self.statut = statut

    def ajouter_produit(self, ref_produit, quantite, prix_vente):
        if self.statut != "En Cours":
            print("Erreur: Impossible d'ajouter un produit. La commande n'est pas 'En Cours'.")
            return False
        
        for item in self.produits_commandes:
            if item['ref_produit'] == ref_produit:
                item['quantite'] += quantite
                self.calculer_total()
                return True

        self.produits_commandes.append({
            "ref_produit": ref_produit,
            "quantite": quantite,
            "prix_vente": float(prix_vente)
        })
        self.calculer_total()
        return True

    def calculer_total(self):
        self.total = 0.0
        for item in self.produits_commandes:
            self.total += item['prix_vente'] * item['quantite']

    def afficher_commande(self, clients_data, produits_data): # Passe les listes de clients et produits
        client = next((c for c in clients_data if c.id_client == self.id_client), None)
        client_nom = f"{client.prenom} {client.nom}" if client else "Client Inconnu"
        
        details = (f"Commande N°: {self.numero_commande} ({self.statut})\n"
                   f"Date: {self.date_creation}\n"
                   f"Client: {client_nom} (ID: {self.id_client})\n"
                   f"Produits:\n")
        if not self.produits_commandes:
            details += "  Aucun produit.\n"
        else:
            for item in self.produits_commandes:
                produit = next((p for p in produits_data if p.reference == item['ref_produit']), None)
                nom_produit = produit.nom if produit else "Produit Inconnu"
                details += (f"  - {nom_produit} (Réf: {item['ref_produit']}) "
                            f"x {item['quantite']} @ {item['prix_vente']:.2f} MAD\n")
        details += f"Total: {self.total:.2f} MAD\n"
        return details
        
    def to_dict(self):
        return {
            "numero_commande": self.numero_commande,
            "date_creation": self.date_creation,
            "id_client": self.id_client,
            "produits_commandes": self.produits_commandes,
            "total": self.total,
            "statut": self.statut
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['numero_commande'], data['date_creation'], data['id_client'],
                   data.get('produits_commandes', []), data.get('total', 0.0), data.get('statut', "En Cours"))