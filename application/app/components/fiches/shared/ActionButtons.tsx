'use client';

import { toast } from '@/hooks/use-toast';
import * as Tooltip from '@radix-ui/react-tooltip';
import { Download, Share2 } from 'lucide-react';

const ActionButtons = () => {
	const handleShare = async () => {
		const url = window.location.href;

		if (navigator.share) {
			try {
				await navigator.share({
					title: document.title,
					url,
				});
			} catch (err: unknown) {
				if (
					err instanceof DOMException &&
					(err.name === 'AbortError' ||
						err.message?.includes('cancelled') ||
						err.message?.includes('aborted'))
				) {
					console.info('Partage annulé par l’utilisateur.');
				} else {
					console.error('Erreur lors du partage :', err);
					toast({
						title: 'Le partage a échoué',
						variant: 'destructive',
					});
				}
			}
		} else {
			try {
				await navigator.clipboard.writeText(url);
				toast({
					title: 'Lien copié dans le presse-papiers !',
				});
			} catch (err) {
				console.error('Erreur lors de la copie du lien :', err);
				toast({
					title: 'Impossible de copier le lien',
					variant: 'destructive',
				});
			}
		}
	};

	return (
		<div className='flex gap-4'>
			<button
				onClick={handleShare}
				title='Partager'
				className='hover:bg-gray-100 rounded p-2 text-darkgreen transition'
			>
				<Share2 className='h-5 w-5' />
			</button>
			<Tooltip.Provider>
				<Tooltip.Root>
					<Tooltip.Trigger asChild>
						<button
							className='hover:bg-gray-100 rounded p-2 text-darkgreen transition'
							disabled
						>
							<Download />
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
		</div>
	);
};

export default ActionButtons;
