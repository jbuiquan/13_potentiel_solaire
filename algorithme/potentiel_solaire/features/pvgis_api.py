"""
File containing the pipeline methodo to call the PVGIS API and add relevant solar system 
assumptions.
https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis_en
"""
import asyncio
from time import sleep

import geopandas as gpd
import requests
import aiohttp

from tqdm.asyncio import tqdm

from potentiel_solaire.logger import get_logger

logger = get_logger()


PVGIS_BASE_URL = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?&"


def get_potentiel_solaire_from_pvgis_api(
    lat: float,
    lon: float,
    peakpower: float,
    loss: int = 14,
    fixed: int = 1,
    mountingplace: str = 'building',
    optimalangles: int = 1,
    angle: float = 0,
    aspect: float = 0,
    outputformat: str = "json",
    pvgis_base_url: str = PVGIS_BASE_URL,
) -> float:
    """
    Method used to build api url and calls the PVGIS API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        peakpower (float): Peak power of the solar system in kW.
        loss (int): The system's losses in percentage. Recommend between 15 - 30 %.
        fixed (int): Fixed versus solar tracking system. Fixed in case of solar rooftop.
        mountingplace (str): # Param should impacts losses. We may be double counting.
        optimalangles (int): Letting the engine optimise the tilt angles.
        angle (float): Inclination angle from horizontal plane of the (fixed) PV system.
        aspect (float): Orientation (azimuth) angle of the (fixed) PV system, 0=south, 90=west, -90=east.
        outputformat (str): Format of the output.
        pvgis_base_url (str): Base URL for the PVGIS API.

    Returns the annual energy production (kWh/yr)
    
    NOTE: Added sleep timer to ensure that we do not exceed the 30 calls / second rate limit.
    """
    if peakpower <= 0:
        return 0.0

    params = {
        "lat": lat,
        "lon": lon,
        "peakpower": peakpower,
        "loss": loss,
        "fixed": fixed,
        "mountingplace": mountingplace,
        "optimalangles": optimalangles,
        "angle": angle,
        "aspect": aspect,
        "outputformat": outputformat,
    }

    response = requests.get(pvgis_base_url, params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data['outputs']['totals']['fixed']['E_y']

    if response.status_code == 429:
        sleep(0.04)
        return get_potentiel_solaire_from_pvgis_api(**params, pvgis_base_url=pvgis_base_url)

    if response.status_code == 529:
        sleep(5)
        return get_potentiel_solaire_from_pvgis_api(**params, pvgis_base_url=pvgis_base_url)

    logger.error(f'Failed to query API. Response: {response}')
    response.raise_for_status()


async def async_get_potentiel_solaire_from_pvgis_api(
    lat: float,
    lon: float,
    peakpower: float,
    loss: int = 14,
    fixed: int = 1,
    mountingplace: str = 'building',
    optimalangles: int = 1,
    angle: float = 0,
    aspect: float = 0,
    outputformat: str = "json",
    pvgis_base_url: str = PVGIS_BASE_URL,
    session: aiohttp.ClientSession = None,
    pbar: tqdm = None
) -> float:
    """
    Async version of get_potentiel_solaire_from_pvgis_api.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        peakpower (float): Peak power of the solar system in kW.
        loss (int): The system's losses in percentage. Recommend between 15 - 30 %.
        fixed (int): Fixed versus solar tracking system. Fixed in case of solar rooftop.
        mountingplace (str): # Param should impacts losses. We may be double counting.
        optimalangles (int): Letting the engine optimise the tilt angles.
        angle (float): Inclination angle from horizontal plane of the (fixed) PV system.
        aspect (float): Orientation (azimuth) angle of the (fixed) PV system, 0=south, 90=west, -90=east.
        outputformat (str): Format of the output.
        pvgis_base_url (str): Base URL for the PVGIS API.
        session (aiohttp.ClientSession): Optional, pass an existing session for efficiency.
        pbar (tqdm): Optional, pass a tqdm progress bar for tracking progress.

    Returns the annual energy production (kWh/yr)
    """
    if peakpower <= 0:
        return 0.0

    params = {
        "lat": lat,
        "lon": lon,
        "peakpower": peakpower,
        "loss": loss,
        "fixed": fixed,
        "mountingplace": mountingplace,
        "optimalangles": optimalangles,
        "angle": angle,
        "aspect": aspect,
        "outputformat": outputformat,
    }

    if session is None:
        session = aiohttp.ClientSession()

    async with session.get(pvgis_base_url, params=params) as response:
        if response.status == 200:
            data = await response.json()
            if pbar is not None:
                pbar.update(1)
            return data['outputs']['totals']['fixed']['E_y']

        if response.status == 429:
            await asyncio.sleep(0.04)
            return await async_get_potentiel_solaire_from_pvgis_api(
                **params,
                pvgis_base_url=pvgis_base_url,
                session=session,
                pbar=pbar,
            )

        if response.status == 529:
            await asyncio.sleep(5)
            return await async_get_potentiel_solaire_from_pvgis_api(
                **params,
                pvgis_base_url=pvgis_base_url,
                session=session,
                pbar=pbar,
            )

        logger.error(f'Failed to query API. Response: {response}')
        raise requests.exceptions.HTTPError(
            f"PVGIS API error: {response.status} - {response.reason}"
        )


def get_potentiel_solaire_from_closest_building(
    schools_with_distance: gpd.GeoDataFrame,
    peakpower: float,
) -> float:
    """
    Method used to get the solar potential from the building with the minimum value for distance_to_center.
    
    Args:  
        schools_with_distance (gpd.GeoDataFrame): DataFrame containing the buildings and their distance to the center.
        peakpower (float): Peak power of the solar system.
    """

    for number_building in range(len(schools_with_distance)):
        n_closest_building = schools_with_distance.sort_values(
                by = 'distance_to_center',
                ascending = True).iloc[number_building]
            
        longitude = n_closest_building.geometry.centroid.x
        latitude = n_closest_building.geometry.centroid.y
        
        try : 
            potentiel_solaire = get_potentiel_solaire_from_pvgis_api(
                lat=latitude,
                lon=longitude,
                peakpower=peakpower
            )

            logger.info(f"Potentiel solaire calculé sur le batiment {n_closest_building.cleabs_bat}")

            return potentiel_solaire
        
        except requests.exceptions.HTTPError as e:
            # Cette erreur arrive quand lapi ne couvre pas la position demandee
            if e.response.status_code == 500:
                logger.warning(f'500 error encountered for building {n_closest_building.cleabs_bat}. Trying next building.')
                continue 
            raise e       
