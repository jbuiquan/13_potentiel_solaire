import { SimpleLngLat } from '@/app/lib/data';
import { CommuneFeature } from '@/app/models/communes';

const API_ROUTE = '/api/geolocate';

export async function fetchCommuneFeatureWithGeoloc({ lat, lng }: SimpleLngLat) {
	try {
		const params = new URLSearchParams();

		params.append('lat', lat.toString());
		params.append('lng', lng.toString());

		const url = `${API_ROUTE}?${params.toString()}`;
		const res = await fetch(url);
		if (!res.ok) throw new Error('Failed to load commune with geoloc from API');

		const data = (await res.json()) as CommuneFeature | null;

		return data;
	} catch (error) {
		console.error('Error while retrieving commune data:', error);
		throw new Error('Failed to load commune with geoloc from API');
	}
}
