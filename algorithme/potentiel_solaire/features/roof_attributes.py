# TODO
import os
import geopandas as gpd
from owslib.wms import WebMapService
from rasterio import MemoryFile
import rasterio.mask
from potentiel_solaire.constants import DATA_FOLDER
import numpy as np
import pandas as pd

def rasterMNH(row):
    url = "https://data.geopf.fr/wms-r/wms?SERVICE=WMS"
    wms = WebMapService(url, version='1.3.0')
    boite = row.total_bounds
    X = int((boite[2]-boite[0])*2)
    Y = int((boite[3]-boite[1])*2)

    img_mns = wms.getmap(layers=["ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES.MNS"], srs='EPSG:2154', bbox=boite, size=(X, Y), format= 'image/geotiff')
    with MemoryFile(img_mns) as memfile:
        with memfile.open() as dataset:
            mns, _ = rasterio.mask.mask(dataset, row.geometry, crop=True)

    img_mnt = wms.getmap(layers=["ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES"], srs='EPSG:2154', bbox=boite, size=(X, Y), format= 'image/geotiff')
    with MemoryFile(img_mnt) as memfile:
        with memfile.open() as dataset:
            mnt, _ = rasterio.mask.mask(dataset, row.geometry, crop=True)
    mnh = mns - mnt
    return mnh

def getMesureMNSToit(row, cache_file="cache.gpkg", layercache="cache_hauteur"):

    row = gpd.GeoDataFrame(row).T
    row = gpd.GeoDataFrame(row, geometry="geometry")
    if "cleabs_left__bat" in row.columns:
        row = row.rename(columns={"cleabs_left__bat": "cleabs"})
    cache_h = DATA_FOLDER / cache_file

    if os.path.isfile(str(cache_h)):
        gdf = gpd.read_file(cache_h, layer=layercache)
        existing = gdf["cleabs"].unique()
    else:
        existing = []
    row = row[["cleabs", "hauteur", "geometry"]]

    if row["cleabs"].iloc[0] in existing:
        h = gdf[gdf.cleabs == row["cleabs"].iloc[0]].hauteur_calculee.iloc[0]
        s = gdf[gdf.cleabs == row["cleabs"].iloc[0]]["hauteur_std-dev"].iloc[0]
        return [h ,s]
    else:
        mnh = rasterMNH(row)
        row["hauteur_calculee"] = np.average(mnh[np.nonzero(mnh)])
        row["hauteur_std-dev"] = np.std(mnh[np.nonzero(mnh)])
        row["hauteur_min"] = np.min(mnh[np.nonzero(mnh)])
        row["hauteur_max"] = np.max(mnh[np.nonzero(mnh)])
        row["hauteur_median"] = np.median(mnh[np.nonzero(mnh)])

        if len(existing):
            gtotal = pd.concat([gdf, row[["cleabs", "hauteur_calculee", "hauteur", "geometry","hauteur_std-dev","hauteur_min","hauteur_max","hauteur_median"]]])
            gtotal.to_file(cache_h, layer=layercache, driver="GPKG")
        else:
            gtotal = row[["cleabs", "hauteur_calculee", "hauteur", "geometry","hauteur_std-dev","hauteur_min","hauteur_max","hauteur_median"]]
            gtotal.to_file(cache_h, layer=layercache, driver="GPKG")

    return [row["hauteur_calculee"], row["hauteur_std-dev"]]

