'use client';

import { useCallback, useMemo } from 'react';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';

import { TabId } from '@/app/components/fiches/Fiches';
import { ACTIVE_TAB_KEY } from '../state-utils';


export type Codes = {
	codeRegion: string | null;
	codeDepartement: string | null;
	codeCommune: string | null;
	codeEtablissement: string | null;
};

type SetCode = (key: keyof Codes, code: string | null, activeTab?: TabId | null) => void;
type SetCodes = (codes: Codes, activeTab?: TabId | null) => void;

type ReturnType = {
	values: Codes;
	setCode: SetCode;
	setCodes: SetCodes;
	reset: () => void;
};

export default function useURLParams(): ReturnType {
	const searchParams = useSearchParams();
	const router = useRouter();
	const pathname = usePathname();

	const setCode: SetCode = useCallback(
		(key, code, activeTab) => {
			const newParams = new URLSearchParams(searchParams);

			if (code === null) {
				newParams.delete(key);
			} else {
				newParams.set(key, code.toString());
			}

			if (activeTab) {
				newParams.set(ACTIVE_TAB_KEY, activeTab.toString());
			} else {
				newParams.delete(ACTIVE_TAB_KEY);
			}

			router.push(`${pathname}?${newParams.toString()}`);
		},
		[pathname, router, searchParams],
	);

	const setCodes: SetCodes = useCallback(
		(codes, activeTab) => {
			const newParams = new URLSearchParams();

			const keys = Object.keys(codes) as unknown as (keyof Codes)[];

			keys.forEach((key) => {
				const code = codes[key];
				if (code === null) {
					newParams.delete(key);

					return;
				}
				newParams.set(key, code.toString());
			});

			if (activeTab) {
				newParams.set(ACTIVE_TAB_KEY, activeTab.toString());
			} else {
				newParams.delete(ACTIVE_TAB_KEY);
			}

			router.push(`${pathname}?${newParams.toString()}`);
		},
		[pathname, router],
	);

	const reset = useCallback(() => {
		router.push(pathname);
	}, [pathname, router]);

	const codeRegion = searchParams.get('codeRegion');
	const codeDepartement = searchParams.get('codeDepartement');
	const codeCommune = searchParams.get('codeCommune');
	const codeEtablissement = searchParams.get('codeEtablissement');

	// avoid creation of new object reference if values do not change (causing re-run of an effect if used as dependency)
	const values = useMemo(
		() => ({
			codeRegion,
			codeDepartement,
			codeCommune,
			codeEtablissement,
		}),
		[codeRegion, codeDepartement, codeCommune, codeEtablissement],
	);

	return { values, setCode, setCodes, reset };
}
