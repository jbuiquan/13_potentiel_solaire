import useSWR from 'swr';

import { fetchEtablissementsGeoJSON } from '../fetchers/fetchEtablissementsGeoJSON';

export default function useEtablissementsGeoJSON(codeCommune: string | null, enabled = true) {
	const key = enabled ? ['etablissementsGeoJSON', codeCommune] : null;

	const { data, error, isLoading } = useSWR(key, () => fetchEtablissementsGeoJSON(codeCommune));

	return {
		etablissementsGeoJSON: data,
		isError: error,
		isLoading,
	};
}
