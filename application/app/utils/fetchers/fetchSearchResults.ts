import { SearchResult } from '@/app/models/search';

const API_ROUTE = '/api/search';

export async function fetchSearchResults(query: string): Promise<SearchResult[]> {
	try {
		const params = new URLSearchParams();
		params.append('query', query);
		const url = `${API_ROUTE}?${params.toString()}`;

		const res = await fetch(url);
		if (!res.ok) throw new Error('Failed to fetch results from search with query ' + query);

		const data = (await res.json()) as SearchResult[];

		return data;
	} catch (error) {
		console.error('Error while retrieving search data with query ' + query, error);
		throw new Error('Failed to fetch results from search with query ' + query);
	}
}
