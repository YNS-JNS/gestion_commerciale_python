# main_app.py
from business_logic import GestionCommercialeApp # Importer la classe principale

# --- Fonctions de Menu (restent ici pour la clarté de l'interface utilisateur) ---
def menu_produits(app_instance):
    while True:
        print("\n--- Menu Produits ---")
        print("1. Ajouter un produit")
        print("2. Afficher les produits")
        print("3. Rechercher un produit")
        print("4. Modifier un produit")
        print("5. Supprimer un produit")
        print("0. Retour")
        choix = input("Choix produits : ")
        if choix == '1': app_instance.ajouter_produit()
        elif choix == '2': app_instance.afficher_produits()
        elif choix == '3': app_instance.rechercher_produit()
        elif choix == '4': app_instance.modifier_produit_menu()
        elif choix == '5': app_instance.supprimer_produit()
        elif choix == '0': break
        else: print("Choix invalide.")

def menu_clients(app_instance):
    while True:
        print("\n--- Menu Clients ---")
        print("1. Ajouter un client")
        print("2. Afficher les clients")
        print("3. Supprimer un client")
        # TODO: Ajouter "Modifier un client", "Rechercher un client"
        print("0. Retour")
        choix = input("Choix clients : ")
        if choix == '1': app_instance.ajouter_client()
        elif choix == '2': app_instance.afficher_clients()
        elif choix == '3': app_instance.supprimer_client()
        elif choix == '0': break
        else: print("Choix invalide.")
        
def menu_commandes(app_instance):
    while True:
        print("\n--- Menu Commandes ---")
        print("1. Créer une commande")
        print("2. Ajouter un produit à une commande")
        print("3. Afficher toutes les commandes")
        print("4. Valider une commande")
        print("5. Annuler une commande")
        print("6. Générer un reçu de commande")
        # TODO: Ajouter "Modifier une commande", "Supprimer une commande"
        print("0. Retour")
        choix = input("Choix commandes : ")
        if choix == '1': app_instance.creer_commande()
        elif choix == '2': app_instance.ajouter_produit_commande()
        elif choix == '3': app_instance.afficher_commandes()
        elif choix == '4': app_instance.valider_commande()
        elif choix == '5': app_instance.annuler_commande()
        elif choix == '6': app_instance.generer_recu_commande()
        elif choix == '0': break
        else: print("Choix invalide.")

# --- Point d'entrée de l'application ---
def run_application():
    app = GestionCommercialeApp() # Crée une instance de notre logique principale
    
    while True:
        print("\n--- Menu Principal (Junior Modifié) ---")
        print("1. Gestion des Produits")
        print("2. Gestion des Clients")
        print("3. Gestion des Commandes")
        print("4. Sauvegarder les données")
        print("0. Quitter")

        choix_principal = input("Votre choix : ")

        if choix_principal == '1':
            menu_produits(app)
        elif choix_principal == '2':
            menu_clients(app)
        elif choix_principal == '3':
            menu_commandes(app)
        elif choix_principal == '4':
            app.sauvegarder_tout()
        elif choix_principal == '0':
            app.sauvegarder_tout() # Sauvegarde avant de quitter
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    run_application()