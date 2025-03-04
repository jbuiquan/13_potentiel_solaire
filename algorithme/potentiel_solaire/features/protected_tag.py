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
    in_protected_area = building.intersects(
        areas_with_protected_buildings.union_all()
    )

    return in_protected_area
