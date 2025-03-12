INSTALL spatial;
LOAD spatial;
INSTALL httpfs;
LOAD httpfs;

SET VARIABLE path_to_folder = '../data/referentiels/'; -- exemple : '/path/to/folder/'

-- 1. création des tables depuis les fichiers geojson (la ligne commentée se base sur un fichier local qui sera plus rapide que via https)
-- Dans certains fichiers le code etablissement n'est pas au format 0xx, on utilise donc LPAD à certains endroits pour homogénéiser le format

CREATE OR REPLACE TABLE regions AS
    SELECT
		reg AS code_region,
		libgeo AS libelle_region,
		0 AS surface_utile,
		0::BIGINT AS potentiel_solaire,
		0 AS count_etablissements,
		0 AS count_etablissements_proteges,
		geom
	FROM
		ST_Read(getvariable('path_to_folder') || 'a-reg2021.json') reg
;


--CREATE OR REPLACE TABLE departements AS
    SELECT
		LPAD(dep, 3, '0') AS code_departement,
		libgeo AS libelle_departement,
		reg AS code_region,
		(SELECT libelle_region FROM regions r WHERE r.code_region = dept.reg) AS libelle_region,
		0 AS surface_utile,
		0::BIGINT AS potentiel_solaire,
		0 AS count_etablissements,
		0 AS count_etablissements_proteges,
		geom
	FROM
		ST_Read(getvariable('path_to_folder') || 'a-dep2021.json') dept
;


CREATE OR REPLACE TABLE communes AS
    SELECT
		codgeo AS code_commune,
		libgeo AS nom_commune,
		LPAD(dep, 3, '0') AS code_departement,
		(SELECT libelle_departement FROM departements dept WHERE dept.code_departement = LPAD(com.dep, 3, '0')) AS libelle_departement,
		reg AS code_region,
		(SELECT libelle_region FROM regions r WHERE r.code_region = com.reg) AS libelle_region,
		0 AS surface_utile,
		0::BIGINT AS potentiel_solaire,
		0 AS count_etablissements,
		0 AS count_etablissements_proteges,
		geom
	FROM
		ST_Read(getvariable('path_to_folder') || 'a-com2022.json') com
;


CREATE OR REPLACE TABLE etablissements AS
    SELECT
		identifiant_de_l_etablissement,
		nom_etablissement,
		type_etablissement,
		libelle_nature,
		code_commune,
		nom_commune,
		code_departement,
		libelle_departement,
		code_region,
		libelle_region,
		0 AS surface_utile,
		0 AS rayonnement_solaire,
		0::BIGINT AS potentiel_solaire,
		FALSE AS protection,
		ST_PointOnSurface(geom) as geo_point
	FROM
		ST_Read(getvariable('path_to_folder') || 'fr-en-annuaire-education.geojson')
;
