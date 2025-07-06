import { Departement } from '@/app/models/departements';

const API_ROUTE = '/api/departements';

export async function fetchDepartement(id: string) {
	try {
		const url = `${API_ROUTE}/${id}`;

		const res = await fetch(url);
		if (!res.ok) throw new Error('Failed to load departement from API');

		const data = (await res.json()) as Departement | undefined;

		return data;
	} catch (error) {
		console.error('Error while retrieving departement data:', error);
		throw new Error('Failed to load departement from API');
	}
}
