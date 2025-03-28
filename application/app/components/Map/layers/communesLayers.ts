import { LayerProps } from 'react-map-gl/maplibre';

import { zonesLayerPaint } from './zonesLayersPaint';

export const COMMUNES_SOURCE_ID = 'communes';

export const communesLayer = {
	id: 'communes',
	type: 'fill',
	source: COMMUNES_SOURCE_ID,
	paint: zonesLayerPaint,
} satisfies LayerProps;

export function getDynamicalCommunesLayer(isVisible: boolean): LayerProps {
	return {
		...communesLayer,
		layout: { visibility: isVisible ? 'visible' : 'none' },
	};
}
