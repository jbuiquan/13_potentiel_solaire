const ACTION_TITLES: string[] = [
  "Je suis un élu et je veux agir",
  "Je suis un particulier et je veux agir"
];

const AccordionCard = () => {
  return (
    <div>
      {ACTION_TITLES.map((title: string, index: number) => (
        <details key={index} className="border p-2 mb-2 bg-blue text-white rounded-md">
          <summary className="cursor-pointer font-bold">{title}</summary>
          <br />
          <p>Lorem ipsum dolor sit amet consectetur. Aliquet bibendum vitae eget tempor velit sit laoreet sed. Nec sit mi urna aenean morbi.</p>
          <br />
          <ul>
            <li className="flex items-center space-x-2">
              <span className="w-1 h-1 bg-white rounded-full inline-block"></span>
              <p>Contacter votre élu pour lui demander d&apos;agir :</p>
            </li>
            <button className="bg-green text-darkgreen px-4 py-2 font-medium rounded-md w-full">
              Contacter par mail mon élu
            </button>
            <li className="flex items-center space-x-2">
              <span className="w-1 h-1 bg-white rounded-full inline-block"></span>
              <p className="mt-2">Signer la pétition pour demander la rénovation énergétique des bâtiments scolaires :</p>
            </li>
            <button className="bg-green text-darkgreen px-4 py-2 font-medium rounded-md w-full">
              Signez la pétition nationale
            </button>
          </ul>
          <br />
          <p className="mt-2">Découvrez les projets de transition énergétique près de chez vous :</p>
          <p className="text-green">- Carte de l&apos;énergie citoyenne</p>
        </details>
      ))}
    </div>
  );
};

export default AccordionCard;
