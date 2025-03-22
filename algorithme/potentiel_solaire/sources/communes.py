import os
from pathlib import Path
import geopandas as gpd
import pandas as pd

from potentiel_solaire.sources.utils import extract_7z
from potentiel_solaire.logger import get_logger
from potentiel_solaire.classes.source import load_sources
from potentiel_solaire.constants import SOURCES_FILEPATH, DATA_FOLDER, DEFAULT_CRS, DEP_AVEC_ARRONDISSEMENT

logger = get_logger()

# Constantes pour les chemins des fichiers
SUB_PATH_COMMUNES = (
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2025-02-17/ADMIN-EXPRESS/"
    "1_DONNEES_LIVRAISON_2025-02-00188/ADE_3-2_SHP_WGS84G_FRA-ED2025-02-17/COMMUNE.shp"
)
SUB_PATH_ARRONDISSEMENTS = (
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2025-02-17/ADMIN-EXPRESS/"
    "1_DONNEES_LIVRAISON_2025-02-00188/ADE_3-2_SHP_WGS84G_FRA-ED2025-02-17/ARRONDISSEMENT_MUNICIPAL.shp"
)


def rename_columns(gdf: gpd.GeoDataFrame, mapping: dict) -> gpd.GeoDataFrame:
    """
    Renomme les colonnes d'un GeoDataFrame selon un mapping donné.
    """
    return gdf.rename(columns=mapping)[['geometry'] + list(mapping.values())]


def process_communes(communes_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Transforme les données géographiques des communes au format attendu.
    """
    return rename_columns(communes_gdf, {
        'INSEE_DEP': 'dep',
        'INSEE_COM': 'codgeo',
        'INSEE_REG': 'reg',
        'NOM': 'libgeo'
    })


def process_arrondissements(arrondissements_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Transforme les données des arrondissements au format des communes.
    """
    return rename_columns(arrondissements_gdf, {
        'INSEE_DEP': 'dep',
        'INSEE_ARM': 'codgeo',
        'INSEE_REG': 'reg',
        'NOM': 'libgeo'
    })


def extract_and_load_shapefile(extraction_folder: str, sub_path: str) -> gpd.GeoDataFrame:
    """
    Charge un fichier shapefile après extraction si nécessaire.
    """
    shapefile_path = os.path.join(extraction_folder, sub_path)
    return gpd.read_file(shapefile_path).set_crs(4326).to_crs(DEFAULT_CRS)


def extract_communes_arrondissement(department: str, output_directory: str = DATA_FOLDER)-> gpd.GeoDataFrame:
    """
    Extrait et traite les données géographiques des communes ou arrondissements d'un département.
    """
    department = department.lstrip('0')
    dep_avec_arrondissement = department in {dep[0] for dep in DEP_AVEC_ARRONDISSEMENT}
    sources = load_sources(SOURCES_FILEPATH)
    
    path_communes_geo_7z = os.path.join(output_directory,  sources['communes'].zip_filename)
    extraction_folder = path_communes_geo_7z[:-3]

    if not os.path.isdir(extraction_folder):
        extract_7z(path_communes_geo_7z, extraction_folder)
    
    if dep_avec_arrondissement:
        region = next(dep[1] for dep in DEP_AVEC_ARRONDISSEMENT if dep[0] == department)
        arrondissements_gdf = extract_and_load_shapefile(extraction_folder, SUB_PATH_ARRONDISSEMENTS)
        arrondissements_gdf = arrondissements_gdf[arrondissements_gdf['INSEE_ARM'].str[:-3] == department]
        arrondissements_gdf['INSEE_DEP'] = department
        arrondissements_gdf['INSEE_REG'] = region
        arrondissements_gdf = process_arrondissements(arrondissements_gdf)
        return arrondissements_gdf
    else:
        communes_gdf = extract_and_load_shapefile(extraction_folder, SUB_PATH_COMMUNES)
        
        communes_gdf = communes_gdf[communes_gdf['INSEE_DEP'].str.lstrip('0') == department]
        communes_gdf = process_communes(communes_gdf)
        return communes_gdf
    
def create_basefile_communes(output_directory: str = DATA_FOLDER)->None:
    """
    Créé un jeu de données avec l'ensemble des communes, les communes composées d'arondissements sont décomposées en arrondissements.

    Args:
        output_directory (str, optional): . Defaults to DATA_FOLDER.
    """    

    sources = load_sources(SOURCES_FILEPATH)
    
    print('sources loaded')
    path_communes_geo_7z = os.path.join(output_directory, sources['communes'].zip_filename)
    extraction_folder = path_communes_geo_7z[:-3]
    output_path = os.path.join(output_directory, sources['communes'].filename)

    if os.path.exists(output_path):
        return

    if not os.path.isdir(extraction_folder):
        extract_7z(path_communes_geo_7z, extraction_folder)
        print('extraction made')

    communes_gdfs =[]

    all_communes = extract_and_load_shapefile(extraction_folder, SUB_PATH_COMMUNES)
    print('loaded full municipalities')

    for dep_region in DEP_AVEC_ARRONDISSEMENT:
        print(dep_region)
        all_communes = all_communes[all_communes['INSEE_DEP'].str.lstrip('0') != dep_region[0].lstrip('0')]

        arrondissements_gdf = extract_and_load_shapefile(extraction_folder, SUB_PATH_ARRONDISSEMENTS)
        arrondissements_gdf = arrondissements_gdf[arrondissements_gdf['INSEE_ARM'].str[:-3] == dep_region[0]]
        arrondissements_gdf['INSEE_DEP'] = dep_region[0]
        arrondissements_gdf['INSEE_REG'] = dep_region[1]
        arrondissements_gdf = process_arrondissements(arrondissements_gdf)

        communes_gdfs.append(arrondissements_gdf)

    all_communes = process_communes(all_communes)
    communes_gdfs.append(all_communes)
    print('started concatenation')

    communes_gdfs = pd.concat(communes_gdfs, ignore_index=True)

    print('simplification')
    communes_gdfs['geometry'] = communes_gdfs['geometry'].simplify(0.00005)

    communes_gdfs.to_file(output_path)
    


