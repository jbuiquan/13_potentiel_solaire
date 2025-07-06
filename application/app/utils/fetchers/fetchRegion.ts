import { Region } from '@/app/models/regions';

const API_ROUTE = '/api/regions';

export async function fetchRegion(id: string) {
	try {
		const url = `${API_ROUTE}/${id}`;

		const res = await fetch(url);
		if (!res.ok) throw new Error('Failed to load region from API');

		const data = (await res.json()) as Region | undefined;

		return data;
	} catch (error) {
		console.error('Error while retrieving region data:', error);
		throw new Error('Failed to load region from API');
	}
}
