// import Link from 'next/link';
import { TopEtablissement } from '@/app/models/etablissements';
import * as Tooltip from '@radix-ui/react-tooltip';
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
						<Tooltip.Provider>
							<Tooltip.Root>
								<Tooltip.Trigger asChild>
									<button
										className='hover:bg-gray-100 rounded p-2 text-darkgreen transition'
										disabled
									>
										<span
											// href={`/etablissements/${etab.id}`}
											aria-disabled='true'
											className='underline decoration-dotted decoration-2 underline-offset-4 transition hover:text-primary'
										>
											{etab.libelle}
										</span>
									</button>
								</Tooltip.Trigger>
								<Tooltip.Portal>
									<Tooltip.Content
										className='z-50 rounded bg-blue px-3 py-1.5 text-xs text-white shadow'
										sideOffset={5}
									>
										Cette fonctionnalité n&apos;est pas encore disponible !
										<Tooltip.Arrow className='fill-black' />
									</Tooltip.Content>
								</Tooltip.Portal>
							</Tooltip.Root>
						</Tooltip.Provider>
					</li>
				))}
			</ul>
		</div>
	);
};

export default TopCard;
