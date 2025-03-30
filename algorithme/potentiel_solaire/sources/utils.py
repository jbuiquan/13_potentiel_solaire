import os
import re

import requests
import itertools
from py7zr.py7zr import SevenZipFile

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import unary_union

from potentiel_solaire.logger import get_logger

logger = get_logger()


def find_matching_files(
    folder_path: str,
    filename_pattern: str,
    folder_pattern: str
) -> list[str]:
    """Searches for files in the given folder that match the specified extension and regex pattern.

    :param folder_path: Path to the directory where files are searched.
    :param filename_pattern: The pattern of the file name
    :param folder_pattern: the pattern of the folder where is the file
    :return: List of matching file paths.
    """
    matching_files = []

    for parent, _, filenames in os.walk(folder_path):
        if re.search(folder_pattern, parent):
            for filename in filenames:
                if re.search(filename_pattern, filename):
                    matching_files.append(os.path.join(parent, filename))

    return matching_files


def download_file(
    url: str,
    output_filepath: str
):
    """Download a file from an url if it does not already exist.

    :param url: URL to download.
    :param output_filepath: Path to save the downloaded file.
    """
    filename = url.split('/')[-1]
    if os.path.exists(output_filepath):
        logger.info(f"{filename} already exists, skipping download.")
        return

    logger.info(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"Downloaded {filename}")
        return

    message = f"Failed to download {filename}: {response.status_code}"
    logger.error(message)
    raise requests.HTTPError(message)


def extract_7z(
    input_filepath: str,
    output_folder: str
):
    """Extract a .7z archive if it exists

    :param input_filepath: Path to file to unzip.
    :param output_folder: Path to folder where extracted files are saved."""
    if not os.path.exists(input_filepath):
        message = f"File {input_filepath} not found"
        logger.error(message)
        raise FileNotFoundError(message)

    logger.info(f"Extracting {input_filepath}...")
    with SevenZipFile(input_filepath, mode='r') as archive:
        archive.extractall(output_folder)

    logger.info(f"Extracted {input_filepath}")

def fill_holes_in_geodataframe(gdf, id_column='id'):
    """
    Process a GeoDataFrame to:
    1. Create a union of all geometries
    2. Extract holes from the union
    3. Match each hole to the closest original geometry by ID
    
    Parameters:
    gdf (GeoDataFrame): Input GeoDataFrame with polygon geometries
    id_column (str): Name of the column containing original feature IDs
    
    Returns:
    GeoDataFrame: A GeoDataFrame of holes with their closest original geometry ID
    """
    
    # Make sure we're working with a copy
    gdf = gdf.copy()
    
    # Step 1: Create union of all geometries
    dissolved = unary_union(gdf.geometry)
    
    # Step 2: Extract all holes from the union
    holes = []
    
    # Handle both single Polygon and MultiPolygon cases
    if dissolved.geom_type == 'MultiPolygon':
        for poly in dissolved.geoms:
            for interior in poly.interiors:
                holes.append(Polygon(interior))
    else:
        for interior in dissolved.interiors:
            holes.append(Polygon(interior))
    
    if not holes:
        return gpd.GeoDataFrame(columns=['hole_geometry', id_column], 
                              geometry='hole_geometry', crs=gdf.crs)
    
    # Create GeoDataFrame for holes
    holes_gdf = gpd.GeoDataFrame(geometry=holes, crs=gdf.crs)
    
    # Step 3: Match each hole to closest original geometry
    # We'll use sjoin_nearest which requires geopandas 0.10.0+
    matched = gpd.sjoin_nearest(
        holes_gdf,
        gdf[[id_column, gdf.geometry.name]],
        how='left',
        lsuffix='hole',
        rsuffix='original'
    )
    #keep only one match per hole
    matched = matched.drop_duplicates(subset='geometry', keep='first')
    # Clean up the result - keep only the hole geometry and original ID
    holes_mapped = matched[['geometry', id_column]]
    
    filled_communes =  pd.concat([gdf, holes_mapped], ignore_index=True).dissolve(by =id_column, as_index=False)
    return filled_communes, holes_mapped


def remove_overlap_in_geodataframe(gdf, id_column, priority='larger', keep_geom='first'):
    """
    Remove overlapping areas from polygons, deleting overlaps from only one polygon in each pair.
    
    Parameters:
        gdf (GeoDataFrame): Input GeoDataFrame with polygon geometries.
        id_column (str): Column name to identify features in the output.
        priority (str, optional): Determines which polygon to keep intact when overlaps occur:
            - 'larger' (default) keeps the larger polygon intact.
            - 'smaller' keeps the smaller polygon intact.
        keep_geom (str, optional): When polygons are equal in size:
            - 'first' (default) keeps the first polygon.
            - 'last' keeps the last polygon.
    
    Returns:
        GeoDataFrame: Modified GeoDataFrame with overlaps selectively removed.
    """
    if gdf.empty:
        raise ValueError("Input GeoDataFrame is empty.")
    
    # Create a dictionary of geometries indexed by their IDs
    modified_geoms = {fid: geom for fid, geom in zip(gdf[id_column], gdf.geometry, strict=False)}
    
    # Compare all pairs of polygons
    for (id1, geom1), (id2, geom2) in itertools.combinations(modified_geoms.items(), 2):
        #filter out points and linestring
        if geom1.intersects(geom2) and geom1.geom_type in ['Polygon', 'MultiPolygon'] and geom2.geom_type in ['Polygon', 'MultiPolygon']:
            overlap = geom1.intersection(geom2)
                
            # Decide which geometry to modify
            if priority == 'larger':
                modify = id1 if geom1.area < geom2.area else id2
            elif priority == 'smaller':
                modify = id1 if geom1.area > geom2.area else id2
            else:
                # For equal areas, use keep_geom parameter
                modify = id2 if keep_geom == 'first' else id1
            
            # Remove overlap from the selected geometry if the overlap is a Polygon or MultiPolygon
            if overlap.geom_type in ['Polygon', 'MultiPolygon']:
                # Check if the overlap is a valid geometry
                if overlap.is_valid:
                    modified_geoms[modify] = modified_geoms[modify].difference(overlap)
                else:
                    logger.warning(f"Invalid geometry found: {overlap}. Skipping this geometry.")
    
    # Create a new GeoDataFrame with modified geometries
    new_geometries = gpd.GeoDataFrame(
        {id_column: list(modified_geoms.keys()), 'geometry': list(modified_geoms.values())},
        crs=gdf.crs
    )

    # Merge with original GeoDataFrame to keep other attributes
    gdf = gdf.rename(columns={'geometry': 'original_geometry'})
    merged = gdf.merge(new_geometries, on=id_column, how='left')
    merged = merged.drop(columns=['original_geometry'])
    return merged
