'use client';

import { useCallback } from 'react';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';

import { TabId } from '@/app/components/fiches/Fiches';
import { ACTIVE_TAB_KEY } from '../state-utils';

type SetActiveFicheTab = (value: TabId | null) => void;

type ReturnType = [boolean, TabId | null, SetActiveFicheTab];

export default function useActiveTab(): ReturnType {
	const searchParams = useSearchParams();
	const router = useRouter();
	const pathname = usePathname();

	const setActiveTab: SetActiveFicheTab = useCallback(
		(value) => {
			const newParams = new URLSearchParams(searchParams);

			if (value) {
				newParams.set(ACTIVE_TAB_KEY, value.toString());
			} else {
				newParams.delete(ACTIVE_TAB_KEY);
			}

			router.push(`${pathname}?${newParams.toString()}`);
		},
		[pathname, router, searchParams],
	);

	const activeTab = searchParams.get(ACTIVE_TAB_KEY) as TabId | null;
	const isFicheOpen = activeTab !== null;

	return [isFicheOpen, activeTab, setActiveTab];
}
