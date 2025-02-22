import os

import numpy as np
import rasterio.mask
from potentiel_solaire.constants import DATA_FOLDER
from potentiel_solaire.sources.utils import find_matching_files, download_file, extract_7z
from potentiel_solaire.logger import get_logger

logger = get_logger()


def find_irradiation_file(
    data_directory: str = DATA_FOLDER
):
    """ Recupere le chemin du fichier .tif des donnees d irradiation

    :param data_directory: ou sont sauvegardes les fichiers
    :return: le chemin absolu du fichier tif
    """
    files = find_matching_files(
        folder_path=data_directory,
        file_extension=".tif",
        filename_pattern=rf"GlobalHorizontalIrradiation"
    )

    assert len(files) < 2, f"More than one tif has been found for irradiation data"

    return files[0] if len(files) > 0 else None


def extract_bd_irradiation(
    output_directory: str = DATA_FOLDER,
):
    """ Extrait le fichier tif des donnees d irradiation

    :param output_directory: ou sont sauvegardes les fichiers
    :return: le chemin absolu du fichier tif
    """
    # check if already extracted
    irradiation_filepath = find_irradiation_file(
        data_directory=output_directory
    )
    if irradiation_filepath is not None:
        logger.info("irradiation file %s already extracted",
                    irradiation_filepath)
        return irradiation_filepath

    url = "https://data.geopf.fr/telechargement/download/ENR/ENR_1-0_IRR-SOL_TIFF_WGS84G_FXX_2023-10-01/ENR_1-0_IRR-SOL_TIFF_WGS84G_FXX_2023-10-01.7z"

    # download zip file
    output_filename = url.split('/')[-1]
    output_7z_filepath = os.path.join(output_directory, output_filename)
    download_file(url=url, output_filepath=output_7z_filepath)

    # extract zip file
    extract_7z(input_filepath=output_7z_filepath, output_folder=output_directory)

    # delete zip file
    os.remove(output_7z_filepath)

    return find_irradiation_file(data_directory=output_directory)


def getIrradiationEcole(batiment):
    # Définition des sources
    tileIrradiation = "/ENR_1-0_IRR-SOL_TIFF_WGS84G_FXX_2023-10-01/1_DONNEES_LIVRAISON/GlobalHorizontalIrradiation.tif"
    path = str(DATA_FOLDER) + "/"+tileIrradiation
    # On créé une zone buffer autour des batiments
    geo = batiment.to_crs(epsg=6933).buffer(2000)  # buffer de 2km
    batiment["geometry"] = geo
    batiment = batiment.to_crs(epsg=4326)
    # Ouverture de la tile avec le bon masque
    irrs = []
    with rasterio.open(path) as img:
        for _, row in batiment.iterrows():
            mapIrradiation, _ = rasterio.mask.mask(img, \
                                                   [row.geometry], crop=True)
            mapIrradiation[np.isnan(mapIrradiation)] = 0
            irr = np.mean(mapIrradiation[mapIrradiation > 100])
            irrs.append(irr)
    # On retourne l'irradiation moyenne
    batiment["rayonnement_solaire"] = irrs
    return batiment
