import geopandas as gpd

from potentiel_solaire.sources.bd_irr import getIrradiationEcole
from potentiel_solaire.features.roof_attributes import calculate_surface_utile
from potentiel_solaire.constants import RENDEMENT_PANNEAU_PV


def calculate_solar_potential(
    schools_buildings: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:

    # Calcul de la surface totale au sol
    crs_init = schools_buildings.crs
    schools_buildings = schools_buildings.to_crs(epsg=6933)  # pourquoi ? est-ce applicable aux DROMs ?
    schools_buildings["surface_totale_au_sol"] = schools_buildings.area
    schools_buildings = schools_buildings.to_crs(crs_init)

    # Calcul de la surface utile
    schools_buildings["surface_utile"] = schools_buildings.apply(
       lambda building: calculate_surface_utile(
           surface_totale_au_sol=building["surface_totale_au_sol"]
       ), axis=1
    )

    schools_buildings["protection"] = schools_buildings.apply(
        lambda building: None, axis=1
    )  # TODO : a implementer

    schools_buildings = getIrradiationEcole(schools_buildings)
    #schools_buildings["rayonnement_solaire"] = schools_buildings.apply(
    #    lambda building: random.choice(range(0, 150)), axis=1
    #)

    schools_buildings["potentiel_solaire"] = \
        schools_buildings["rayonnement_solaire"] * \
        schools_buildings["surface_utile"] * \
        RENDEMENT_PANNEAU_PV

    #schools_buildings["potentiel_solaire"] = schools_buildings.apply(
    #    lambda building: random.choice(range(0, 1500)), axis=1
    #)

    return schools_buildings
