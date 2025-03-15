## Création de la base de données DuckDB

Pour initialiser une base duckdb :

En utilisant le CLI :

1. Télécharger le CLI pour son environnement et l'installer - https://duckdb.org/docs/installation/?version=stable&environment=cli

    Pour linux, par exemple :
    `curl https://install.duckdb.org | sh`

	Pour Windows, par exemple :
	`winget install DuckDB.cli`

2. Se rendre dans le répertoire où se trouve le script SQL ({repertoire_projet}/algorithm/)

    `cd /database/`

3. Lancer la commande de création de la base

    `duckdb -init .\create-database.sql -no-stdin potentiel_solaire.duckdb`

En utilisant un éditeur SQL, par exemple DBeaver : https://dbeaver.io/

1. Installer l'outil
2. Créer une connexion duckdb en choisissant l'option pour créer une base et lui fournir un chemin pour la base de données
3. Ouvrir le script sql sur cette nouvelle base de données et l'exécuter


## Recuperation des données brutes

Etre dans le dossier algorithme

    cd algorithme

Installer les dépendances & activer l'environnement

    poetry install
    poetry shell

Lancer le script de recuperation sur un departement

    run-pipeline-algorithme -d 093

Une fois ce script réussi, les données et resultats devraient être visibles dans ce dossier data.
