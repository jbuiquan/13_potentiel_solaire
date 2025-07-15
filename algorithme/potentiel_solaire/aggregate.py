import geopandas as gpd


def merge_schools_etablissements_with_buildings_results(
    schools_establishments: gpd.GeoDataFrame,
    schools_buildings_results: gpd.GeoDataFrame
):
    """Merge les resultats par batiment avec les etablissements scolaires

    :param schools_establishments: annuaire des etablissements scolaires
    :param schools_buildings_results: potentiel solaire a lechelle des batiments
    :return: geodataframe des resultats de potentiel solaire merge avec les etablissements scolaires
    """
    return schools_establishments.merge(
        schools_buildings_results,
        how="left",
        on="identifiant_de_l_etablissement"
    ).copy()


def aggregate_buildings_attachment_by_etablishment(
    schools_establishments: gpd.GeoDataFrame,
    schools_buildings_results: gpd.GeoDataFrame
):
    """Aggrege les resultats de potentiel solaire par établissement

    :param schools_establishments: annuaire des etablissements scolaires
    :param schools_buildings_results: potentiel solaire a lechelle des batiments
    :return: geodataframe des resultats aggreges
    """
    schools_buildings_results["nb_batiments_associes"] = 1

    schools_buildings_results = merge_schools_etablissements_with_buildings_results(
        schools_establishments,
        schools_buildings_results
    )

    schools_buildings_results.loc[schools_buildings_results['nb_batiments_associes'].isna(), 'nb_batiments_associes'] = 0

    return schools_buildings_results.groupby(by=["identifiant_de_l_etablissement"]).agg({
        "nb_batiments_associes": "sum",
    }).reset_index()



def aggregate_protection_by_etablishment(
    schools_establishments: gpd.GeoDataFrame,
    schools_buildings_results: gpd.GeoDataFrame
):
    """Aggrege les resultats de protection par établissement

    :param schools_establishments: annuaire des etablissements scolaires
    :param schools_buildings_results: protection a lechelle des batiments
    :return: geodataframe des resultats aggreges
    """
    schools_buildings_results = merge_schools_etablissements_with_buildings_results(
        schools_establishments,
        schools_buildings_results
    )
    
    schools_buildings_results.loc[schools_buildings_results['protection'].isna(), 'protection'] = False

    return schools_buildings_results.groupby(by=["identifiant_de_l_etablissement"]).agg({
        "protection": "any",  # Si un seul batiment est protégé, l'établissement est protégé.
    }).reset_index()


def aggregate_solar_potential_by_etablishment(
    schools_establishments: gpd.GeoDataFrame,
    schools_buildings_results: gpd.GeoDataFrame
):
    """Aggrege les resultats de potentiel solaire par établissement

    :param schools_establishments: annuaire des etablissements scolaires
    :param schools_buildings_results: potentiel solaire a lechelle des batiments
    :return: geodataframe des resultats aggreges
    """
    schools_buildings_results = merge_schools_etablissements_with_buildings_results(
        schools_establishments,
        schools_buildings_results
    )
    
    schools_buildings_results.loc[schools_buildings_results['surface_utile'].isna(), 'surface_utile'] = 0
    schools_buildings_results.loc[schools_buildings_results['potentiel_solaire'].isna(), 'potentiel_solaire'] = 0

    return schools_buildings_results.groupby(by=["identifiant_de_l_etablissement"]).agg({
        "surface_utile": "sum",
        "potentiel_solaire": "sum",
    }).reset_index()
