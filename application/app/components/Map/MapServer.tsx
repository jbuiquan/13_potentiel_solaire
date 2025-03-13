import { Suspense } from 'react';

import { fetchCommunesGeoJSON, fetchEtablissementsGeoJSON } from '@/app/lib/data';

import Loading from '../Loading';
import { MapClient } from './MapClient';

export default async function Map() {
	const etablissementsGeoJSON = await fetchEtablissementsGeoJSON();
	const communesGeoJSON = await fetchCommunesGeoJSON(null);

	return (
		<Suspense fallback={<Loading />}>
			<MapClient etablissements={etablissementsGeoJSON} communes={communesGeoJSON} />
		</Suspense>
	);
}
