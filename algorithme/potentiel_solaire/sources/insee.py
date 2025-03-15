import os

from potentiel_solaire.constants import (
    DATA_FOLDER,
    COMMUNES_GEOMETRIES_FILENAME,
    DEPARTEMENTS_GEOMETRIES_FILENAME,
    REGIONS_GEOMETRIES_FILENAME,
)
from potentiel_solaire.logger import get_logger
from potentiel_solaire.sources.utils import download_file

logger = get_logger()


def extract_insee_communes_geometries(
    output_filename: str = COMMUNES_GEOMETRIES_FILENAME,
    output_directory: str = DATA_FOLDER,
):
    """Extrait les contours des communes francaises

    :param output_filename: nom du fichier cree
    :param output_directory: dossier ou est sauvegarde le fichier
    :return: le chemin du fichier cree
    """
    filepath = os.path.join(output_directory, output_filename)
    if os.path.exists(filepath):
        logger.info("file %s communes geometries already extracted", filepath)
        return filepath

    url = "https://www.data.gouv.fr/fr/datasets/r/fb3580f6-e875-408d-809a-ad22fc418581"
    download_file(url=url, output_filepath=filepath)

    return filepath


def extract_insee_departements_geometries(
    output_filename: str = DEPARTEMENTS_GEOMETRIES_FILENAME,
    output_directory: str = DATA_FOLDER,
):
    """Extrait les contours des departements francais

    :param output_filename: nom du fichier cree
    :param output_directory: dossier ou est sauvegarde le fichier
    :return: le chemin du fichier cree
    """
    filepath = os.path.join(output_directory, output_filename)
    if os.path.exists(filepath):
        logger.info("file %s departements geometries already extracted", filepath)
        return filepath

    url = "https://www.data.gouv.fr/fr/datasets/r/92f37c92-3aae-452c-8af1-c77e6dd590e5"
    download_file(url=url, output_filepath=filepath)

    return filepath


def extract_insee_regions_geometries(
    output_filename: str = REGIONS_GEOMETRIES_FILENAME,
    output_directory: str = DATA_FOLDER,
):
    """Extrait les contours des regions francaises

    :param output_filename: nom du fichier cree
    :param output_directory: dossier ou est sauvegarde le fichier
    :return: le chemin du fichier cree
    """
    filepath = os.path.join(output_directory, output_filename)
    if os.path.exists(filepath):
        logger.info("file %s regions geometries already extracted", filepath)
        return filepath

    url = "https://www.data.gouv.fr/fr/datasets/r/d993e112-848f-4446-b93b-0a9d5997c4a4"
    download_file(url=url, output_filepath=filepath)

    return filepath
