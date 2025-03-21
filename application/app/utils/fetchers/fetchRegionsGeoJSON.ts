import { RegionsGeoJSON } from '@/app/models/regions';

import getBaseURL from './getBaseURL';

const API_ROUTE = '/api/get-regions';

export async function fetchRegionsGeoJSON(codeRegion: string | null) {
	try {
		const url = new URL(API_ROUTE, getBaseURL());

		if (codeRegion) url.searchParams.append('codeRegion', codeRegion);

		const res = await fetch(url.toString());
		if (!res.ok) throw new Error('Failed to load regions from API');

		const data = (await res.json()) as RegionsGeoJSON;

		return data;
	} catch (error) {
		//TODO: create empty geojson collection as fallback value
		console.error('Error while retrieving regions data:', error);
		throw new Error('Failed to load regions from API');
	}
}
