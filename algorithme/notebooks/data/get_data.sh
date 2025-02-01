#!/bin/sh


if [ ! -f ./contour-des-departements.geojson ]; then
    wget https://www.data.gouv.fr/fr/datasets/r/90b9341a-e1f7-4d75-a73c-bbc010c7feeb
    mv 90b9341a-e1f7-4d75-a73c-bbc010c7feeb contour-des-departements.geojson
fi

if [ ! -f ./fr-en-annuaire-education.geojson ]; then
wget https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-annuaire-education/exports/geojson
mv geojson fr-en-annuaire-education.geojson
fi

if [ ! -f ./BDTOPO_3-4_TOUSTHEMES_SHP_LAMB93_D093_2024-12-15.7z ]; then
    wget https://data.geopf.fr/telechargement/download/BDTOPO/BDTOPO_3-4_TOUSTHEMES_SHP_LAMB93_D093_2024-12-15/BDTOPO_3-4_TOUSTHEMES_SHP_LAMB93_D093_2024-12-15.7z
fi

if [ ! -f ./PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01.7z ]; then
    wget https://data.geopf.fr/telechargement/download/PARCELLAIRE-EXPRESS/PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01/PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01.7z
fi

# May need sudo apt-get install p7zip-full

7z x PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01.7z
7z x BDTOPO_3-4_TOUSTHEMES_SHP_LAMB93_D093_2024-12-15.7z