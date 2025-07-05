from tqdm import tqdm

import geopandas as gpd

from potentiel_solaire.classes.results import DepartementResults
from potentiel_solaire.constants import DEFAULT_CRS
from potentiel_solaire.logger import get_logger
from potentiel_solaire.sources.bd_topo import extract_bd_topo
from potentiel_solaire.sources.extract import extract_sources
from potentiel_solaire.sources.schools_establishments import get_schools_establishments_of_interest

logger = get_logger()


def extract_pipeline(
    codes_departement: list[str],
):
    """Extraction des donnees pour plusieurs departements.

    Args:
        codes_departement (list[str]): Codes des departements pour lesquels les donnees doivent etre extraites.
    """
    # Extraction des sources de donnees
    sources = extract_sources()
    for name, source in sources.items():
        logger.info(f"source {name} extracted at {source.filepath}")

    for code_departement in tqdm(codes_departement):
        # Extraction des donnees pour le departement
        logger.info(f"Extraction des donnees pour le departement {code_departement}")

        # Extraction de la BD TOPO pour le departement
        bd_topo_path = extract_bd_topo(code_departement=code_departement)
        logger.info(f"BD TOPO extraite ici: {bd_topo_path}")

        # Determination des etablissements scolaires du departement
        schools_establishments = get_schools_establishments_of_interest(
            schools_filepath=sources["etablissements"].filepath,
            code_departement=code_departement,
            types_etablissements=['Ecole', 'Lycée', 'Collège'],
            statut_public_prive="Public",
            etat="OUVERT",
            crs=DEFAULT_CRS
        )
        nb_schools = schools_establishments.shape[0]
        logger.info(f"Nb d'établissements scolaires: {nb_schools}")
        
        # Determination de la zone d'interet
        communes = gpd.read_file(bd_topo_path, layer="commune").to_crs(DEFAULT_CRS)
        geom_of_interest = communes.sjoin(schools_establishments).dissolve()[["geometry"]]

        # Save results
        results = DepartementResults(code_departement=code_departement)

        results.save_gdf(
            gdf=schools_establishments, 
            layer="schools_establishments"
        )

        results.save_gdf(
            gdf=geom_of_interest, 
            layer="geom_of_interest"
        )
