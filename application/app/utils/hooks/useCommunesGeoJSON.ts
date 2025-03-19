import useSWR from 'swr';

import { fetchCommunesGeoJSON } from '../fetchers/fetchCommunesGeoJSON';

export default function useCommunesGeoJSON() {
	const { data, error, isLoading } = useSWR('communesGeoJSON', fetchCommunesGeoJSON, {
		revalidateOnFocus: false,
		revalidateIfStale: false,
	});

	return {
		communesGeoJSON: data,
		isError: error,
		isLoading,
	};
}
