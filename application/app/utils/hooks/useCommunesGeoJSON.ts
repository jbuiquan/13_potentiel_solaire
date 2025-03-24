import useSWR from 'swr';

import { fetchCommunesGeoJSON } from '../fetchers/fetchCommunesGeoJSON';

export default function useCommunesGeoJSON(codeDepartement: string | null, enabled = true) {
	const key = enabled ? ['communesGeoJSON', codeDepartement] : null;

	console.log(key);

	const { data, error, isLoading } = useSWR(key, () => fetchCommunesGeoJSON(codeDepartement), {
		keepPreviousData: true,
	});

	return {
		communesGeoJSON: data,
		isError: error,
		isLoading,
	};
}
