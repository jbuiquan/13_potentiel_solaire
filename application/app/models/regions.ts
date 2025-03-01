export interface RegionProperties {
  code_region: string;
  libelle_region: string;
  surface_utile: number;
  potentiel_solaire: number;
  count_etablissements: number;
  count_etablissements_proteges: number;
}
export type Region = Regions["features"][number];

export type Regions = GeoJSON.FeatureCollection<
  GeoJSON.Geometry,
  RegionProperties
>;
