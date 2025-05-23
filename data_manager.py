# data_manager.py
import json
import os

# --- Configuration des chemins (peut être importé depuis un fichier config si besoin) ---
DATA_DIR = "data"
PRODUITS_FILE = os.path.join(DATA_DIR, "produits.json")
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
COMMANDES_FILE = os.path.join(DATA_DIR, "commandes.json")
RECUS_DIR = os.path.join(DATA_DIR, "recus")

def initialiser_dossiers():
    """S'assure que les dossiers de données existent."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RECUS_DIR, exist_ok=True)

def charger_donnees_json(fichier_path):
    """Charge les données depuis un fichier JSON."""
    initialiser_dossiers() # S'assurer que le dossier data existe avant de lire
    try:
        with open(fichier_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Erreur: Le fichier {fichier_path} est corrompu. Retourne une liste vide.")
        return []

def sauvegarder_donnees_json(fichier_path, donnees):
    """Sauvegarde les données dans un fichier JSON."""
    initialiser_dossiers() # S'assurer que le dossier data existe avant d'écrire
    try:
        with open(fichier_path, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
    except IOError:
        print(f"Erreur: Impossible d'écrire dans le fichier {fichier_path}.")

def sauvegarder_recu_txt(nom_fichier, contenu):
    initialiser_dossiers()
    chemin_complet = os.path.join(RECUS_DIR, nom_fichier)
    try:
        with open(chemin_complet, 'w', encoding='utf-8') as f:
            f.write(contenu)
        print(f"Reçu sauvegardé : {chemin_complet}")
    except IOError:
        print(f"Erreur lors de la sauvegarde du fichier : {chemin_complet}")