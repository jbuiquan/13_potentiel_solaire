import geopandas as gpd
from shapely import Geometry


def link_protected_buildings(
    building: Geometry,
    protected_buildings: gpd.GeoDataFrame,
    buffer_size_for_protected_buildings: float = 0.005
) -> gpd.GeoDataFrame:
    """Fonction pour lier les batiments proteges aux batiments scolaires.
    
    :param building: batiment rataches a une ecole
    :param protected_buildings: gdf des batiments protege
    :param buffer_size_for_protected_buildings: taille du buffer autour des batiments proteges
    :return: si le batiment est dans une zone protegee
    """
    buffer_protected_buildings = protected_buildings.buffer(
        buffer_size_for_protected_buildings, 
        cap_style="round"
    )

    in_protected_area = building.intersects(
        buffer_protected_buildings.unary_union
    )

    return in_protected_area
