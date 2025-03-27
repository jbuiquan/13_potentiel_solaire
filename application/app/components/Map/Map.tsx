'use client';

import { useRef, useState } from 'react';
import {
	Layer,
	LayerProps,
	LngLatLike,
	Map as MapFromReactMapLibre,
	MapMouseEvent,
	MapProps as MapPropsReactMapLibre,
	MapRef,
	Source,
	ViewStateChangeEvent,
} from 'react-map-gl/maplibre';

import { CommuneFeature } from '@/app/models/communes';
import { DepartementFeature } from '@/app/models/departements';
import { RegionFeature } from '@/app/models/regions';
import useCommunesGeoJSON from '@/app/utils/hooks/useCommunesGeoJSON';
import useDepartementsGeoJSON from '@/app/utils/hooks/useDepartementsGeoJSON';
import useEtablissementsGeoJSON from '@/app/utils/hooks/useEtablissementsGeoJSON';
import useRegionsGeoJSON from '@/app/utils/hooks/useRegionsGeoJSON';
import { bbox } from '@turf/turf';
import { GeoJSONSource } from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

import { EtablissementsGeoJSON } from '../../models/etablissements';
import { ClusterFeature } from './interfaces';
import {
	COMMUNES_SOURCE_ID,
	communesLayer,
	getDynamicalCommunesLayer,
} from './layers/communesLayers';
import {
	DEPARTEMENTS_SOURCE_ID,
	departementsLayer,
	getDynamicalDepartementsLayer,
} from './layers/departementsLayers';
import {
	ETABLISSEMENTS_SOURCE_ID,
	clusterLayer,
	getDynamicalClusterCountLayer,
	getDynamicalClusterLayer,
	getDynamicalUnclusteredPointLayer,
} from './layers/etablissementsLayers';
import { REGIONS_SOURCE_ID, getDynamicalRegionsLayer, regionsLayer } from './layers/regionsLayers';

const MAP_STYLE_URL = `${process.env.NEXT_PUBLIC_BASE_URL}/map-styles/map-style.json`;

// TODO: Respecter les conditions de réutilisation des données Etalab
// - Mentionner la source des données (Etalab)
// - Indiquer la date de mise à jour du fichier map-style.json
// - Vérifier et respecter la licence (Licence Ouverte 2.0 ou ODbL)

const initialViewState = {
	longitude: 1.888334,
	latitude: 46.603354,
	zoom: 5,
} satisfies MapPropsReactMapLibre['initialViewState'];

const style: React.CSSProperties = {
	width: 1200,
	height: 800,
};

const ANIMATION_TIME_MS = 800;

const COMMUNES_VISIBLE_ZOOM_THRESHOLD = 7;
const DEPARTEMENTS_VISIBLE_ZOOM_THRESHOLD = 5;

type EventFeature<Feature extends GeoJSON.Feature = GeoJSON.Feature> = Feature & {
	layer: LayerProps;
	source: string;
};

type EventRegionFeature = EventFeature<RegionFeature>;
type EventDepartementFeature = EventFeature<DepartementFeature>;
type EventCommunesFeature = EventFeature<CommuneFeature>;

type ClusterEtablissementFeature = EventFeature<
	ClusterFeature<EtablissementsGeoJSON['features'][number]['geometry']>
>;

/**
 * Type guard function that checks if the feature is from a layer
 * @param feature to check
 * @param layer the feature could be from
 * @returns
 */
function isFeatureFrom<T extends EventFeature>(
	feature: EventFeature | undefined,
	layer: LayerProps,
): feature is T {
	if (!feature) return false;

	return feature.layer.id === layer.id;
}

