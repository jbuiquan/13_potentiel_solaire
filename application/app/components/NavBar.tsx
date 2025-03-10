import Link from 'next/link';

const links = [
	{
		title: 'Accueil',
		href: '/',
	},
	{
		title: 'Source & méthodologie',
		href: '/source_methodology',
	},
	{
		title: 'A propos',
		href: '/about',
	},
];

export function NavBar() {
	return (
		<nav className='sticky top-0 z-50 bg-yellow-600'>
			<div className='mx-auto flex max-w-screen-xl items-center justify-between p-4'>
				<Link href='/'>
					<div className='text-2xl font-semibold'>Potentiel Solaire</div>
				</Link>
				<ul className='mt-4 flex flex-col p-4 font-medium md:mt-0 md:flex-row md:space-x-8 md:p-0'>
					{links.map((link) => (
						<li key={link.href}>
							<Link href={link.href} className='block px-3 py-2 md:p-0'>
								{link.title}
							</Link>
						</li>
					))}
				</ul>
			</div>
		</nav>
	);
}
