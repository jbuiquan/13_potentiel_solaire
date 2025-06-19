import { NbEtablissementsByNiveauPotentiel } from './common';
import { TopEtablissement, TypeEtablissement } from './etablissements';

/**
 * List of the Commune type properties.
 */
//TODO: change values to camelCase after merge #190
export const CommunePropertiesKeys = {
	Id: 'code_commune',
	Nom: 'nom_commune',
	CodeDepartement: 'code_departement',
	LibelleDepartement: 'libelle_departement',
	CodeRegion: 'code_region',
	LibelleRegion: 'libelle_region',
	NbElevesTotal: 'nb_eleves_total',
	NbElevesPrimaires: 'nb_eleves_primaires',
	NbEtablissementsTotal: 'nb_etablissements_total',
	NbEtablissementsPrimaires: 'nb_etablissements_primaires',
	NbEtablissementsProtegesTotal: 'nb_etablissements_proteges_total',
	NbEtablissementsProtegesPrimaires: 'nb_etablissements_proteges_primaires',
	SurfaceExploitableMaxTotal: 'surface_exploitable_max_total',
	SurfaceExploitableMaxPrimaires: 'surface_exploitable_max_primaires',
	PotentielSolaireTotal: 'potentiel_solaire_total',
	PotentielSolairePrimaires: 'potentiel_solaire_primaires',
	PotentielNbFoyersTotal: 'potentiel_nb_foyers_total',
	PotentielNbFoyersPrimaires: 'potentiel_nb_foyers_primaires',
	TopEtablissementsTotal: 'top_etablissements_total',
	TopEtablissementsPrimaires: 'top_etablissements_primaires',
	NbEtablissementsParNiveauPotentielTotal: 'nb_etablissements_par_niveau_potentiel_total',
	NbEtablissementsParNiveauPotentielPrimaires: 'nb_etablissements_par_niveau_potentiel_primaires',
} as const;

export type Commune = {
	code_commune: string;
	nom_commune: string;
	code_departement: string;
	libelle_departement: string;
	code_region: string;
	libelle_region: string;
	nb_eleves_total: number;
	nb_eleves_primaires: number;
	nb_etablissements_total: number;
	nb_etablissements_primaires: number;
	nb_etablissements_proteges_total: number;
	nb_etablissements_proteges_primaires: number;
	surface_exploitable_max_total: number;
	surface_exploitable_max_primaires: number;
	potentiel_solaire_total: number;
	potentiel_solaire_primaires: number;
	potentiel_nb_foyers_total: number;
	potentiel_nb_foyers_primaires: number;
	top_etablissements_total: Array<TopEtablissement>;
	top_etablissements_primaires: Array<TopEtablissement>;
	nb_etablissements_par_niveau_potentiel_total: NbEtablissementsByNiveauPotentiel;
	nb_etablissements_par_niveau_potentiel_primaires: NbEtablissementsByNiveauPotentiel;
};

// --- GeoJSON ----
export interface CommuneFeatureProperties {
	code_commune: string;
	nom_commune: string;
	code_departement: string;
	code_region: string;
	potentiel_solaire_total: number;
	potentiel_solaire_lycees: number;
	potentiel_solaire_colleges: number;
	potentiel_solaire_primaires: number;
}
export type CommuneFeature = CommunesGeoJSON['features'][number];

export type CommunesGeoJSON = GeoJSON.FeatureCollection<
	GeoJSON.Polygon | GeoJSON.MultiPolygon,
	CommuneFeatureProperties
>;

// Reference keys for proper access with maplibre layer properties
export const COMMUNE_GEOJSON_KEY_NOM: keyof CommuneFeatureProperties = 'nom_commune';

export const POTENTIEL_KEY_BY_LEVEL_MAPPING: Record<
	TypeEtablissement,
	keyof CommuneFeatureProperties
> = {
	Lycée: 'potentiel_solaire_lycees',
	Collège: 'potentiel_solaire_colleges',
	Ecole: 'potentiel_solaire_primaires',
};
