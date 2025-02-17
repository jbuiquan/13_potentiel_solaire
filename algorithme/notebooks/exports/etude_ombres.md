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
ax.set_title("Ombres portées (en noir) sur les batiments (echelle en mètres)\nEcole ID: "+id+"\n") 
cx.add_basemap(ax, crs=ecole_cible.crs, source=cx.providers.GeoportailFrance.orthos )
fig.show()
```


    
![png](etude_ombres_files/etude_ombres_12_0.png)
    

