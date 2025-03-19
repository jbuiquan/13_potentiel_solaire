import useSWR from 'swr';

import { fetchEtablissementsGeoJSON } from '../fetchers/fetchEtablissementsGeoJSON';

export default function useEtablissementsGeoJSON() {
	const { data, error, isLoading } = useSWR('etablissementsGeoJSON', fetchEtablissementsGeoJSON, {
		revalidateOnFocus: false,
		revalidateIfStale: false,
	});

	return {
		etablissementsGeoJSON: data,
		isError: error,
		isLoading,
	};
}
