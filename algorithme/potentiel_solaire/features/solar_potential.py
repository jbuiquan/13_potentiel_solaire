import random

import geopandas as gpd


def calculate_solar_potential(
    schools_buildings: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:

    # TODO: Calculs faux pour le moment

    schools_buildings["surface_utile"] = schools_buildings.apply(
        lambda building: random.choice(range(0, 50)), axis=1
    )

    schools_buildings["protection"] = schools_buildings.apply(
        lambda building: random.choice([True, False]), axis=1
    )

    schools_buildings["rayonnement_solaire"] = schools_buildings.apply(
        lambda building: random.choice(range(0, 150)), axis=1
    )

    schools_buildings["potentiel_solaire"] = schools_buildings.apply(
        lambda building: random.choice(range(0, 1500)), axis=1
    )

    return schools_buildings
