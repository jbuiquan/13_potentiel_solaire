"""
File containing the pipeline methodo to call the PVGIS API and add relevant solar system 
assumptions.
https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis_en
"""
from time import sleep
import geopandas as gpd
import json
import requests

from potentiel_solaire.logger import get_logger


logger = get_logger()


PVGIS_BASE_URL = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?&"

DEFAULT_QUERY_PARAMS = {
    'loss': 14, # The system's losses in percentage. Recommend between 15 - 30 %
    'fixed': 1,  # Fixed versus solar tracking system. Fixed in case of solar rooftop.
    'mountingplace': 'building', # Param should impacts losses. We may be double counting.
    'optimalangles': 1, # Letting the engine optimise the ti
}

V0_OPTIMISED_PVGIS_QUERY_PARAMS = [
    'lat', 
    'lon',
    'peakpower',
]

V0_BASIC_QUERY_PARAMS = [
    'lat', 
    'lon',
    'angle',
    'aspect', # azimuth
    'peakpower'
]

def build_query_params_url(params: gpd.GeoSeries) -> str:
    """
    Helper function building the PV GIS API query url with all requested params.
    Adds a check on the only required parameters.
    """
    if (params['peakpower'] <= 0) or params[['lat', 'lon']].isna().any():
        return None
    
    url= PVGIS_BASE_URL + "&".join([f'{key}={value}' for key, value 
                                    in DEFAULT_QUERY_PARAMS.items()]) + '&'
    url+= "&".join([f'{idx}={params[idx]}' for idx in params.index])
    return url + '&outputformat=json'


def call_pvgis_api(query: str | None) -> float | None:
    """
    Method used to build api url and calls the PVGIS API.
    
    Returns the annual energy production (MWh/yr)
    
    NOTE: Added sleep timer to ensure that we do not exceed the 30 calls / second rate limit.
    TODO: There are many more output parameters available.
    """
    if not query:
        return None
    
    try:
        if response := requests.get(query):
            row_json = json.loads(response.text)
            sleep(0.04)
            return row_json['outputs']['totals']['fixed']['E_y'] / 1_000
        logger.error(f'Failed to query API. Response: {response}')
        return None
    except Exception as e:
        logger.error(e)
        return None
