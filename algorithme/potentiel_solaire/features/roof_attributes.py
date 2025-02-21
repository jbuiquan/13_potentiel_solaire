# TODO
import os
import geopandas as gpd
from owslib.wms import WebMapService
from rasterio import MemoryFile
import rasterio.mask
from potentiel_solaire.constants import DATA_FOLDER
import numpy as np
import pandas as pd


def getHauteurBatiment(row, cache_file="cache.gpkg", layercache="cache_hauteur"):

    url = "https://data.geopf.fr/wms-r/wms?SERVICE=WMS"
    wms = WebMapService(url, version='1.3.0')

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
        return gdf[gdf.cleabs == row["cleabs"].iloc[0]].hauteur_calculee.iloc[0]
    else:
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
        h = np.average(mnh[np.nonzero(mnh)])
        row["hauteur_calculee"] = h

        if len(existing):
            gtotal = pd.concat([gdf, row[["cleabs", "hauteur_calculee", "hauteur", "geometry"]]])
            gtotal.to_file(cache_h, layer=layercache, driver="GPKG")
        else:
            gtotal = row[["cleabs", "hauteur_calculee", "hauteur", "geometry"]]
            gtotal.to_file(cache_h, layer=layercache, driver="GPKG")
    return h
