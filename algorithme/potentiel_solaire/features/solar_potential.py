import geopandas as gpd

from potentiel_solaire.features.pvgis_api import build_query_params_url, call_pvgis_api
from potentiel_solaire.logger import get_logger
from potentiel_solaire.features.protected_tag import link_protected_buildings
from potentiel_solaire.constants import (
    CRS_FOR_BUFFERS
)

logger = get_logger()


def calculate_solar_potential(
    schools_buildings: gpd.GeoDataFrame,
    areas_with_protected_buildings: gpd.GeoDataFrame,
    crs_for_buffers: int = CRS_FOR_BUFFERS
) -> gpd.GeoDataFrame:
    """Fonction principale pour calculer le potentiel solaire.

    :param schools_buildings: les batiments rataches a une ecole
    :param areas_with_protected_buildings: gdf des zones avec des batiments proteges
    :param crs_for_buffers: crs utilise pour le calcul des buffers (en metres)
    :return: le geodataframe des batiments scolaires avec les features de potentiel solaire et le
    productible annuel estimé par l'API PVGIS.
    """
    # Extrait latitude & longitude de la geometry
    schools_buildings['lon'] = schools_buildings.centroid.map(lambda p: p.x)
    schools_buildings['lat'] = schools_buildings.centroid.map(lambda p: p.y)

    # Calcul de la surface totale au sol
    crs_init = schools_buildings.crs
    schools_buildings = schools_buildings.to_crs(epsg=crs_for_buffers)
    schools_buildings["surface_totale_au_sol"] = schools_buildings.area
    schools_buildings = schools_buildings.to_crs(crs_init)

    # Calcul de la surface de toit utile
    schools_buildings["surface_utile"] = schools_buildings["surface_totale_au_sol"].map(
       lambda surface_totale: calculate_surface_utile(surface_totale)
    )
    
    # Calcul de la capacité installé
    schools_buildings["peakpower"] = schools_buildings["surface_utile"].map(
        lambda surface_utile: calculate_installed_capacity(surface_utile)
    )

    # Construire la requête pour PVGIS
    schools_buildings["url"] = schools_buildings[["lat", "lon", "peakpower"]].apply(
        lambda query_params: build_query_params_url(query_params), axis=1
    )
    
    # Requête API PVGIS
    schools_buildings["potentiel_solaire"] = schools_buildings[["url", "peakpower"]].apply(
        lambda x: call_pvgis_api(x["url"]) if x["peakpower"] > 0 else 0, axis=1
    )

    # Ajout du tag batiments proteges ou en zone protegee
    schools_buildings["protection"] = schools_buildings["geometry"].map(
        lambda geometry: link_protected_buildings(
            building=geometry,
            areas_with_protected_buildings=areas_with_protected_buildings
        )
    )

    return schools_buildings


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


def calculate_installed_capacity(rooftop_surface: float) -> float:
    """
    Transform useable surface into installed capacity (peakpower), with assumption that a 
    typical PV panel produces 225W/m2, as per some modules here https://www.csisolar.com/module/.
    """
    return rooftop_surface * 225 / 1_000  # in kW
