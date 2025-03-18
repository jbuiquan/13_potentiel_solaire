import MapWithLoader from './components/Map/MapWithLoader';

export default function Home() {
	return (
		<div className='mx-auto flex max-w-screen-xl items-center justify-around'>
			<MapWithLoader />
		</div>
	);
}
