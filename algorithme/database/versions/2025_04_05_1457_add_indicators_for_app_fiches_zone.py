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
