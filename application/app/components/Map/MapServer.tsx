import { Suspense } from 'react';

import { fetchEtablissementsGeoJSON } from '@/app/lib/data';

import Loading from '../Loading';
import { MapClient } from './MapClient';

export default async function Map() {
	const data = await fetchEtablissementsGeoJSON();

	return (
		<Suspense fallback={<Loading />}>
			<MapClient etablissements={data} />
		</Suspense>
	);
}
