from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd

from potentiel_solaire.constants import RESULTS_FOLDER

@dataclass
class DepartementResults:
    code_departement: str
    folder: Path = RESULTS_FOLDER

    def __post_init__(self):
        self.folder.mkdir(exist_ok=True)

    @property
    def gpkg_filepath(self) -> Path:
        """Path to the .gpkg file for the departement."""
        return self.folder / f"D{self.code_departement}_pipeline_results.gpkg"
    
    def save_gdf(self, gdf: gpd.GeoDataFrame, layer: str) -> None:
        """Save a GeoDataFrame to the .gpkg file."""
        gdf.to_file(self.gpkg_filepath, layer=layer, driver="GPKG")

    def load_gdf(self, layer: str) -> gpd.GeoDataFrame:
        """Load a GeoDataFrame from the .gpkg file."""
        return gpd.read_file(self.gpkg_filepath, layer=layer)
