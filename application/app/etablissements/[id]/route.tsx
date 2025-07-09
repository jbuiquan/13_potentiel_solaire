import { NextRequest, NextResponse } from 'next/server';

import { fetchEtablissement } from '@/app/utils/fetchers/fetchEtablissement';
import { buildActiveTabParam, buildCodesParam } from '@/app/utils/state-utils';

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
	const { id } = await params;

	try {
		// In Next.js, this code runs on the Edge Runtime, which does not have access to the app's internal API routes via relative URLs, we have to pass the origin
		const etablissement = await fetchEtablissement(id, request.nextUrl.origin);
		if (etablissement) {
			const { code_region, code_departement, code_commune } = etablissement;
			const codesParams = buildCodesParam({
				codeRegion: code_region,
				codeDepartement: code_departement,
				codeCommune: code_commune,
				codeEtablissement: id,
			});
			const activeTabParam = buildActiveTabParam('etablissement');
			return NextResponse.redirect(
				new URL(
					`/?${codesParams.toString()}&${activeTabParam.toString()}`,
					request.nextUrl.origin,
				),
			);
		}
	} catch (e) {
		console.error('Error while fetching etablissement:', e);
		return NextResponse.error();
	}
}
