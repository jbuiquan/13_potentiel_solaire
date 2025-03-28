import { LayerProps } from 'react-map-gl/maplibre';

import { zonesLayerPaint } from './zonesLayersPaint';

export const REGIONS_SOURCE_ID = 'regions';

export const regionsLayer = {
	id: 'regions',
	type: 'fill',
	source: REGIONS_SOURCE_ID,
	paint: zonesLayerPaint,
} satisfies LayerProps;

export function getDynamicalRegionsLayer(isVisible: boolean): LayerProps {
	return {
		...regionsLayer,
		layout: { visibility: isVisible ? 'visible' : 'none' },
	};
}
