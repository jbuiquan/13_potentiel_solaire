import geopandas as gpd
from shapely import Geometry


def link_protected_buildings(
    building: Geometry,
    areas_with_protected_buildings: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Fonction pour lier les batiments proteges aux batiments scolaires.
    
    :param building: batiment rataches a une ecole
    :param areas_with_protected_buildings: gdf des zones avec des batiments proteges
    :return: si le batiment est dans une zone protegee
    """
    building_gdf = gpd.GeoDataFrame(
        {"geometry": [building]},  
        crs=areas_with_protected_buildings.crs
    )

    overlay = gpd.overlay(
        building_gdf,
        areas_with_protected_buildings,
        how="intersection"
    )

    in_protected_area = not overlay.empty

    return in_protected_area


def add_protected_tag_for_buildings(
    schools_buildings: gpd.GeoDataFrame,
    areas_with_protected_buildings: gpd.GeoDataFrame,
):
    """Ajoute le tag de protection aux batiments scolaires.

    :param schools_buildings: gdf des batiments scolaires
    :param areas_with_protected_buildings: gdf des zones avec des batiments proteges
    :return: gdf des batiments scolaires avec le tag de protection
    """
    schools_buildings["protection"] = schools_buildings.apply(
        lambda building: link_protected_buildings(
            building=building["geometry"],
            areas_with_protected_buildings=areas_with_protected_buildings
        ), axis=1
    )

    return schools_buildings

