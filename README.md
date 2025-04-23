# OC_project_3 

Ce projet fait partie du cours de développement Python d'OpenClassrooms. Le but de ce projet est de creer une application logiciel de gestion de tournoi d echec.

## Description

Ce projet consiste à créer une application logiciel de gestion de tournoi d'échec. L'application doit permettre de créer des tournois, de gérer les joueurs, de suivre les tours et les matchs, et enfin de générer des rapports sur les tournois.

## Prérequis

- Python 3.x
- Git

 

## Installation

1. Clonez ce dépôt :
   Dans un terminal, exécuter la commande suivante : 
   git clone https://github.com/xavierjeanne/OC_Project_3.git

2. Accéder au répertoire du projet :
   cd Oc_project_3

3. Créer un environnement virtuel, l'activer puis installer les dépendances :
   python -m venv env
   source env\Scripts\activate
   pip install -r requirements.txt

4. Executer le script :
   python main.py

5. Pour générer un rapport flake8 en html 
   flake8 --format=html --htmldir=flake-report
   le rapport se retouve dans le dossier flake-report (index.html)

## Utilisation de l'application

### Menu principal
Après avoir lancé l'application, vous accéderez au menu principal qui propose trois options :
- **Gestion des Joueurs** : Pour créer et gérer les joueurs
- **Gestion des Tournois** : Pour créer et gérer les tournois
- **Rapports** : Pour consulter différents rapports

### Gestion des Joueurs
1. Cliquez sur "Gestion des Joueurs" depuis le menu principal
2. Pour ajouter un joueur :
   - Remplissez tous les champs (Nom, Prénom, Date de naissance, ID National)
   - L'ID National doit contenir 2 lettres suivies de 5 chiffres
   - La date de naissance doit être au format JJ/MM/AAAA
   - Cliquez sur "Enregistrer"
3. Pour modifier un joueur :
   - Cliquez sur l'icône d'édition à côté du joueur dans la liste
   - Modifiez les informations nécessaires
   - Cliquez sur "Enregistrer"

### Gestion des Tournois
1. Cliquez sur "Gestion des Tournois" depuis le menu principal
2. Pour créer un tournoi :
   - Remplissez les informations du tournoi (Nom, Lieu, Dates, Nombre de tours, Description)
   - Cliquez sur "Enregistrer"
3. Pour ajouter des joueurs à un tournoi :
   - Sélectionnez un tournoi dans la liste en cliquant sur une ligne du tableau
   - Cliquez sur "Ajouter des joueurs"
   - Cochez les joueurs à ajouter (minimum 8)
   - Cliquez sur "Mettre à jour les joueurs"
4. Pour gérer un tournoi :
   - Sélectionnez un tournoi dans la liste
   - Cliquez sur "Gestion du tournoi"

### Gestion d'un tournoi en cours
1. Pour créer un nouveau tour :
   - Cliquez sur "Créer un nouveau tour"
2. Pour terminer un tour :
   - Sélectionnez le tour dans la liste
   - Cliquez sur "Terminer le tour sélectionné"
3. Pour mettre à jour les scores d'un match :
   - Sélectionnez un match dans la liste en cliquant sur une ligne du tableau
   - Cliquez sur "Mettre à jour les scores"
   - Entrez les scores (0, 0.5 ou 1)
   - Cliquez sur "Enregistrer"
4. Pour terminer le tournoi :
   - Cliquez sur "Terminer le tournoi"

### Rapports
1. Cliquez sur "Rapports" depuis le menu principal
2. Naviguez entre les différents onglets pour consulter :
   - Liste des joueurs par ordre alphabétique
   - Liste des tournois
   - Détails d'un tournoi spécifique
   - Joueurs d'un tournoi spécifique
   - Tours et matchs d'un tournoi
   - Scores d'un tournoi

## Structure des données
- Les joueurs sont identifiés par leur ID National unique
- Les tournois comportent par défaut 4 tours
- Les scores possibles pour un match sont : 0 (défaite), 0.5 (match nul), 1 (victoire)
- La somme des scores d'un match ne peut pas dépasser 1