export default function FranceMap() {
	const mapRef = useRef<MapRef>(null);
	const [currentZoom, setCurrentZoom] = useState(initialViewState.zoom);

	const [codeRegion, setCodeRegion] = useState<string>();
	const [codeDepartement, setCodeDepartement] = useState<string>();
	const [codeCommune, setCodeCommune] = useState<string>();

	const { regionsGeoJSON } = useRegionsGeoJSON();
	const { departementsGeoJSON } = useDepartementsGeoJSON(
		codeRegion ?? null,
		codeRegion !== undefined,
	);
	const { communesGeoJSON } = useCommunesGeoJSON(
		codeDepartement ?? null,
		codeDepartement !== undefined,
	);

	const { etablissementsGeoJSON } = useEtablissementsGeoJSON(
		codeCommune ?? null,
		codeCommune !== undefined,
	);

	async function zoomOnCluster(feature: ClusterEtablissementFeature) {
		if (!mapRef.current) return;

		const clusterId = feature.properties.cluster_id;

		const geojsonSource = mapRef.current.getSource(ETABLISSEMENTS_SOURCE_ID) as GeoJSONSource;

		const zoom = await geojsonSource.getClusterExpansionZoom(clusterId);

		const { coordinates } = feature.geometry;

		if (coordinates.length !== 2) {
			throw new Error('The coordinates doesnt have a length of 2');
		}

		mapRef.current.easeTo({
			center: coordinates as LngLatLike,
			zoom,
			duration: ANIMATION_TIME_MS,
		});
	}

	function zoomOnFeature(feature: CommuneFeature | DepartementFeature | RegionFeature) {
		if (!mapRef.current) return;

		const [minLng, minLat, maxLng, maxLat] = bbox(feature);

		mapRef.current.fitBounds(
			[
				[minLng, minLat],
				[maxLng, maxLat],
			],
			{ padding: 40, duration: ANIMATION_TIME_MS },
		);
	}

	async function handleClickOnRegion(feature: RegionFeature) {
		zoomOnFeature(feature);

		setCodeRegion(feature.properties.code_region);
	}

	async function handleClickOnDepartement(feature: DepartementFeature) {
		zoomOnFeature(feature);

		setCodeDepartement(feature.properties.code_departement);
	}

	async function handleClickOnCommunes(feature: CommuneFeature) {
		zoomOnFeature(feature);

		setCodeCommune(feature.properties.code_commune);
	}

	async function onClick(event: MapMouseEvent) {
		if (!mapRef.current || !event.features) return;

		const feature = event.features[0] as unknown as EventFeature;

		if (isFeatureFrom<EventRegionFeature>(feature, regionsLayer)) {
			handleClickOnRegion(feature);

			return;
		}

		if (isFeatureFrom<EventDepartementFeature>(feature, departementsLayer)) {
			handleClickOnDepartement(feature);

			return;
		}

		if (isFeatureFrom<EventCommunesFeature>(feature, communesLayer)) {
			handleClickOnCommunes(feature);

			return;
		}

		if (isFeatureFrom<ClusterEtablissementFeature>(feature, clusterLayer)) {
			zoomOnCluster(feature);

			return;
		}
	}

	function handleZoom(event: ViewStateChangeEvent) {
		setCurrentZoom(event.viewState.zoom);
	}

	if (!clusterLayer.id || !regionsLayer.id || !departementsLayer.id || !communesLayer.id) {
		throw new Error('Layers not defined');
	}

	const isDepartementsLayerVisible =
		Boolean(codeRegion) && currentZoom > DEPARTEMENTS_VISIBLE_ZOOM_THRESHOLD;
	const isCommunesLayerVisible =
		Boolean(codeDepartement) && currentZoom > COMMUNES_VISIBLE_ZOOM_THRESHOLD;
	const isEtablissementsLayerVisible =
		Boolean(codeCommune) && currentZoom > COMMUNES_VISIBLE_ZOOM_THRESHOLD;

	return (
		<MapFromReactMapLibre
			ref={mapRef}
			initialViewState={initialViewState}
			mapStyle={MAP_STYLE_URL}
			interactiveLayerIds={[
				regionsLayer.id,
				departementsLayer.id,
				communesLayer.id,
				clusterLayer.id,
			]}
			style={style}
			onClick={onClick}
			onZoom={handleZoom}
		>
			{regionsGeoJSON && (
				<Source id={REGIONS_SOURCE_ID} type='geojson' data={regionsGeoJSON}>
					<Layer {...getDynamicalRegionsLayer(true)} />
				</Source>
			)}
			{departementsGeoJSON && (
				<Source id={DEPARTEMENTS_SOURCE_ID} type='geojson' data={departementsGeoJSON}>
					<Layer {...getDynamicalDepartementsLayer(isDepartementsLayerVisible)} />
				</Source>
			)}
			{communesGeoJSON && (
				<Source id={COMMUNES_SOURCE_ID} type='geojson' data={communesGeoJSON}>
					<Layer {...getDynamicalCommunesLayer(isCommunesLayerVisible)} />
				</Source>
			)}
			{etablissementsGeoJSON && (
				<Source
					id={ETABLISSEMENTS_SOURCE_ID}
					type='geojson'
					data={etablissementsGeoJSON}
					cluster={true}
					clusterMaxZoom={14}
					clusterRadius={50}
				>
					<Layer {...getDynamicalClusterLayer(isEtablissementsLayerVisible)} />
					<Layer {...getDynamicalClusterCountLayer(isEtablissementsLayerVisible)} />
					<Layer {...getDynamicalUnclusteredPointLayer(isEtablissementsLayerVisible)} />
				</Source>
			)}
		</MapFromReactMapLibre>
	);
}
