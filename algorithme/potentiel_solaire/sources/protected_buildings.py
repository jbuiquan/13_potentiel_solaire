import geopandas as gpd
from potentiel_solaire.constants import DATA_FOLDER, CRS
from potentiel_solaire.logger import get_logger

logger = get_logger()

def extract_protected_buildings(
        code_departement : "str"
    ) -> str:
    """Extrait les batiments proteges pour un departement donne

    :param code_departement: code du departement
    :return: chemin du fichier .geojson des batiments proteges pour un departement donne
    """

    protected_buildings_file_url = "https://data.culturecommunication.gouv.fr/api/explore/v2.1/catalog/datasets/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/exports/geojson?lang=fr&timezone=Europe%2FBerlin"

    protected_buildings = gpd.read_file(protected_buildings_file_url)

    protected_buildings = protected_buildings.to_crs(CRS)

    protected_buildings = protected_buildings[[
        "reference",
        "departement_format_numerique",
        "geometry"
    ]]

    if code_departement[0] == "0":
        code_departement = code_departement[1:] 

    protected_buildings = protected_buildings[protected_buildings["departement_format_numerique"] == code_departement]

    protected_buildings_path = f"{DATA_FOLDER}/liste_immeubles_proteges_0{code_departement}.geojson"

    protected_buildings.to_file(protected_buildings_path, driver='GeoJSON')  

    return protected_buildings_path