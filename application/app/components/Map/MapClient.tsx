'use client';

import { useCallback, useRef, useState } from 'react';

import type { LngLatLike, MapMouseEvent, MapRef } from '@vis.gl/react-maplibre';
import { Layer, Map as MapFromReactMapLibre, Popup, Source } from '@vis.gl/react-maplibre';
import { type GeoJSONSource } from 'maplibre-gl';

import { EtablissementsGeoJSON } from '../../models/etablissements';
import { ClusterFeature } from './interfaces';
import {
	ETABLISSEMENTS_SOURCE_ID,
	clusterCountLayer,
	clusterLayer,
	unclusteredPointLayer,
} from './layers';

const MAP_STYLE_URL = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

type HoverInfo = {
	longitude: number;
	latitude: number;
	name: string;
};

type ClusterEtablissementFeature = ClusterFeature<
	EtablissementsGeoJSON['features'][number]['geometry']
>;

type MapProps = {
	etablissements: EtablissementsGeoJSON;
};

export function MapClient({ etablissements }: MapProps) {
	const mapRef = useRef<MapRef>(null);
	const [hoverInfo, setHoverInfo] = useState<HoverInfo>();

	const onHover = useCallback((event: MapMouseEvent) => {
		console.log(event.features);
		const feature =
			event.features && (event.features[0] as unknown as ClusterEtablissementFeature);
		if (!feature) return;

		console.log(feature.properties);

		setHoverInfo({
			longitude: feature.geometry.coordinates[0],
			latitude: feature.geometry.coordinates[1],
			name: feature.properties.nom_etablissement,
		});
	}, []);

	const onLeave = useCallback(() => {
		setHoverInfo(undefined);
	}, []);

	const onClick = async (event: MapMouseEvent) => {
		console.log(event);
		if (!mapRef.current) return;

		const feature =
			event.features && (event.features[0] as unknown as ClusterEtablissementFeature);
		if (!feature) return;
		console.log(feature);
		const clusterId = feature.properties.cluster_id;

		const geojsonSource = mapRef.current.getSource('etablissements') as GeoJSONSource;

		const zoom = await geojsonSource.getClusterExpansionZoom(clusterId);

		const { coordinates } = feature.geometry;

		if (coordinates.length !== 2) {
			throw new Error('The coordinates doesnt have a length of 2');
		}

		mapRef.current.easeTo({
			center: coordinates as LngLatLike,
			zoom,
			duration: 500,
		});
	};

	if (!clusterLayer.id) {
		throw new Error('Layer not defined');
	}

	const hoveredFeature = (hoverInfo && hoverInfo.name) || '';

	return (
		<>
			<MapFromReactMapLibre
				style={{ width: 600, height: 600 }}
				initialViewState={{
					latitude: 40.67,
					longitude: -103.59,
					zoom: 3,
				}}
				mapStyle={MAP_STYLE_URL}
				interactiveLayerIds={[clusterLayer.id]}
				onClick={onClick}
				onMouseMove={onHover}
				onMouseLeave={onLeave}
				ref={mapRef}
			>
				<Source
					id={ETABLISSEMENTS_SOURCE_ID}
					type='geojson'
					data={etablissements}
					cluster={true}
					clusterMaxZoom={14}
					clusterRadius={50}
				>
					<Layer {...clusterLayer} />
					<Layer {...clusterCountLayer} />
					<Layer {...unclusteredPointLayer} />
				</Source>
				{hoverInfo && (
					<Popup
						longitude={hoverInfo?.longitude}
						latitude={hoverInfo?.latitude}
						offset={[0, -10] as [number, number]}
						closeButton={false}
					>
						{hoveredFeature}
					</Popup>
				)}
			</MapFromReactMapLibre>
		</>
	);
}
