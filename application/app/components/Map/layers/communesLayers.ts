import { LayerProps } from 'react-map-gl/maplibre';

import { zonesLayerPaint } from './zonesLayersPaint';

export const COMMUNES_SOURCE_ID = 'communes';

export const communesLayer = {
	id: 'communes',
	type: 'fill',
	source: COMMUNES_SOURCE_ID,
	// The communes zones arent filled to be able to see the map
	//paint: { ...zonesLayerPaint, 'fill-color': '', 'fill-opacity': 0 },
	paint: zonesLayerPaint,
	maxzoom: 11,
} satisfies LayerProps;

export function getDynamicalCommunesLayer(isVisible: boolean): LayerProps {
	return {
		...communesLayer,
		layout: { visibility: isVisible ? 'visible' : 'none' },
	};
}

export const communesLineLayer = {
	id: 'communesLine',
	type: 'line',
	source: COMMUNES_SOURCE_ID,
	paint: { 'line-color': 'grey', 'line-width': 1 },
} satisfies LayerProps;

export function getDynamicalCommunesLineLayer(isVisible: boolean): LayerProps {
	return {
		...communesLineLayer,
		layout: { visibility: isVisible ? 'visible' : 'none' },
	};
}
