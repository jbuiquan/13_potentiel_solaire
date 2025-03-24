import { LayerProps } from 'react-map-gl/maplibre';

export const REGIONS_SOURCE_ID = 'regions';

export const regionsLayer = {
	id: 'regions',
	type: 'fill',
	source: REGIONS_SOURCE_ID,
	paint: {
		'fill-color': [
			'interpolate',
			['linear'],
			['get', 'potentiel_solaire'],
			0,
			'black',
			200,
			'yellow',
		],
		'fill-opacity': 0.5,
	},
} satisfies LayerProps;

export function getDynamicalRegionsLayer(isVisible: boolean): LayerProps {
	return {
		...regionsLayer,
		layout: { visibility: isVisible ? 'visible' : 'none' },
	};
}
