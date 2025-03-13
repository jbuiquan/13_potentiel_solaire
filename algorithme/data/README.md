## Recuperation des données brutes

Etre dans le dossier algorithme

    cd algorithme

Installer les dépendances & activer l'environnement

    poetry install
    poetry shell

Lancer le script de recuperation

    extract-sample-data

Une fois ce script réussi, les données dézippées devraient être visibles dans ce dossier data.


## Espace à prévoir

Dossiers

```shell
1,6G	../data/BDTOPO_3-4_TOUSTHEMES_GPKG_LAMB93_D093_2024-12-15
206M	../data/PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01
2,6G	../data/MNS-Correl_1-0__TIFF_LAMB93_D093_2024-01-01
```

et les fichiers

```shell
244M BDTOPO_3-4_TOUSTHEMES_GPKG_LAMB93_D093_2024-12-15.7z
165M BDTOPO_3-4_TOUSTHEMES_SHP_LAMB93_D093_2024-12-15.7z
3,3M contour-des-departements.geojson
627M ENR_1-0_POT-SOL-SOL_GPKG_LAMB93_FXX_2024-04-01.7z
141M fr-en-annuaire-education.geojson
 39M PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01.7z
788M potentiel-gisement-solaire-brut-au-bati.geojson
424M potentiel-gisement-solaire-brut-au-bati.gpkg
2,1G potentiel-solaire.geojson
1,1G potentiel-solaire.gpkg
3,2M saint_denis_reference_data.gpkg
```

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
