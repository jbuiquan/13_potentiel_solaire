import geopandas as gpd
from potentiel_solaire.constants import DATA_FOLDER, CRS
from potentiel_solaire.logger import get_logger

logger = get_logger()


def extract_protected_buildings(
    crs: int = CRS
) -> str:
    """Extrait les batiments proteges

    :param crs: projection
    :return: chemin du fichier .geojson des batiments proteges
    """
    protected_buildings_file_url = "https://data.culturecommunication.gouv.fr/api/explore/v2.1/catalog/datasets/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/exports/geojson?lang=fr&timezone=Europe%2FBerlin"

    protected_buildings = gpd.read_file(protected_buildings_file_url)

    protected_buildings = protected_buildings.to_crs(crs)

    protected_buildings = protected_buildings[[
        "reference",
        "departement_format_numerique",
        "geometry"
    ]]

    protected_buildings_path = f"{DATA_FOLDER}/liste_immeubles_proteges.geojson"

    protected_buildings.to_file(protected_buildings_path, driver='GeoJSON')  

    return protected_buildings_path


def get_protected_buildings_of_interest(
    bd_protected_buildings_path: str,
    geom_of_interest: gpd.GeoDataFrame,
    crs: int = CRS
):
    """Filtre et renvoit les batiments proteges sur la zone d'interet

    :param bd_protected_buildings_path: chemin du fichier .geojson des batiments proteges
    :param geom_of_interest: geodataframe avec la geometrie d interet
    :param crs: projection
    :return: gdf des batiments proteges sur la zone d'interet
    """
    protected_buildings = gpd.read_file(
        bd_protected_buildings_path, mask=geom_of_interest
    ).to_crs(crs)

    return protected_buildings
