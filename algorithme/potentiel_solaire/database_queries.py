from importlib.metadata import version
from dataclasses import dataclass
from typing import Literal, Optional

import duckdb
import pandas as pd

from potentiel_solaire.constants import DUCK_DB_PATH
from potentiel_solaire.logger import get_logger

logger = get_logger()


@dataclass
class ZoneAggregation:
    table: Literal["communes", "departements", "regions"]
    group_by: Literal["code_commune", "code_departement", "code_region"]
    suffix: Literal["", "_primaires", "_colleges", "_lycees", "_total"] = ""
    type_etablissement: Optional[Literal["Ecole", "Collège", "Lycée"]] = None


def get_connection():
    conn = duckdb.connect(DUCK_DB_PATH)

    # Load Spatial extension
    conn.execute("""
        INSTALL spatial;
        LOAD spatial;
    """)

    conn.commit()

    return conn


def get_departements():
    with get_connection() as conn:
        query = """
        SELECT code_departement
        FROM departements 
        GROUP BY code_departement
        """

        return list(conn.query(query).df()["code_departement"].unique())


def get_departements_for_region(code_region: str):
    with get_connection() as conn:
        query = f"""
        SELECT code_departement
        FROM departements 
        WHERE code_region = '{code_region}'
        GROUP BY code_departement
        """

        return list(conn.query(query).df()["code_departement"].unique())


def get_regions():
    with get_connection() as conn:
        query = """
        SELECT code_region
        FROM regions 
        GROUP BY code_region
        """

        return list(conn.query(query).df()["code_region"].unique())


def update_results_for_schools(
    results_by_school: pd.DataFrame,
):
    with get_connection() as conn:
        conn.register("results_by_school", results_by_school)

        code_version = version('potentiel_solaire')

        update_query = f"""
            UPDATE etablissements
            SET 
                surface_exploitable_max = results_by_school.surface_utile,
                potentiel_solaire = results_by_school.potentiel_solaire,
                protection = results_by_school.protection,
                date_calcul = CURRENT_TIMESTAMP,
                version = '{code_version}',
                nb_batiments_associes = results_by_school.nb_batiments_associes
            FROM
                results_by_school
            WHERE
                etablissements.identifiant_de_l_etablissement = results_by_school.identifiant_de_l_etablissement
        """

        conn.execute(update_query)


def update_indicators_for_aggregation(
    aggregation: ZoneAggregation,
):
    """Save indicators for a given aggregation"""
    agg_filter = f"type_etablissement = '{aggregation.type_etablissement}'" if aggregation.type_etablissement else "1 = 1"

    update_query = f"""
    WITH 
        agg AS (
            SELECT 
                {aggregation.group_by},
                SUM(COALESCE(nb_eleves, 0)) AS nb_eleves,
                COUNT(*) AS nb_etablissements,
                SUM(CASE WHEN protection THEN 1 ELSE 0 END) AS nb_etablissements_proteges,
                SUM(surface_exploitable_max) AS surface_exploitable_max,
                SUM(potentiel_solaire) AS potentiel_solaire,
            FROM etablissements
            WHERE {agg_filter}
            GROUP BY {aggregation.group_by})


    UPDATE {aggregation.table}
    SET 
        nb_eleves{aggregation.suffix} = agg.nb_eleves,
        nb_etablissements{aggregation.suffix} = agg.nb_etablissements,
        nb_etablissements_proteges{aggregation.suffix} = agg.nb_etablissements_proteges,
        surface_exploitable_max{aggregation.suffix} = agg.surface_exploitable_max,
        potentiel_solaire{aggregation.suffix} = agg.potentiel_solaire,
        potentiel_nb_foyers{aggregation.suffix} = FLOOR(agg.potentiel_solaire / 5000),
    FROM agg
    WHERE {aggregation.table}.{aggregation.group_by} = agg.{aggregation.group_by};

    WITH
        top_etablissements AS (
            SELECT
                {aggregation.group_by},
                json_object(
                    'id', identifiant_de_l_etablissement, 
                    'libelle', nom_etablissement, 
                    'potentiel_solaire', potentiel_solaire
                ) AS etablissement_json,
            FROM etablissements
            WHERE {agg_filter} 
                AND NOT protection 
                AND potentiel_solaire > 0
            QUALIFY ROW_NUMBER() OVER (PARTITION BY {aggregation.group_by} ORDER BY potentiel_solaire DESC) <= 3
            ORDER BY {aggregation.group_by}, potentiel_solaire DESC),
                
        agg AS (
            SELECT
                {aggregation.group_by},
                list(etablissement_json)::JSON AS top_etablissements
            FROM top_etablissements
            GROUP BY {aggregation.group_by}
        )
            
    UPDATE {aggregation.table}
    SET
        top_etablissements{aggregation.suffix} = agg.top_etablissements
    FROM agg
    WHERE {aggregation.table}.{aggregation.group_by} = agg.{aggregation.group_by};
    """
    
    with get_connection() as conn:
        logger.info(f"Saving indicators for {aggregation}")
        conn.execute(update_query)



def update_indicators_for_communes():
    """Update indicators for communes"""
    agggregations = [
        ZoneAggregation(table="communes", group_by="code_commune", suffix="_primaires", type_etablissement="Ecole"),
        ZoneAggregation(table="communes", group_by="code_commune", suffix="_total"),
    ]

    for aggregation in agggregations:
        update_indicators_for_aggregation(aggregation)



def update_indicators_for_departements():
    """Update indicators for departements"""
    agggregations = [
        ZoneAggregation(table="departements", group_by="code_departement", suffix="_colleges", type_etablissement="Collège"),
        ZoneAggregation(table="departements", group_by="code_departement", suffix="_total"),
    ]

    for aggregation in agggregations:
        update_indicators_for_aggregation(aggregation)


def update_indicators_for_regions():
    """Update indicators for regions"""
    agggregations = [
        ZoneAggregation(table="regions", group_by="code_region", suffix="_lycees", type_etablissement="Lycée"),
        ZoneAggregation(table="regions", group_by="code_region", suffix="_total"),
    ]

    for aggregation in agggregations:
        update_indicators_for_aggregation(aggregation)
