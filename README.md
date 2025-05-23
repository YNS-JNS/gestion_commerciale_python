
# Système de Gestion Commerciale en Python

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repo-blue?logo=github&url=https://github.com/YNS-JNS/gestion_commerciale_python)](https://github.com/YNS-JNS/gestion_commerciale_python.git)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Vous pouvez choisir une autre licence si vous le souhaitez -->

Application en ligne de commande (CLI) pour la gestion simplifiée des produits, clients et commandes, avec persistance des données au format JSON. Ce projet est conçu à des fins éducatives pour illustrer les concepts de base de la programmation orientée objet et de la manipulation de fichiers en Python.

## Table des Matières

- [Système de Gestion Commerciale en Python](#système-de-gestion-commerciale-en-python)
  - [Table des Matières](#table-des-matières)
  - [Fonctionnalités](#fonctionnalités)
  - [Structure du Projet](#structure-du-projet)
  - [Prérequis](#prérequis)
  - [Installation](#installation)
  - [Utilisation](#utilisation)
  - [Détails Techniques](#détails-techniques)
    - [Modèles de Données (`models.py`)](#modèles-de-données-modelspy)
    - [Persistance des Données (`data_manager.py`)](#persistance-des-données-data_managerpy)
    - [Logique Métier (`business_logic.py`)](#logique-métier-business_logicpy)
  - [Pistes d'Amélioration](#pistes-damélioration)
  - [Auteur](#auteur)
  - [Licence](#licence)

## Fonctionnalités

*   **Gestion des Produits :**
    *   Ajouter, afficher, rechercher, modifier et supprimer des produits.
    *   Gestion du stock (incrémentation/décrémentation).
*   **Gestion des Clients :**
    *   Ajouter, afficher et supprimer des clients.
    *   (Modification et recherche de client à implémenter).
*   **Gestion des Commandes :**
    *   Créer des commandes associées à un client.
    *   Ajouter des produits à une commande existante (si "En Cours").
    *   Calculer automatiquement le total de la commande.
    *   Valider une commande (change le statut, décrémente le stock des produits).
    *   Annuler une commande (change le statut, restaure le stock si la commande était validée).
    *   Générer un reçu textuel simple pour une commande et l'enregistrer.
*   **Persistance des Données :**
    *   Sauvegarde et chargement automatique des données (produits, clients, commandes) dans des fichiers JSON.
    *   Les données sont sauvegardées à la fermeture de l'application ou manuellement.
*   **Interface Utilisateur :**
    *   Navigation simple via des menus en ligne de commande.
    *   Devise utilisée : MAD (Dirham Marocain).

## Structure du Projet

Le projet est organisé en plusieurs modules pour une meilleure lisibilité et maintenabilité :

```
gestion_commerciale_python/  (Nom du dépôt)
├── main_app.py             # Point d'entrée, gestion des menus CLI
├── models.py               # Définition des classes Produit, Client, Commande
├── data_manager.py         # Fonctions pour la lecture/écriture des fichiers de données
├── business_logic.py       # Classe principale avec la logique métier (GestionCommercialeApp)
├── data/                   # Répertoire des données persistantes (généré par l'application)
│   ├── produits.json
│   ├── clients.json
│   ├── commandes.json
│   └── recus/              # Répertoire pour les reçus de commandes
└── README.md               # Ce fichier
```
*(Note: Adaptez `gestion_commerciale_python/` au nom réel de votre dossier racine si différent du nom du dépôt).*

## Prérequis

*   Python 3.7 ou une version ultérieure.

Aucune bibliothèque externe n'est requise pour ce projet.

## Installation

1.  **Cloner le dépôt :**
    Ouvrez un terminal et exécutez la commande suivante :
    ```bash
    git clone https://github.com/YNS-JNS/gestion_commerciale_python.git
    cd gestion_commerciale_python 
    ```
    *(Adaptez `gestion_commerciale_python` au nom du dossier créé par `git clone` si vous avez renommé le dépôt localement).*

2.  **Créer le répertoire de données (optionnel) :**
    L'application créera le répertoire `data/` et `data/recus/` au premier lancement si ils n'existent pas. Vous pouvez aussi les créer manuellement dans le dossier du projet :
    ```bash
    mkdir data
    mkdir data/recus
    ```

## Utilisation

Pour lancer l'application, assurez-vous d'être dans le répertoire racine du projet (`gestion_commerciale_python/`) dans votre terminal, puis exécutez :

```bash
python main_app.py
```

Suivez les instructions affichées dans les menus pour interagir avec l'application.

*   Les données sont chargées au démarrage.
*   Les données sont sauvegardées lorsque vous quittez l'application ou via l'option de sauvegarde manuelle dans le menu principal.

## Détails Techniques

### Modèles de Données (`models.py`)

Le projet utilise trois classes principales pour représenter les entités métier :
*   **`Produit`**: `reference` (unique, généré), `nom`, `prix_unitaire` (MAD), `stock`.
*   **`Client`**: `id_client` (unique, généré), `nom`, `prenom`, `adresse`, `telephone`, `email`.
*   **`Commande`**: `numero_commande` (unique, généré), `date_creation`, `id_client` (référence), `produits_commandes` (liste de dictionnaires), `total` (MAD), `statut` ("En Cours", "Validée", "Annulée").

Chaque classe modèle inclut des méthodes `to_dict()` pour la sérialisation en JSON et `@classmethod from_dict()` pour la désérialisation.

### Persistance des Données (`data_manager.py`)

*   Les données sont stockées au format JSON dans le répertoire `data/`.
*   Trois fichiers principaux sont utilisés : `produits.json`, `clients.json`, `commandes.json`.
*   Les reçus de commande sont sauvegardés sous forme de fichiers texte (`.txt`) dans le sous-répertoire `data/recus/`.
*   Le module `data_manager.py` centralise toutes les opérations de lecture et d'écriture de fichiers.

### Logique Métier (`business_logic.py`)

La classe `GestionCommercialeApp` encapsule la logique principale de l'application :
*   Gestion des listes d'objets (produits, clients, commandes) en mémoire.
*   Implémentation des fonctionnalités de création, lecture, mise à jour, suppression (CRUD) pour chaque entité.
*   Logique de validation des commandes, incluant la vérification et la mise à jour des stocks.
*   Interaction avec le `data_manager` pour le chargement et la sauvegarde des données.

## Pistes d'Amélioration

Ce projet constitue une base qui peut être étendue de plusieurs manières :

*   **Validation des Entrées Plus Robuste :** Implémenter des expressions régulières pour la validation des emails, numéros de téléphone, etc.
*   **Gestion des Erreurs Améliorée :** Utiliser des exceptions personnalisées pour une meilleure gestion des cas d'erreur.
*   **Fonctionnalités Manquantes :** Compléter les options de modification/recherche pour les clients, et de modification/suppression pour les commandes.
*   **Tests Unitaires :** Ajouter des tests (par exemple avec `unittest` ou `pytest`) pour assurer la fiabilité du code.
*   **Logging :** Intégrer le module `logging` pour tracer les opérations et les erreurs.
*   **Interface Utilisateur :** Remplacer l'interface en ligne de commande par une interface graphique (Tkinter, PyQt) ou une interface web (Flask, Django).
*   **Base de Données :** Utiliser une base de données (SQLite, PostgreSQL) pour une gestion des données plus performante et transactionnelle.

## Auteur

*   **Abdeladim AIBOUS**
*   **Youness AIT M'BAREK**
    *   GitHub : [@YNS-JNS](https://github.com/yns-jns)
    *   Dépôt du projet : [gestion_commerciale_python](https://github.com/YNS-JNS/gestion_commerciale_python.git)

## Licence

Ce projet est distribué sous la licence MIT. Vous pouvez consulter le fichier `LICENSE` (si vous en ajoutez un) ou vous référer à [opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) pour plus de détails sur cette licence.
Si vous n'avez pas de fichier `LICENSE` spécifique dans votre dépôt, vous pouvez simplifier cette section ou la supprimer.