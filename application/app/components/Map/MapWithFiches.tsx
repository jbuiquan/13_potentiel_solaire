'use client';

import { Suspense } from 'react';

import useIsFicheOpen from '@/app/utils/hooks/useIsFicheOpen';
import useSelectedPlaces from '@/app/utils/hooks/useSelectedPlaces';
import { useMapFilter } from '@/app/utils/providers/mapFilterProvider';

import HomeOverlay from '../HomeOverlay/HomeOverlay';
import Fiches from '../fiches/Fiches';
import FranceMap from './FranceMap';

export default function MapWithFiches() {
	const { filterState } = useMapFilter();
	const { etablissement, commune, departement, region, isFetching } = useSelectedPlaces();
	const [isFicheOpen] = useIsFicheOpen();

	return (
		<div className='flex flex-1 flex-col'>
			<div className='relative flex-1'>
				<Suspense>
					<HomeOverlay />
					<FranceMap filters={filterState} />
				</Suspense>
			</div>
			{isFicheOpen && !isFetching && (
				<Fiches
					commune={commune ?? undefined}
					departement={departement ?? undefined}
					region={region ?? undefined}
					etablissement={etablissement ?? undefined}
				/>
			)}
		</div>
	);
}
