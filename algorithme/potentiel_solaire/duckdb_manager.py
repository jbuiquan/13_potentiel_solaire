import duckdb
import pandas as pd

def get_connection():
    conn = duckdb.connect('./../database/potentiel_solaire.duckdb')

    # Load Spatial extension
    conn.execute("""
        INSTALL spatial;
        LOAD spatial;
            """)

    conn.commit()

    return conn


def save_solar_potential_by_school(
    results_by_school: pd.DataFrame,
    code_departement: str
):
    with get_connection() as conn:
        conn.register("results_by_school", results_by_school)

        update_query = """
            UPDATE etablissements
            SET 
                surface_utile = results_by_school.surface_utile,
                potentiel_solaire = results_by_school.potentiel_solaire,
                protection = results_by_school.protection
            FROM
                results_by_school
            WHERE
                etablissements.identifiant_de_l_etablissement = results_by_school.identifiant_de_l_etablissement
        """

        conn.execute(update_query)

        query = f"""
            SELECT
                *,
                ST_AsGeoJSON(geo_point) as geometry
            FROM
                etablissements
            WHERE
            code_departement = '{code_departement}'
            """

        stats_schools = conn.query(query).df()

        return stats_schools
    
    return None


def save_solar_potential_by_city(
    code_departement: str
):
    with get_connection() as conn:
        update_query = f"""
            UPDATE communes
            SET 
                surface_utile = agg.surface_utile,
                potentiel_solaire = agg.potentiel_solaire,
                count_etablissements = agg.count_etablissements,
                count_etablissements_proteges = agg.count_etablissements_proteges
            FROM (
                SELECT 
                    code_commune,
                    SUM(surface_utile) AS surface_utile,
                    SUM(potentiel_solaire) AS potentiel_solaire,
                    COUNT(*) AS count_etablissements,
                    SUM(CASE WHEN protection THEN 1 ELSE 0 END) AS count_etablissements_proteges
                FROM etablissements
                GROUP BY code_commune
            ) AS agg
            WHERE
            communes.code_commune = agg.code_commune
            AND communes.code_departement = '{code_departement}'
            """

        conn.execute(update_query)

        query = f"""
        SELECT
            *,
            ST_AsGeoJSON(geom) as geometry
        FROM
            communes
        WHERE
            code_departement = '{code_departement}'
                """

        return conn.query(query).df()
    
    return None

def save_solar_potential_by_department(
    code_departement: str
):
    with get_connection() as conn:
        update_query = f"""
            UPDATE departements
            SET 
                surface_utile = agg.surface_utile,
                potentiel_solaire = agg.potentiel_solaire,
                count_etablissements = agg.count_etablissements,
                count_etablissements_proteges = agg.count_etablissements_proteges
            FROM (
                SELECT 
                    code_departement,
                    SUM(surface_utile) AS surface_utile,
                    SUM(potentiel_solaire) AS potentiel_solaire,
                    COUNT(*) AS count_etablissements,
                    SUM(CASE WHEN protection THEN 1 ELSE 0 END) AS count_etablissements_proteges
                FROM etablissements
                GROUP BY code_departement
            ) AS agg
            WHERE
                departements.code_departement = agg.code_departement
                AND departements.code_departement = '{code_departement}'
            """

        conn.execute(update_query)

        query = f"""
            SELECT
                *,
                ST_AsGeoJSON(geom) as geometry 
            FROM
                departements WHERE code_departement = '{code_departement}'
            """
        return conn.query(query).df()
    
    return None