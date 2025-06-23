'use client';

import * as React from 'react';
import { useEffect, useState } from 'react';

import { FilterState, useMapFilter } from '@/app/utils/providers/mapFilterProvider';
import { Button } from '@/components/ui/button';
import { DropdownMenuCheckboxItem } from '@/components/ui/dropdown-menu';
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuTrigger,
} from '@radix-ui/react-dropdown-menu';
import { ListFilter } from 'lucide-react';

const FILTERS_LABEL: Record<keyof FilterState, string> = {
	Lycée: 'Lycées',
	Collège: 'Collèges',
	Ecole: 'Écoles',
	All: 'Tous',
};

const getNextState = (
	prevState: FilterState,
	[key, checked]: [keyof FilterState, boolean],
): FilterState => {
	if (key === 'All') {
		if (!checked) return prevState;
		return {
			Lycée: checked,
			Collège: checked,
			Ecole: checked,
			All: checked,
		};
	}
	const nextState = { ...prevState, [key]: checked };
	const stateArrayWithoutAll = Object.entries(nextState).filter(([key]) => key !== 'All');
	const allChecked = stateArrayWithoutAll.every(([, value]) => value === true);
	return { ...nextState, All: allChecked };
};

const Filters: React.FC = () => {
	const { filterState, setFilterState } = useMapFilter();

	// Local state to stage changes
	const [stagedState, setStagedState] = useState<FilterState>(filterState);
	const [open, setOpen] = useState(false);

	// Sync staged state with global state when dropdown opens
	useEffect(() => {
		if (open) setStagedState(filterState);
	}, [open, filterState]);

	function onCheckedChange(key: keyof FilterState, checked: boolean) {
		setStagedState((prev) => getNextState(prev, [key, checked]));
	}

	const stateArrayWithoutAll = Object.entries(stagedState).filter(([key]) => key !== 'All');
	const allChecked = stateArrayWithoutAll.every(([, value]) => value === true);
	const lastChecked = stateArrayWithoutAll.filter(([, value]) => value === true).length === 1;

	function handleValidate() {
		setFilterState(() => stagedState);
		setOpen(false);
	}

	function handleCancel() {
		setStagedState(filterState);
		setOpen(false);
	}

	// Indicator logic: true if any filter except "All" is active
	const filtersOn =
		Object.entries(filterState).filter(([key, value]) => key !== 'All' && value === true)
			.length < 3;

	return (
		<DropdownMenu open={open} onOpenChange={setOpen}>
			<DropdownMenuTrigger asChild>
				<div className='relative flex flex-col items-center'>
					{filtersOn && (
						<span
							className='absolute right-1 top-1 z-10 h-2 w-2 rounded-full border border-white bg-amber-600'
							aria-label='Filtres actifs'
						/>
					)}
					{/* TODO: add proper colors */}
					<Button variant='ghost' className='bg-inherit hover:bg-black'>
						<ListFilter className='shrink-0 stroke-green' size={24} />
					</Button>
				</div>
			</DropdownMenuTrigger>
			<DropdownMenuContent className='w-56 rounded-sm border-2 border-white bg-blue text-white'>
				{(Object.keys(stagedState) as (keyof FilterState)[]).map((key) => (
					<DropdownMenuCheckboxItem
						className='cursor-pointer rounded-none'
						key={key}
						checked={stagedState[key]}
						onCheckedChange={onCheckedChange.bind(null, key)}
						onSelect={(e) => e.preventDefault()}
						disabled={
							(key === 'All' && allChecked) ||
							(key !== 'All' && lastChecked && stagedState[key] === true)
						}
					>
						{FILTERS_LABEL[key]}
					</DropdownMenuCheckboxItem>
				))}
				{/* FIXME: (a11y) :buttons should be focusable + aria (x filters applied aria-live message ?)*/}
				<div className='my-2 flex justify-center gap-2 px-2'>
					<Button
						size='sm'
						variant='outline'
						onClick={handleCancel}
						className='border-white text-blue hover:text-blue'
					>
						Annuler
					</Button>
					<Button size='sm' variant='default' onClick={handleValidate}>
						Valider
					</Button>
				</div>
			</DropdownMenuContent>
		</DropdownMenu>
	);
};

export default Filters;
