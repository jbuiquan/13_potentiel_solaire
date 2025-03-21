import useSWRImmutable from 'swr/immutable';

import { fetchDepartementsGeoJSON } from '../fetchers/fetchDepartementsGeoJSON';

export default function useDepartementsGeoJSON(codeRegion: string | null) {
	const { data, error, isLoading } = useSWRImmutable('departementsGeoJSON', () =>
		fetchDepartementsGeoJSON(codeRegion),
	);

	return {
		departementsGeoJSON: data,
		isError: error,
		isLoading,
	};
}
