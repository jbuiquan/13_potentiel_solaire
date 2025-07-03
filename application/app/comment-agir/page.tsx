'use client';

import StaticPage from '../components/StaticPage';
import {
	ELU_BODY,
	ELU_INTRO_LONG,
	PARTICULIER_BODY,
	PARTICULIER_INTRO_LONG,
} from '../components/content/accordion-actions';
import commentAgirContent from '../components/content/comment-agir';
import AccordionCard from '../components/fiches/shared/AccordionCard';

const actionsLong = [
	{
		title: 'Je suis un élu et je veux agir',
		content: (
			<>
				{ELU_INTRO_LONG}
				{ELU_BODY}
			</>
		),
	},
	{
		title: 'Je suis un particulier et je veux agir',
		content: (
			<>
				{PARTICULIER_INTRO_LONG}
				{PARTICULIER_BODY}
			</>
		),
	},
];

export default function CommentAgirPage() {
	return (
		<>
			<StaticPage {...commentAgirContent} />
			<AccordionCard actions={actionsLong} />
      <div className="h-32" />
		</>
	);
}
