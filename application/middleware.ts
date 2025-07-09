import { NextRequest, NextResponse } from 'next/server';

import { fetchEtablissement } from './app/utils/fetchers/fetchEtablissement';
import { buildActiveTabParam, buildCodesParam } from './app/utils/state-utils';

export async function middleware(request: NextRequest) {
	const [, , idFromPath] = request.nextUrl.pathname.split('/');

	if (!idFromPath) {
		return NextResponse.next();
	}

	try {
// In Next.js middleware, the code runs on the Edge Runtime, which does not have access to the app's internal API routes via relative URLs, we have to pass the origin
		const etablissement = await fetchEtablissement(idFromPath, request.nextUrl.origin);
		if (etablissement) {
			const { code_region, code_departement, code_commune } = etablissement;
			const codesParams = buildCodesParam({
				codeRegion: code_region,
				codeDepartement: code_departement,
				codeCommune: code_commune,
				codeEtablissement: idFromPath,
			});
			const activeTabParam = buildActiveTabParam('etablissement');
			return NextResponse.redirect(
				new URL(`/?${codesParams.toString()}&${activeTabParam.toString()}`, request.url),
			);
		}
	} catch (e) {
		console.error('Error while fetching etablissement:', e);
		return NextResponse.next();
	}
}

export const config = {
	matcher: ['/etablissement/:path'],
};
