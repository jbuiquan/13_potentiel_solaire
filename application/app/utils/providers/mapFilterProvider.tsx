'use client';

import { Dispatch, ReactNode, SetStateAction, createContext, useContext, useState } from 'react';

import { TypeEtablissement } from '@/app/models/etablissements';

export type FilterState = Record<TypeEtablissement | 'All', boolean>;

const initialState: FilterState = {
	Lycée: true,
	Collège: true,
	Ecole: true,
	All: true,
};

export interface MapFilterContextType {
	filterState: FilterState;
	setFilterState: Dispatch<SetStateAction<FilterState>>;
}

export const MapFilterContext = createContext<MapFilterContextType | undefined>(undefined);

export const MapFilterProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
	const [filterState, setFilterState] = useState(initialState);

	// const setNextState = useCallback(
	// 	([key, checked]: [keyof FilterState, boolean]) => {
	// 		setFilterState(getNextState(filterState, [key, checked]));
	// 	},
	// 	[filterState, setFilterState],
	// );

	return (
		<MapFilterContext.Provider value={{ filterState, setFilterState }}>
			{children}
		</MapFilterContext.Provider>
	);
};

export function useMapFilter() {
	const context = useContext(MapFilterContext);
	if (context === undefined) {
		throw new Error('useMapFilter must be used with a MapFilterProvider');
	}
	return context;
}
