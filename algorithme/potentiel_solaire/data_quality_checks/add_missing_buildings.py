

import pandas as pd
import geopandas as gpd

def add_pci_buildings_missing_topo(topo_buildings: gpd.GeoDataFrame, pci_buildings: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Add missing buildings from the PCI db to the TOPO db
    
    Steps:
    1. Ensure same CRS
    2. Identify which PCI buildings are missing from TOPO
    3. Add them to the TOPO structure
    """

    if topo_buildings.crs != pci_buildings.crs:
        pci_buildings = pci_buildings.to_crs(topo_buildings.crs)
    
    topo_sindex = topo_buildings.sindex
    
    new_buildings = []
    for idx, pci_building in pci_buildings.iterrows():
        possible_matches = list(topo_sindex.intersection(pci_building.geometry.bounds))
        
        if not possible_matches:
            # no overlap - this is a new building
            new_building = {
                'geometry': pci_building.geometry,
                'cleabs': f'PCI_{idx}',  
                'construction_legere': False,  
                'hauteur': None,
                'source': 'PCI'  
            }
            new_buildings.append(new_building)
            continue
            
        # check overlap > threshold 
        is_new = True
        for match_idx in possible_matches:
            topo_geom = topo_buildings.iloc[match_idx].geometry
            if pci_building.geometry.intersects(topo_geom):
                # Calculate overlap ratio
                intersection_area = pci_building.geometry.intersection(topo_geom).area
                min_area = min(pci_building.geometry.area, topo_geom.area)
                overlap_ratio = intersection_area / min_area
                
                if overlap_ratio > 0.1:  # buildings overlap by more than 10%
                    is_new = False
                    break
        
        if is_new:
            new_building = {
                'geometry': pci_building.geometry,
                'cleabs': f'PCI_{idx}',
                'construction_legere': False,
                'hauteur': None,
                'source': 'PCI'
            }
            new_buildings.append(new_building)
    
    if new_buildings:
        new_buildings_gdf = gpd.GeoDataFrame(new_buildings, crs=topo_buildings.crs)
        
        # add source to original TOPO buildings
        topo_buildings = topo_buildings.copy()
        topo_buildings['source'] = 'TOPO'
        
        final_buildings = pd.concat([topo_buildings, new_buildings_gdf], ignore_index=True)
    else:
        final_buildings = topo_buildings.copy()
        final_buildings['source'] = 'TOPO'
    
    print(f"Original TOPO buildings: {len(topo_buildings)}")
    print(f"Added PCI buildings: {len(new_buildings)}")
    print(f"Total buildings: {len(final_buildings)}")
    
    return final_buildings
