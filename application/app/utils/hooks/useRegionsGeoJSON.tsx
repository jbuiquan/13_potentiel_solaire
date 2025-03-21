import useSWRImmutable from 'swr/immutable';

import { fetchRegionsGeoJSON } from '../fetchers/fetchRegionsGeoJSON';

export default function useRegionsGeoJSON(codeRegion: string | null) {
	const { data, error, isLoading } = useSWRImmutable('regionsGeoJSON', () =>
		fetchRegionsGeoJSON(codeRegion),
	);

	return {
		regionsGeoJSON: data,
		isError: error,
		isLoading,
	};
}
