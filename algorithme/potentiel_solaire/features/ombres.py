import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx
from shapely.affinity import translate
from shapely.ops import unary_union
from shapely import intersection
from pathlib import Path
import numpy as np



def getBatimentsEcoles(ID, ecoles, batiments):
    # @TODO: Docstring à écrire
    ecole_cible = ecoles[ ecoles.cleabs_left == ID]
    zone = ecole_cible["geometry"].iloc[0]
    batiments_ecole = batiments[batiments.within(zone)]
    hauteur_moyenne = batiments_ecole['hauteur'].mean()
    batiments_ecole.fillna(value=hauteur_moyenne, inplace=True)
    return batiments_ecole, ecole_cible, zone



def getBatiments(ID, ecoles, batiments, rayon=100):
    # @TODO: Docstring à écrire
    zone = ecoles[ecoles.cleabs_left == ID]["geometry"].iloc[0]
    batiments_ecole = batiments[batiments.within(zone)]
    hauteur_moyenne = batiments_ecole['hauteur'].mean()
    if hauteur_moyenne > 0:
        batiments_ecole.fillna(value=hauteur_moyenne, inplace=True)
    else:
        raise KeyError("None")
    hauteur_min = batiments_ecole['hauteur'].min()
    batiments["distance"] = batiments.geometry.distance(zone)
    batiments_voisins = batiments[batiments["distance"] < rayon].copy()
    batiments_voisins = batiments[batiments.within(zone.buffer(rayon))]
    hauteur_moyenne_voisins = batiments_voisins['hauteur'].mean()
    batiments_ecole.fillna(value=hauteur_moyenne_voisins, inplace=True)
    return batiments_voisins[batiments_voisins["hauteur"] > hauteur_min]



def getOmbreUnitaire(ombres_potentielles, h, i, shape_batiment, resolution=10):
    # @TODO: Docstring à écrire
    saisons = {
        "hiver": 15,       # Soleil bas en hiver (21 décembre)
        "printemps": 45,   # Équinoxe (21 mars)
        "été": 75,         # Soleil haut en été (21 juin)
        "automne": 45      # Équinoxe (21 septembre)
    }

    jours_cles = ["hiver", "printemps", "été", "automne"]

    # @TODO: Rajouter plus d'heures
    heures = [12]

    ombre_totale = []
    for _, saison in enumerate(jours_cles):
        for _ in heures:
            angle_solaire = np.radians(saisons[saison])
            for _, row in ombres_potentielles.iterrows():
                hauteur_relative = row["hauteur"] - h
                distance_ombre = hauteur_relative / np.tan(angle_solaire)
                # @TODO: pourquoi hardcoder 45 ci-dessous?
                deplacement_x = distance_ombre * np.cos(np.radians(45))
                deplacement_y = distance_ombre * np.sin(np.radians(45))
                ombre_projetee = []
                for r in range(resolution+1):
                    ombre_projetee.append(translate(row["geometry"], xoff=r*deplacement_x/resolution, yoff=r*deplacement_y/resolution))
                ombre_projetee = unary_union(ombre_projetee)
                ombrage = intersection(shape_batiment,ombre_projetee)
                ombre_totale.append(ombrage)
    ombre_totale = unary_union(ombre_totale)
    return ombre_totale

def getOmbre(batiments_ecole, batiments_hauts):
    ombres = []
    for _, row in batiments_ecole.iterrows():
        h = row["hauteur"]
        i = row["cleabs_left__bat"]
        shape_batiment = row["geometry"]
        ombres_potentielles = batiments_hauts[(batiments_hauts.hauteur > h)]
        ombres_potentielles_shapes = getOmbreUnitaire(ombres_potentielles, h, i, shape_batiment,resolution=10)
        if not ombres_potentielles_shapes.is_empty:
            ombres.append(ombres_potentielles_shapes)
    ombres = unary_union(ombres)
    ombres = gpd.GeoDataFrame(geometry=[ombres], crs=2154)
    ombres["geometries"] = ombres.apply(lambda x: [g for g in x.geometry.geoms], axis=1)
    ombres = ombres.explode(column="geometries").drop(columns="geometry").set_geometry("geometries").rename_geometry("geometry").reset_index(drop=True)
    return ombres