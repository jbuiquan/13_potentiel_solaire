// import Link from 'next/link';
import { TopEtablissement } from '@/app/models/etablissements';
import * as Popover from '@radix-ui/react-popover';
import { Sun } from 'lucide-react';

const UNKNOWN_TEXTS = {
	top_etablissement: 'Aucun établissement mis en avant pour cette collectivité.',
};

const medals = ['🥇', '🥈', '🥉'];

type Props = {
	topEtablissements: TopEtablissement[] | null;
};

const TopCard = ({ topEtablissements }: Props) => {
	if (!topEtablissements || topEtablissements.length === 0) {
		return <p className='text-gray-500 italic'>{UNKNOWN_TEXTS.top_etablissement}</p>;
	}

	return (
		<div>
			<div className='flex gap-1 text-grey'>
				<Sun />
				<p>Top 3 potentiel solaire :</p>
			</div>
			<ul className='list-none space-y-1 pl-0 font-bold text-darkgreen'>
				{topEtablissements.slice(0, 3).map((etab, index) => (
					<li key={etab.id}>
						{medals[index]}{' '}
						<Popover.Root>
							<Popover.Trigger asChild>
								<span
									className='hover:bg-gray-100 rounded text-darkgreen transition'
									aria-disabled='true'
								>
									<span
										// href={/etablissements/${etab.id}}
										aria-disabled='true'
										className='underline decoration-dotted decoration-2 underline-offset-4 transition hover:text-primary'
									>
										{etab.libelle}
									</span>
								</span>
							</Popover.Trigger>
							<Popover.Portal>
								<Popover.Content
									className='z-50 rounded bg-blue px-3 py-1.5 text-xs text-white shadow'
									sideOffset={5}
								>
									Cette fonctionnalité n&apos;est pas encore disponible !
									<Popover.Arrow className='fill-black' />
								</Popover.Content>
							</Popover.Portal>
						</Popover.Root>
					</li>
				))}
			</ul>
		</div>
	);
};

export default TopCard;
