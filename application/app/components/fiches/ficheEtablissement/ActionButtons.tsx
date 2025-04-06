'use client';

import { useCallback } from 'react';

import { Download, Share2 } from 'lucide-react';
import { toast } from 'sonner';

const ActionButtons = () => {
	const handleShare = useCallback(async () => {
		const url = window.location.href;

		if (navigator.share) {
			try {
				await navigator.share({
					title: document.title,
					url,
				});
			} catch (err) {
				console.error('Erreur lors du partage :', err);
			}
		} else {
			try {
				await navigator.clipboard.writeText(url);
				toast.success('Lien copié dans le presse-papiers !');
			} catch (err) {
				console.error('Erreur lors de la copie du lien :', err);
				toast.error('Impossible de copier le lien');
			}
		}
	}, []);

	return (
		<div className='flex gap-4'>
			<button
				onClick={handleShare}
				title='Partager'
				className='rounded p-2 text-darkgreen transition hover:bg-gray-100'
			>
				<Share2 className='h-5 w-5' />
			</button>
			<button className='rounded p-2 text-darkgreen transition hover:bg-gray-100'>
				<Download />
			</button>
		</div>
	);
};

export default ActionButtons;
