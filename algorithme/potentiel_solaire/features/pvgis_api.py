"""
File containing the pipeline methodo to call the PVGIS API and add relevant solar system 
assumptions.
"""

import geopandas as gpd
from dataclasses import dataclass
import json, requests

from algorithme.potentiel_solaire.constants import USEABLE_SURFACE


PVGIS_BASE_URL = f"https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?&"

pvgis_params = dict(
    lat = 48.890751,
    lon = 2.405467,
    angle = 36,
    aspect = 0, # azimuth
    peakpower=1,
)

DEFAULT_QUERY_PARAMS = {
    'loss': 20, # The system's losses in percentage. Recommend between 15 - 30 %
    'fixed': 1,  # Fixed versus solar tracking system. Fixed in case of solar rooftop.
    'mountingplace': 'building', # Param should impacts losses. We may be double counting.
    
}

# @dataclass
# class PVInstallation:
#     id: str
#     lat: float
#     lon: float
#     surface: float
#     angle: float
#     orientation: float
#     horizon: dict[int, float] | None = None
    
    

def call_pvgis_api(df: gpd.GeoDataFrame) -> dict:
    """
    
    """
    # For each row / building
        # Extract lat lon from geometry
        # Apply system assumptions
        # Build string query
        # Query url
        
    
    response = requests.get(url=f'{PVGIS_BASE_URL}&{build_query_params_url(params)}')
    return json.loads(response.text)


def build_query_params_url(params: dict[str, str]) -> str:
    """
    TODO
    """
    url=f'{PVGIS_BASE_URL}&outputformat=json&'
    url= PVGIS_BASE_URL + "&".join([f'{key}={value}' for key, value 
                                    in DEFAULT_QUERY_PARAMS.items()])
    url+= "&".join([f'{key}={value}' for key, value in params.items()])
    return url


def apply_system_assumptions() -> dict:
    """
    
    """
    # Get rid of roofs too small
    # Get rid of roofs badly exposed (from North-West (180) to North-East (360))
    # Reduced total area to useable surface area
    # Calculate system's power from its useable surface
    # Specify rooftop system structural properties
    # Add system's loss assumption
    

def calculate_useable_surface(surface: float) -> float:
    """
    Applies hypothesis of the useable surface, accounting for other installations, space
    between panels, etc.
    """
    return surface * USEABLE_SURFACE


def estimate_installed_capacity(surface: float) -> float:
    """
    Calculates the PV installation wattage from the typical PV panel (225W / m2), as per
    some modules here https://www.csisolar.com/module/ 
    """
    return surface * 225 / 1_000 # in kW
