import os 

import geopandas as gpd
import pandas as pd
import requests
import topojson as tp


from potentiel_solaire.logger import get_logger
from potentiel_solaire.classes.source import load_sources
from potentiel_solaire.constants import SOURCES_FILEPATH, DATA_FOLDER, DEFAULT_CRS, DEP_AVEC_ARRONDISSEMENT, EPSILON_SIMPLIFICATION
from potentiel_solaire.sources.utils import fill_holes_in_geodataframe, remove_overlap_in_geodataframe

logger = get_logger()


def get_arrondissements() -> gpd.GeoDataFrame:
    """Renvoit les arrondissements des departements avec des arrondissements"""
    sources = load_sources(SOURCES_FILEPATH)

    departements = gpd.read_file(sources["departements"].filepath).to_crs(4326)

    geom_of_interest = departements[departements["dep"].isin(DEP_AVEC_ARRONDISSEMENT)].dissolve()

    xmin, ymin, xmax, ymax = geom_of_interest.geometry.bounds.loc[0]

    url = "https://data.geopf.fr/wfs/ows"
    params = {
        "service": "WFS",
        "request": "GetFeature",
        "version": "2.0.0",
        "typename": "ADMINEXPRESS-COG.LATEST:arrondissement_municipal",
        "srsname": "EPSG:4326",
        "outputFormat": "application/json",
        "bbox": f"{xmin},{ymin},{xmax},{ymax},EPSG:4326",
    }

    response = requests.get(url, params=params)
    arrondissements = gpd.GeoDataFrame.from_features(response.json()).set_crs(DEFAULT_CRS)
    arrondissements.geometry = arrondissements.geometry.make_valid()

    return arrondissements

def simplify_arrondissements(arrondissements: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Créé un jeu de données avec l'ensemble des communes composées d'arrondissements

    Args:
        output_directory (str, optional): . Defaults to DATA_FOLDER.
    
    Returns:
        Tuple(gpd.GeoDataFrame, list): Un tuple contenant un GeoDataFrame des communes et une liste des codes insee des
        communes qui sont des arrondissements
    """    
    # Simplify arrondissements
    topo = tp.Topology(arrondissements, prequantize=False)
    simplified_arrondissements = topo.toposimplify(EPSILON_SIMPLIFICATION/300).to_gdf()

    # We simplify in two steps to avoid memory issues and ensure that the boundaries are respected
    topo = tp.Topology(simplified_arrondissements, prequantize=False)
    arrondissements_final = topo.toposimplify(EPSILON_SIMPLIFICATION/10, prevent_oversimplify=True).to_gdf()

    topo = tp.Topology(arrondissements_final, prequantize=False)
    arrondissements_final = topo.toposimplify(EPSILON_SIMPLIFICATION, prevent_oversimplify=True).to_gdf()

    return arrondissements_final
    
def get_municipalities() -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """
    Retrieves municipalities, distinguishing those that belong to departments with arrondissements.

    We add the full IDF because the borders that we have to simplify are between the departments of the IDF and the surrounding regions, not within the department

    Returns:
        tuple:
            - municipalities_with_arrondissement (gpd.GeoDataFrame): Municipalities in departments with arrondissements.
            - municipalities_without_arrondissement (gpd.GeoDataFrame): Municipalities in other departments.
    """
    sources = load_sources(SOURCES_FILEPATH)
    municipalities = gpd.read_file(sources["communes"].filepath).to_crs(4326)
    municipalities['codgeo'] = municipalities['codgeo'].astype(str)

    # Filter municipalities based on department codes
    municipalities_with_arrondissement = municipalities[
        (municipalities["dep"].isin(DEP_AVEC_ARRONDISSEMENT)) | (municipalities["reg"] == '11')
    ]
    municipalities_without_arrondissement = municipalities[
        ~(municipalities["dep"].isin(DEP_AVEC_ARRONDISSEMENT)) & (municipalities["reg"] != '11')
    ]

    return municipalities_with_arrondissement, municipalities_without_arrondissement


def split_municipalities_into_arrondissements(output_directory: str = DATA_FOLDER) -> tuple[str, list]:
    """
    Orchestrator function that takes care of splitting the municipalities into arrondissements and ensuring that the geometries are valid, without holes or overlaps.

    Args:
        output_directory (str, optional): Path to save the output file. Defaults to DATA_FOLDER.

    Returns:
        tuple:
            - output_path (str): Path to the output GeoJSON file.
            - modified_departements (list): List of modified department codes.
    """
    # Load arrondissements and municipalities
    arrondissements = get_arrondissements()
    municipalities_with_arrondissement, municipalities_without_arrondissement = get_municipalities()

    # Map department to region
    mapping_dep_region = municipalities_with_arrondissement[['dep', 'reg']].drop_duplicates()

    # Exclude municipalities that are arrondissements - we will replace them with the arrondissements
    codgeos_of_arrondissement_municipalities = [str(codgeo) for codgeo in arrondissements['insee_com'].tolist()]
    municipalities_with_arrondissement = municipalities_with_arrondissement[
        ~municipalities_with_arrondissement['codgeo'].isin(codgeos_of_arrondissement_municipalities)
    ]

    # Rename and clean up arrondissement data
    arrondissements = arrondissements.rename(columns={"insee_arm": "codgeo", 'nom_m': 'libgeo'})
    arrondissements['dep'] = arrondissements['codgeo'].str[:2]
    arrondissements['reg'] = arrondissements['dep'].map(mapping_dep_region.set_index('dep')['reg'])
    arrondissements = arrondissements[['codgeo', 'geometry', 'dep', 'reg', 'libgeo']]

    # Merge back municipalities and arrondissements
    municipalities_with_arrondissement = pd.concat([
        municipalities_with_arrondissement[['codgeo', 'geometry', 'dep', 'reg', 'libgeo']],
        arrondissements
    ], ignore_index=True).drop_duplicates(subset='codgeo', keep='first')

    # Ensure geometries are valid
    municipalities_with_arrondissement['geometry'] = municipalities_with_arrondissement['geometry'].make_valid()
    municipalities_with_arrondissement, _ = fill_holes_in_geodataframe(
        municipalities_with_arrondissement, id_column='codgeo'
    )
    municipalities_with_arrondissement = remove_overlap_in_geodataframe(
        municipalities_with_arrondissement, id_column='codgeo'
    )

    # Track modified departments
    modified_departements = municipalities_with_arrondissement['dep'].unique().tolist()

    # Merge all municipalities and save to file
    municipalities = pd.concat([municipalities_with_arrondissement, municipalities_without_arrondissement], ignore_index=True)
    output_path = os.path.join(output_directory, "communes_updated_with_arrondissements.geojson")
    municipalities.to_file(output_path, driver="GeoJSON")

    return output_path, modified_departements

if __name__ == "__main__":
    split_municipalities_into_arrondissements()
