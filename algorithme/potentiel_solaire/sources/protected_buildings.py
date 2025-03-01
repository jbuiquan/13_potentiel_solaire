import geopandas as gpd
from potentiel_solaire.constants import DATA_FOLDER, CRS, BUFFER_SIZE_FOR_PROTECTED_BUILDINGS
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


def get_areas_with_protected_buildings(
    bd_protected_buildings_path: str,
    geom_of_interest: gpd.GeoDataFrame,
    buffer_size_for_protected_buildings: float = BUFFER_SIZE_FOR_PROTECTED_BUILDINGS,
    crs: int = CRS
):
    """Filtre et renvoit les batiments proteges sur la zone d'interet

    :param bd_protected_buildings_path: chemin du fichier .geojson des batiments proteges
    :param geom_of_interest: geodataframe avec la geometrie d interet
    :param buffer_size_for_protected_buildings: taille du buffer autour des batiments proteges
    :param crs: projection
    :return: gdf des zones avec des batiments proteges
    """
    protected_buildings = gpd.read_file(
        bd_protected_buildings_path, mask=geom_of_interest
    ).to_crs(crs)

    areas_with_protected_buildings = protected_buildings.buffer(
        buffer_size_for_protected_buildings,
        cap_style="round"
    )

    return areas_with_protected_buildings
