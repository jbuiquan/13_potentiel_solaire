import { FillLayerSpecification } from 'maplibre-gl';

export const zonesLayerPaint = {
	'fill-color': [
		'interpolate',
		['linear'],
		['get', 'potentiel_solaire'],
		0,
		'black',
		200,
		'yellow',
	],
	'fill-opacity': 0.4,
	'fill-outline-color': 'black',
} satisfies FillLayerSpecification['paint'];
