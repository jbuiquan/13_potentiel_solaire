import { LayerProps } from 'react-map-gl/maplibre';

export const DEPARTEMENTS_SOURCE_ID = 'departements';

export const departementsLayer = {
	id: 'departements',
	type: 'fill',
	source: DEPARTEMENTS_SOURCE_ID,
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

export function getDynamicalDepartementsLayer(isVisible: boolean): LayerProps {
	return {
		...departementsLayer,
		layout: { visibility: isVisible ? 'visible' : 'none' },
	};
}
