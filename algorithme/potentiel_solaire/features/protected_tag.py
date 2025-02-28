import geopandas as gpd
from shapely import Geometry
from potentiel_solaire.constants import CRS

def link_protected_buildings(
    building : Geometry,
    bd_protected_buildings_path: str,
    buffer_size_for_protected_buildings: float = 0.005
) -> gpd.GeoDataFrame:
    """Fonction pour lier les batiments proteges aux batiments scolaires.
    
    :param building: batiment rataches a une ecole
    :param bd_protected_buildings_path : chemin du fichier .geojson des batiments proteges
    :param buffer_size_for_protected_buildings: taille du buffer autour des batiments proteges
    :return: si le batiment est dans une zone protegee
    """

    protected_buildings = gpd.read_file(bd_protected_buildings_path).to_crs(CRS)

    buffer_protected_buildings = protected_buildings.buffer(
        buffer_size_for_protected_buildings, 
        cap_style="round"
    )

    in_protected_area = building.intersects(
        buffer_protected_buildings.unary_union
    )

    return in_protected_area