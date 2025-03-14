import { cache, Suspense } from 'react';

import Loading from '../Loading';
import { MapClient } from './MapClient';

//FIXME: move to client side to avoid "Single item size exceeds maxSize" error
//TODO: use swr / tanstack query to handle loading/errors
const fetchEtablissements = cache(async () => {
	try {
		const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/data/etablissements.geojson`);
		if (!res.ok) throw new Error("Failed to load etablissements from geojson file");
		const data = await res.json();
		return {data};
	} catch (error) {
		//TODO: create empty geojson collection as fallback value
		console.error('Error while retrieving etablissements data:', error);
		return {error: true};
	}
  });

const fetchCommunes = cache(async () => {
	try {
		const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/data/communes.geojson`);
		if (!res.ok) throw new Error("Failed to load communes from geojson file");
		const data = await res.json();
		return {data};
	} catch (error) {
		//TODO: create empty geojson collection as fallback value
		console.error('Error while retrieving communes data:', error);
		return {error: true};
	}
});

export default async function Map() {
	const {data: etablissementsGeoJSON, error: errorEtablissements} = await fetchEtablissements();
	const  {data: communesGeoJSON,  error: errorCommunes} = await fetchCommunes();

	if (errorEtablissements || errorCommunes) return ('Erreur lors du chargement des données de la carte...');

	return (
		<Suspense fallback={<Loading />}>
			<MapClient etablissements={etablissementsGeoJSON} communes={communesGeoJSON} />
		</Suspense>
	);
}
