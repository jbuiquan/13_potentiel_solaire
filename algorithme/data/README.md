## Recuperation des données

Etre dans le dossier algorithme

    cd algorithme

Installer les dépendances & activer l'environnement

    poetry install
    poetry shell

Initialiser la base de données duckdb

    alembic upgrade head

Lancer le script de recuperation sur un departement

    run-pipeline-algorithme -d 093

Une fois ce script réussi, les données et resultats devraient être visibles :
* dans ce dossier pour les fichiers sources listes dans [sources.yaml](sources.yaml)
* dans le dossier [results](results) pour les resultats sur le departement : [093_pipeline_results.gpkg](results/D093_pipeline_results.gpkg)
* dans la [database duckdb](../database/potentiel_solaire.duckdb)
