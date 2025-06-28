"""enhance search view

Revision ID: 5153ebff0158
Revises: 5f96d921513d
Create Date: 2025-06-28 12:09:06.199271

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5153ebff0158'
down_revision: Union[str, None] = '5f96d921513d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# schema
etablissements_table = "etablissements"
communes_table = "communes"
departements_table = "departements"
regions_table = "regions"
search_view_table = "search_view"


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(f"""
    UPDATE {search_view_table} sv
    SET 
        extra_data = to_json(struct_pack(c.code_departement, c.libelle_departement))
    FROM communes c
    WHERE sv.source_table = 'communes'
    AND sv.id = c.code_commune
    """)

    op.execute(f"""
    UPDATE {search_view_table} sv
    SET 
        sanitized_libelle = lower(regexp_replace(regexp_replace(strip_accents(e.nom_etablissement), '[^\w\s]', ' ', 'g'), '[\s]{2,}', ' ', 'g')) 
            || ' ' || e.code_postal
            || ' ' || lower(regexp_replace(regexp_replace(strip_accents(e.nom_commune), '[^\w\s]', ' ', 'g'), '[\s]{2,}', ' ', 'g')) 
    FROM etablissements e
    WHERE sv.source_table = 'etablissements'
    AND sv.id = e.identifiant_de_l_etablissement;
    """)


def downgrade() -> None:
    """Downgrade schema."""

    # Previous search view table
    op.execute(f"""
    UPDATE {search_view_table} sv
    SET 
         extra_data = NULL::json
    WHERE sv.source_table = 'communes'
    """)

    op.execute(f"""
    UPDATE {search_view_table} sv
    SET 
        sanitized_libelle = lower(regexp_replace(regexp_replace(strip_accents(e.nom_etablissement), '[^\w\s]', ' ', 'g'), '[\s]{2,}', ' ', 'g'))
    FROM etablissements e
    WHERE sv.source_table = 'etablissements'
    AND sv.id = e.identifiant_de_l_etablissement;
    """)
