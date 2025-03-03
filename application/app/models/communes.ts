export interface CommuneProperties {
	code_commune: string;
	nom_commune: string;
	code_departement: string;
	libelle_departement: string;
	code_region: string;
	libelle_region: string;
	surface_utile: number;
	potentiel_solaire: number;
	count_etablissements: number;
	count_etablissements_proteges: number;
}
export type Commune = Communes['features'][number];

export type Communes = GeoJSON.FeatureCollection<GeoJSON.Geometry, CommuneProperties>;
