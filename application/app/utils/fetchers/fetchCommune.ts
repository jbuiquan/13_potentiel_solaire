import { Commune } from '@/app/models/communes';

const API_ROUTE = '/api/communes';

export async function fetchCommune(id: string) {
	try {
		const url = `${API_ROUTE}/${id}`;

		const res = await fetch(url);
		if (!res.ok) throw new Error('Failed to load commune from API');

		const data = (await res.json()) as Commune | undefined;

		return data;
	} catch (error) {
		console.error('Error while retrieving commune data:', error);
		throw new Error('Failed to load commune from API');
	}
}
