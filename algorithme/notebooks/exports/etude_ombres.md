## Analyse d'ombre sur un établissement de St denis


```python
# Autoreload des modules
%load_ext autoreload
%autoreload 2
```

### Imports


```python
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from pathlib import Path

from potentiel_solaire.features.ombres import getBatimentsEcoles, getOmbre, getBatiments
```


```python
import warnings
warnings.filterwarnings('ignore') 
```


```python
# Executer ci dessous ci besoin pour récupérer les données
# !extract-sample-data
# Et pour sauver une version markdown des notebooks, utiliser
# jupyter nbconvert donnees_par_ecole.ipynb --to markdown --output-dir=exports/
```

### Chargement des Bâtiments et Zones Éducatives


```python
DATA_FOLDER = Path("../data")

saint_denis_path = DATA_FOLDER / "saint_denis_reference_data.gpkg"

ecoles = gpd.read_file(saint_denis_path, layer="bdtopo_education").to_crs(2154)
batiments = gpd.read_file(saint_denis_path, layer="bdtopo_batiment").to_crs(2154)
```

# Création des ombres


```python
# On charge les couches
ecoles = gpd.read_file(saint_denis_path, layer="bdtopo_education").to_crs(2154)
batiments = gpd.read_file(saint_denis_path, layer="bdtopo_batiment").to_crs(2154)
```


```python
# Choix d'une école
ID = "SURFACTI0000000002555648"
```


```python
# Capture des batiments proches
batiments_ecole, ecole_cible, zone = getBatimentsEcoles(ID, ecoles, batiments)
batiments_proches = getBatiments(ID, ecoles, batiments, rayon = 100)
# Et on créé les ombres
ombres = getOmbre(batiments_ecole, batiments_proches)
```


```python
# Et on représente les ombres
fig, ax = plt.subplots(figsize=(15,5))
ecole_cible.plot(ax=ax, alpha=0.2, color ="green", edgecolor='yellow')
batiments_ecole.plot(ax=ax, alpha=0.6, linewidth=1,facecolor="none", edgecolor='red', label="batiments")
batiments_ecole.plot(ax=ax, alpha=0.5,column="hauteur",legend=True,figsize=(15,5),cmap="RdBu_r")
ombres.plot(ax=ax, alpha=0.9, color ="black")
ax.set_title("Ombres portées (en noir) sur les batiments (echelle en mètres)\nEcole ID: "+ID+"\n") 
cx.add_basemap(ax, crs=ecole_cible.crs, source=cx.providers.GeoportailFrance.orthos )
fig.show()
```


    
![png](etude_ombres_files/etude_ombres_12_0.png)
    


# Essayons maintenant avec une date heure


```python
import ephem
from datetime import datetime
import math

def get_sun_position(latitude, longitude, date, hour):
    """
    Calculate sun's position (altitude and azimuth) for given coordinates, date and hour
    
    Args:
        latitude (float): Latitude in degrees (-90 to 90)
        longitude (float): Longitude in degrees (-180 to 180)
        date (str): Date in format 'YYYY-MM-DD'
        hour (int): Hour of the day (0-23)
    
    Returns:
        tuple: (altitude in degrees, azimuth in degrees)
    """
    # Create observer object
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    
    # Parse the date string and set the specified hour
    specified_date = datetime.strptime(date, '%Y-%m-%d')
    specified_date = specified_date.replace(hour=hour, minute=0, second=0)
    observer.date = specified_date
    
    # Calculate sun's position
    sun = ephem.Sun()
    sun.compute(observer)
    
    # Convert altitude and azimuth to degrees
    altitude = math.degrees(sun.alt)
    azimuth = math.degrees(sun.az)
    
    return altitude, azimuth
```


```python
import geopandas as gpd
from shapely.affinity import translate
from shapely.ops import unary_union
from shapely import intersection
import numpy as np
```


```python
a, b= get_sun_position(42, 3, "2024-06-21", 12)
a,b 
```




    (71.32316440778013, 187.2342545098887)




```python

def getOmbreUnitaire(ombres_potentielles, h, i, shape_batiment, resolution=10):
    # @TODO: Docstring à écrire
    saisons = {
        "hiver": "2024-12-21",       # Soleil bas en hiver (21 décembre)
        "printemps": "2024-03-21",   # Équinoxe (21 mars)
        "été": "2024-06-21",         # Soleil haut en été (21 juin)
        "automne": "2024-09-21"      # Équinoxe (21 septembre)
    }

    jours_cles = list(saisons.keys())

    # Heures à considérer
    heures = [10,12,14,16]
    # @TODO à tweaker
    POS = [43,2]
    
    ombre_totale = []
    for _, saison in enumerate(jours_cles):
        for heure in heures:
            X, Y = get_sun_position(POS[0], POS[1], saisons[saison], heure)
            #print(X,Y-180)
            X = np.radians(X)
            Y = np.radians(Y-180)            
            for _, row in ombres_potentielles.iterrows():
                hauteur_relative = row["hauteur"] - h
                distance_ombre = hauteur_relative / np.tan(X)
                # @TODO: pourquoi hardcoder 45 ci-dessous?
                deplacement_x = distance_ombre * np.sin(Y)
                deplacement_y = distance_ombre * np.cos(Y)

                ombre_projetee = []
                for r in range(resolution+1):
                    ombre_projetee.append(translate(row["geometry"], xoff=r*deplacement_x/resolution, yoff=r*deplacement_y/resolution))
                ombre_projetee = unary_union(ombre_projetee)
                ombrage = intersection(ombre_projetee,shape_batiment) # ombre_projetee shape_batiment
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
```


```python
ombres = getOmbre(batiments_ecole, batiments_proches)
```


```python
# Et on représente les ombres
fig, ax = plt.subplots(figsize=(15,5))
ecole_cible.plot(ax=ax, alpha=0.2, color ="green", edgecolor='yellow')
batiments_ecole.plot(ax=ax, alpha=0.6, linewidth=1,facecolor="none", edgecolor='red', label="batiments")
batiments_ecole.plot(ax=ax, alpha=0.8,column="hauteur",legend=True,figsize=(15,5),cmap="RdBu_r")
ombres.plot(ax=ax, alpha=0.9, color ="black")
ax.set_title("Ombres portées (en noir) sur les batiments (échelle en mètres)\nEcole ID: "+ID+"\n") 
cx.add_basemap(ax, crs=ecole_cible.crs, source=cx.providers.GeoportailFrance.orthos )
fig.show()
```


    
![png](etude_ombres_files/etude_ombres_19_0.png)
    

