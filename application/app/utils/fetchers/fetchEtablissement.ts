import { Etablissement } from '@/app/models/etablissements';

const API_ROUTE = '/api/etablissements';

export async function fetchEtablissement(id: string, origin?: string) {
	try {
		const url = origin ? `${origin}${API_ROUTE}/${id}` : `${API_ROUTE}/${id}`;

		const res = await fetch(url);
		if (!res.ok) throw new Error('Failed to load etablissement from API');

		const data = (await res.json()) as Etablissement | undefined;

		return data;
	} catch (error) {
		console.error('Error while retrieving etablissement data:', error);
		throw new Error('Failed to load etablissement from API');
	}
}
