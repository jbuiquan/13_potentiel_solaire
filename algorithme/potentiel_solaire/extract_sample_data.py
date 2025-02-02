import os

import requests
import py7zr

from potentiel_solaire.constants import DATA_FOLDER
from potentiel_solaire.logger import get_logger

logger = get_logger()


def download_file(url, filename, data_folder=DATA_FOLDER):
    """Download a file from a URL if it does not already exist."""
    filepath = data_folder / filename
    if not os.path.exists(filepath):
        logger.info(f"Downloading {filename}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Downloaded {filename}")
        else:
            logger.error(f"Failed to download {filename}: {response.status_code}")
    else:
        logger.info(f"{filename} already exists, skipping download.")


def extract_7z(filename, data_folder=DATA_FOLDER):
    """Extract a .7z archive if it exists."""
    filepath = data_folder / filename
    if os.path.exists(filepath):
        logger.info(f"Extracting {filename}...")
        with py7zr.SevenZipFile(filepath, mode='r') as archive:
            archive.extractall(data_folder)
        logger.info(f"Extracted {filename}")
    else:
        logger.info(f"File {filename} not found, skipping extraction.")


def delete_7z(filename, data_folder=DATA_FOLDER):
    """Delete a .7z archive if it exists."""
    filepath = data_folder / filename
    if os.path.exists(filepath):
        os.remove(filepath)
        logger.info(f"Deleted {filename}")
    else:
        logger.warning(f"File {filename} not found, skipping deletion.")


def main():
    # Define file URLs and names
    files = [
        ("https://www.data.gouv.fr/fr/datasets/r/90b9341a-e1f7-4d75-a73c-bbc010c7feeb",
         "contour-des-departements.geojson"),
        ("https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-annuaire-education/exports/geojson",
         "fr-en-annuaire-education.geojson"),
        ("https://data.geopf.fr/telechargement/download/BDTOPO/BDTOPO_3-4_TOUSTHEMES_GPKG_LAMB93_D093_2024-12-15/BDTOPO_3-4_TOUSTHEMES_GPKG_LAMB93_D093_2024-12-15.7z",
         "BDTOPO_3-4_TOUSTHEMES_GPKG_LAMB93_D093_2024-12-15.7z"),
        ("https://data.geopf.fr/telechargement/download/PARCELLAIRE-EXPRESS/PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01/PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01.7z",
         "PARCELLAIRE-EXPRESS_1-1__SHP_LAMB93_D093_2024-10-01.7z")
    ]

    # Download files
    for url, filename in files:
        download_file(url, filename)
        if filename.endswith(".7z"):
            # Extract .7z files
            extract_7z(filename)
            delete_7z(filename)


if __name__ == "__main__":
    main()
