import { NextRequest } from 'next/server';

import { fetchRegionsGeoJSON } from '@/app/lib/data';

/**
 * Get regions.
 * Get every regions if no codeRegion is provided.
 * @param request
 * @returns
 */
export async function GET(request: NextRequest) {
	const searchParams = request.nextUrl.searchParams;
	const codeRegion = searchParams.get('codeRegion');
	try {
		const data = await fetchRegionsGeoJSON(codeRegion);
		return Response.json(data, {
			status: 200,
		});
	} catch (error) {
		console.error('Error while retrieving data:', error);
		return Response.json({ error }, { status: 500 });
	}
}
