import geopandas as gpd

from potentiel_solaire.features.solar_exposition import calculate_solar_exposition_building
from potentiel_solaire.features.roof_attributes import calculate_surface_utile
from potentiel_solaire.features.protected_tag import link_protected_buildings
from potentiel_solaire.constants import (
    RENDEMENT_PANNEAU_PV,
    BUFFER_SIZE_FOR_SOLAR_EXPOSITION,
    CRS_FOR_BUFFERS
)


def calculate_solar_potential(
    schools_buildings: gpd.GeoDataFrame,
    bd_irradiation_path: str,
    areas_with_protected_buildings: gpd.GeoDataFrame,
    buffer_for_solar_exposition: int = BUFFER_SIZE_FOR_SOLAR_EXPOSITION,
    rendement_panneau_pv: float = RENDEMENT_PANNEAU_PV,
    crs_for_buffers: int = CRS_FOR_BUFFERS
) -> gpd.GeoDataFrame:
    """Fonction principale pour calculer le potentiel solaire.

    :param schools_buildings: les batiments rataches a une ecole
    :param bd_irradiation_path: chemin du fichier .tif des donnees d irradiation
    :param areas_with_protected_buildings: gdf des zones avec des batiments proteges
    :param buffer_for_solar_exposition: distance autour du batiment a prendre en compte pour le rayonnement solaire
    :param rendement_panneau_pv: ration du rendement d un panneau solaire
    :param crs_for_buffers: crs utilise pour le calcul des buffers (en metres)
    :return: le geodataframe des batiments scolaires avec les features de potentiel solaire
    """

    # Calcul de la surface totale au sol & zone de 2km autour des batiment
    crs_init = schools_buildings.crs
    schools_buildings = schools_buildings.to_crs(epsg=crs_for_buffers)
    schools_buildings["surface_totale_au_sol"] = schools_buildings.area
    schools_buildings["zone_pour_rayonnement_solaire"] = schools_buildings.buffer(
        distance=buffer_for_solar_exposition
    ).to_crs(crs_init)
    schools_buildings = schools_buildings.to_crs(crs_init)

    # Calcul de la surface utile
    schools_buildings["surface_utile"] = schools_buildings.apply(
       lambda building: calculate_surface_utile(
           surface_totale_au_sol=building["surface_totale_au_sol"]
       ), axis=1
    )

    # Calcul de l exposition solaire
    schools_buildings["rayonnement_solaire"] = schools_buildings.apply(
       lambda building: calculate_solar_exposition_building(
           zone_for_solar_exposition=building["zone_pour_rayonnement_solaire"],
           bd_irradiation_path=bd_irradiation_path
       ), axis=1
    )

    # Calcul potentiel solaire
    schools_buildings["potentiel_solaire"] = \
        schools_buildings["rayonnement_solaire"] * \
        schools_buildings["surface_utile"] * \
        rendement_panneau_pv

    # Ajout du tag batiments proteges ou en zone protegee
    schools_buildings["protection"] = schools_buildings.apply(
        lambda building: link_protected_buildings(
            building=building["geometry"],
            areas_with_protected_buildings=areas_with_protected_buildings
        ), axis=1
    )

    return schools_buildings
