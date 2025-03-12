import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

from potentiel_solaire.features.roof_attributes import recuperation_mns


def getAngles(EW, debug=False):
    # l'array d est la distance au centre de la carte
    d = np.array(range(len(EW))) - len(EW)//2
    # Un px = 2metre donc on normalise
    d = d / 2  # because 2px per meter
    # On calcule l'angle, donc on commence par la tangente
    # Il faut connaitre la hauteur de l'endroit d'où on mesure:
    hcentre = EW[len(EW)//2]
    # On calcule les tangents
    angle_ew = (EW - hcentre) / np.abs(d)
    # On retire les points trops proches dans un rayon de 5m
    angle_ew[np.abs(d) < 10] = 0
    # Et les points en dessous de l'horizon
    angle_ew[angle_ew < 0] = 0
    # On calcule la tangente de l'angle
    angle_ew = np.arctan(angle_ew)
    # Et on remonte à l'angle a travers la tangente
    S = int(np.max(angle_ew[len(EW)//2:])*57.2958)
    N = int(np.max(angle_ew[:len(EW)//2])*57.2958)
    if debug:
        plt.plot(d, EW)
        plt.plot(d, angle_ew*50)
        plt.vlines(0, ymin=min(EW), ymax=max(EW), color="red")
        print("Values", N, S)
    return N, S


def get_horizon_roof(batiment_cible, crs, cache=False):

    if type(batiment_cible) == pd.core.series.Series:
        batiment_cible = pd.DataFrame(batiment_cible).T
        batiment_cible = gpd.GeoDataFrame(batiment_cible,
                                          geometry="geometry",
                                          crs=crs)
    # On créé les images centrées sur le bâtiment
    h = recuperation_mns(batiment_cible, cache=cache)[0]
    hbis = rotate(h, angle=-45, reshape=True)
    # Puis on calcule les angles sur les 4 droites
    angls = np.max(h[:, h.shape[1]//2-10:h.shape[1]//2+10], axis=1)
    n, s = getAngles(angls)
    angls = np.max(h[h.shape[0]//2-10:h.shape[0]//2+10], axis=0)
    w, e = getAngles(angls)
    angls = np.max(hbis[:, hbis.shape[0]//2-10:hbis.shape[0]//2+10], axis=1)
    nw, se = getAngles(angls)
    angls = np.max(hbis[hbis.shape[0]//2-10:hbis.shape[0]//2+10], axis=0)
    sw, ne = getAngles(angls)

    return [n, ne, e, se, s, sw, w, nw]
