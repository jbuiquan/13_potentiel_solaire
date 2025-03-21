const baseURL = process.env.NEXT_PUBLIC_BASE_URL;

export default function getBaseURL() {
	console.log({ baseURL });
	if (baseURL === undefined) {
		throw new Error('Base URL is not defined, check your .env');
	}

	console.log({ baseURL });

	return baseURL;
}
