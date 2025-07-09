'use client';

import { Suspense } from 'react';

import useActiveTab from '@/app/utils/hooks/useActiveTab';
import useSelectedPlaces from '@/app/utils/hooks/useSelectedPlaces';

import HomeOverlay from '../HomeOverlay/HomeOverlay';
import Fiches from '../fiches/Fiches';
import FranceMap from './FranceMap';

export default function MapWithFiches() {
	const { etablissement, commune, departement, region, isFetching } = useSelectedPlaces();
	const [isFicheOpen] = useActiveTab();

	return (
		<div className='flex flex-1 flex-col'>
			<div className='relative flex-1'>
				<Suspense>
					<HomeOverlay />
					<FranceMap />
				</Suspense>
			</div>
			{isFicheOpen && (
				<Fiches
					commune={commune ?? undefined}
					departement={departement ?? undefined}
					region={region ?? undefined}
					etablissement={etablissement ?? undefined}
					isFetching={isFetching}
				/>
			)}
		</div>
	);
}
