import { LayerProps } from 'react-map-gl/maplibre';

import { DEPARTEMENT_GEOJSON_KEY_NOM } from '@/app/models/departements';
import { FilterState } from '@/app/utils/providers/mapFilterProvider';
import { ExpressionSpecification } from '@maplibre/maplibre-gl-style-spec';

import { COLOR_THRESHOLDS } from '../constants';
import { fillColorFromFilters } from './regionsLayers';
import { zonesLayerPaint } from './zonesLayersPaint';

export const DEPARTEMENTS_SOURCE_ID = 'departements';
export const DEPARTEMENTS_LABELS_SOURCE_ID = 'departements-labels';

function getDepartementsLayer(filterState: FilterState, isBackground = false) {
	return {
		id: 'departements',
		type: 'fill',
		source: DEPARTEMENTS_SOURCE_ID,
		paint: zonesLayerPaint(
			COLOR_THRESHOLDS.region,
			isBackground,
			fillColorFromFilters(filterState) as ExpressionSpecification,
		),
		maxzoom: 11,
	} satisfies LayerProps;
}

export const departementsLayer = (filterState: FilterState) => getDepartementsLayer(filterState);
export const departementsBackgroundLayer = (filterState: FilterState) =>
	getDepartementsLayer(filterState, true);

export const departementsLabelsLayer = {
	id: 'departements-labels',
	type: 'symbol',
	source: DEPARTEMENTS_LABELS_SOURCE_ID,
	layout: {
		'text-field': ['get', DEPARTEMENT_GEOJSON_KEY_NOM],
		'text-size': 12,
		'text-anchor': 'center',
		'text-max-width': 5,
		'text-allow-overlap': true,
	},
	paint: {
		'text-color': '#333333',
		'text-halo-color': '#ffffff',
		'text-halo-width': 2,
	},
} satisfies LayerProps;
