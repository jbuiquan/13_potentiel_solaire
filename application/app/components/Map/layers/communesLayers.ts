import { LayerProps } from 'react-map-gl/maplibre';

export const COMMUNES_SOURCE_ID = 'communes';

export const communesLayer = {
	id: 'communes',
	type: 'fill',
	source: COMMUNES_SOURCE_ID,
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

export function getDynamicalCommunesLayer(isVisible: boolean): LayerProps {
	return {
		...communesLayer,
		layout: { visibility: isVisible ? 'visible' : 'none' },
	};
}
