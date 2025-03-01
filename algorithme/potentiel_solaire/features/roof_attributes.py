# TODO
from owslib.wms import WebMapService
from rasterio import MemoryFile
import rasterio.mask
import geopandas as gpd


def recuperation_flux_wms(boite: list[int], layer: str,
                          srs: str, X: int, Y: int):
    """
    Retrieve geospatial data from a WMS service as a GeoTIFF image.

    This function connects to the French national geographic institute's (IGN)
    WMS server and retrieves raster data for the specified layer and bounding
    box.

    Parameters
    ----------
    boite : tuple or list
        Bounding box coordinates in the format (xmin, ymin, xmax, ymax)
        defining the area of interest.
    layer : str
        The WMS layer name to request (e.g.,
        "ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES").
    srs : str
        Spatial reference system identifier (e.g., 'EPSG:2154') for the
        coordinate system of the input bounding box and output data.
    X : int
        Width of the requested image in pixels.
    Y : int
        Height of the requested image in pixels.

    Returns
    -------
    bytes
        The raw GeoTIFF image data as a bytes object, which can be processed
        further using libraries like rasterio or saved to a file.

    Notes
    -----
    - Uses the OWSLib WebMapService client to connect to the IGN WMS server
    - Requests data in GeoTIFF format for preserving geospatial information
    - The server URL is hardcoded to the French Géoportail WMS endpoint
    - Uses WMS version 1.3.0 for the request
    """

    url = "https://data.geopf.fr/annexes/ressources/wms-r/essentiels.xml"
    # Originally "https://data.geopf.fr/wms-r/wms?SERVICE=WMS" 
    # but failed with a 'content-type' error.
    wms = WebMapService(url, version='1.3.0')

    img_mns = wms.getmap(layers=[layer],
                         srs=srs, bbox=boite, size=(X, Y),
                         format='image/geotiff')
    return img_mns


def recuperation_mnx_batiment(row: gpd.GeoDataFrame,
                              srs: str,
                              layer: str):
    """
    Retrieve elevation raster data (MNS or MNT) for a specific building
    footprint.

    This function calculates the bounding box of the input geometry,
    retrieves the corresponding elevation data via WMS, and then masks
    the raster to the exact building geometry.

    Parameters
    ----------
    row : geopandas.GeoSeries or similar
        A row containing building geometry information with 'geometry'
        attribute and 'total_bounds' method to retrieve the bounding box.
    srs : str
        Spatial reference system identifier (e.g., 'EPSG:2154') for the
        coordinate system to use in the WMS request.
    layer : str
        WMS layer name to request (e.g.,
        "ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES.MNS"
        for MNS or "ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES" for MNT).

    Returns
    -------
    numpy.ndarray
        Masked elevation raster data corresponding to the building geometry.

    Notes
    -----
    - Uses the recuperation_flux_wms function to retrieve the elevation data
    - Uses rasterio.mask to clip the raster to the building geometry
    - The MemoryFile class is used to handle the raster data in memory
    """
    boite = row.total_bounds
    X = int((boite[2]-boite[0])*2)
    Y = int((boite[3]-boite[1])*2)

    img_mns = recuperation_flux_wms(boite, layer,
                                    srs=srs, X=X, Y=Y)
    with MemoryFile(img_mns) as memfile:
        with memfile.open() as dataset:
            mns, _ = rasterio.mask.mask(dataset, row.geometry, crop=True)

    return mns


def recuperation_mns_batiment(row: gpd.GeoDataFrame):
    srs_mnx = 'EPSG:2154'
    nom_couche_mns = "ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES.MNS"
    return recuperation_mnx_batiment(row, srs_mnx, nom_couche_mns)


def recuperation_mnt_batiment(row: gpd.GeoDataFrame):
    srs_mnx = 'EPSG:2154'
    nom_couche_mnt = "ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES"
    return recuperation_mnx_batiment(row, srs_mnx, nom_couche_mnt)


def recuperation_mnh_batiment(row: gpd.GeoDataFrame):
    """
    Calculate the normalized height model (MNH) for a building by subtracting
    the Digital Terrain Model (MNT) from the Digital Surface Model (MNS).

    This function retrieves both the MNT and MNS data for a specific building
    represented by the input row, and calculates the difference between them to
    obtain the normalized height model, which represents the height of objects
    above ground level.

    Parameters
    ----------
    row : geopandas.GeoSeries
        A row with geometric information about a building, required by the
        underlying recuperation_mnx_batiment function.

    Returns
    -------
    numpy.ndarray or similar
        The MNH for the building, calculated as
        the difference between MNS and MNT values.
    """

    mns = recuperation_mns_batiment(row)
    mnt = recuperation_mnt_batiment(row)
    return mns - mnt


def calculate_surface_utile(surface_totale_au_sol: float):
    """Calcule la surface utile pour le PV.

    Pour le moment il s agit d'un simple ratio.
    @TODO Remplacer par une formule plus fine

    :param surface_totale_au_sol: surface totale au sol du batiment
    :return: la surface utile pour installation de panneaux PV
    """
    if surface_totale_au_sol <= 100:
        return 0

    if 100 < surface_totale_au_sol < 500:
        ratio = 0.4 * surface_totale_au_sol / 5000 + 0.2
        return ratio * surface_totale_au_sol

    return 0.6 * surface_totale_au_sol

