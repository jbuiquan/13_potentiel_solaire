"""add indicators for app fiches zone

Revision ID: b80cbbbf68d9
Revises: 49d44d790ee6
Create Date: 2025-04-05 14:57:19.102683

"""
from dataclasses import dataclass
from typing import Optional, Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b80cbbbf68d9'
down_revision: Union[str, None] = '49d44d790ee6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


@dataclass
class Aggregation:
    table: str
    group_by: str
    suffix: str = ""
    type_etablissement: Optional[str] = None

@dataclass
class Indicator:
    name: str
    data_type: str
    default_value: Optional[str] = None

@dataclass
class ZoneAggregationIndicator:
    aggregation: Aggregation
    indicator: Indicator

    @property
    def table_name(self) -> str:
        return self.aggregation.table
    
    @property
    def column_name(self) -> str:
        return f"{self.indicator.name}{self.aggregation.suffix}"
    
    @property
    def column_type(self) -> str:
        return f"{self.indicator.data_type} DEFAULT {self.indicator.default_value}" if self.indicator.default_value else self.indicator.data_type


# aggregations to add
new_aggregations = [
    Aggregation(table="communes", group_by="code_commune", suffix="_primaires", type_etablissement="Ecole"),
    Aggregation(table="communes", group_by="code_commune", suffix="_total"),
    Aggregation(table="departements", group_by="code_departement", suffix="_colleges", type_etablissement="Collège"),
    Aggregation(table="departements", group_by="code_departement", suffix="_total"),
    Aggregation(table="regions", group_by="code_region", suffix="_lycees", type_etablissement="Lycée"),
    Aggregation(table="regions", group_by="code_region", suffix="_total"),
]


# indicators to add
new_indicators = [
    Indicator(name="nb_eleves", data_type="INTEGER", default_value="0"),
    Indicator(name="nb_etablissements", data_type="INTEGER", default_value="0"),
    Indicator(name="nb_etablissements_proteges", data_type="INTEGER", default_value="0"),
    Indicator(name="surface_exploitable_max", data_type="INTEGER", default_value="0"),
    Indicator(name="potentiel_solaire", data_type="BIGINT", default_value="0"),
    Indicator(name="potentiel_nb_foyers", data_type="INTEGER", default_value="0"),
    Indicator(name="top_etablissements", data_type="JSON"),
]


# new indicators x aggregations to add
new_zone_aggregation_indicators = [
    ZoneAggregationIndicator(
        aggregation=aggregation,
        indicator=indicator
    )
    for aggregation in new_aggregations
    for indicator in new_indicators
]


# indicators to delete
deleted_indicators = [
    Indicator(name="surface_utile", data_type="INTEGER", default_value="0"),
    Indicator(name="potentiel_solaire", data_type="BIGINT", default_value="0"),
    Indicator(name="count_etablissements", data_type="INTEGER", default_value="0"),
    Indicator(name="count_etablissements_proteges", data_type="INTEGER", default_value="0"),
]

# aggregations to delete
deleted_aggregations = [
    Aggregation(table="communes", group_by="code_commune"),
    Aggregation(table="departements", group_by="code_departement"),
    Aggregation(table="regions", group_by="code_region"),
]

# deleted indicators x aggregations to delete
deleted_zone_aggregation_indicators = [
    ZoneAggregationIndicator(
        aggregation=aggregation,
        indicator=indicator
    )
    for aggregation in deleted_aggregations
    for indicator in deleted_indicators
]


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSTALL spatial;
        LOAD spatial;
    """)

    # Rename column for surface_utile in etablissements table
    op.execute("""
        ALTER TABLE etablissements
        RENAME COLUMN surface_utile TO surface_exploitable_max
    """)

    # Add new columns to each table
    for zone_agg_ind in new_zone_aggregation_indicators:
        op.execute(f"""
            ALTER TABLE {zone_agg_ind.table_name}
            ADD COLUMN IF NOT EXISTS {zone_agg_ind.column_name} {zone_agg_ind.column_type}
        """)

    # Remove columns for each table
    for zone_agg_ind in deleted_zone_aggregation_indicators:
        op.execute(f"""
            ALTER TABLE {zone_agg_ind.table_name}
            DROP COLUMN IF EXISTS {zone_agg_ind.column_name}
        """)

    # Update values with new schema
    for aggregation in new_aggregations:
        agg_filter = f"type_etablissement = '{aggregation.type_etablissement}'" if aggregation.type_etablissement else "1 = 1"

        op.execute(f"""
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
            WHERE {aggregation.table}.{aggregation.group_by} = agg.{aggregation.group_by}
        """)


        op.execute(f"""
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
            WHERE {aggregation.table}.{aggregation.group_by} = agg.{aggregation.group_by}
        """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        INSTALL spatial;
        LOAD spatial;
    """)

    # Add new columns to each table
    for zone_agg_ind in deleted_zone_aggregation_indicators:
        op.execute(f"""
            ALTER TABLE {zone_agg_ind.table_name}
            ADD COLUMN IF NOT EXISTS {zone_agg_ind.column_name} {zone_agg_ind.column_type}
        """)

    # Remove columns for each table
    for zone_agg_ind in new_zone_aggregation_indicators:
        op.execute(f"""
            ALTER TABLE {zone_agg_ind.table_name}
            DROP COLUMN IF EXISTS {zone_agg_ind.column_name}
        """)
    
    # Rename column for surface_exploitable_max in etablissements table
    op.execute("""
        ALTER TABLE etablissements
        RENAME COLUMN surface_exploitable_max TO surface_utile
    """)

    # Update values with old schema
    for aggregation in deleted_aggregations:
        agg_filter = f"type_etablissement = '{aggregation.type_etablissement}'" if aggregation.type_etablissement else "1 = 1"

        op.execute(f"""
            WITH 
                agg AS (
                    SELECT 
                        {aggregation.group_by},
                        SUM(surface_utile) AS surface_utile,
                        SUM(potentiel_solaire) AS potentiel_solaire,
                        COUNT(*) AS count_etablissements,
                        SUM(CASE WHEN protection THEN 1 ELSE 0 END) AS count_etablissements_proteges,             
                    FROM etablissements
                    WHERE {agg_filter}
                    GROUP BY {aggregation.group_by})


            UPDATE {aggregation.table}
            SET 
                surface_utile{aggregation.suffix} = agg.surface_utile,
                potentiel_solaire{aggregation.suffix} = agg.potentiel_solaire,
                count_etablissements{aggregation.suffix} = agg.count_etablissements,
                count_etablissements_proteges{aggregation.suffix} = agg.count_etablissements_proteges,        
            FROM agg
            WHERE {aggregation.table}.{aggregation.group_by} = agg.{aggregation.group_by}
        """)
