interface Etablissement {
  nom_etablissement?: string;
  adresse_1?: string | null;
  adresse_2?: string | null;
  adresse_3?: string | null;
  nb_eleves?: number | null;
  protection?: boolean;
  potentiel_solaire?: number;
  surface_utile?: number;
}

interface FicheEtablissementProps {
  feature: Etablissement;
  onClose: () => void;
}


export default function FicheEtablissement({ feature }: FicheEtablissementProps) {
  if (!feature) return null;

  return (
    <div>
      <h1 className="font-bold text-2xl">{feature.nom_etablissement || "Nom inconnu"}</h1>
      <p>{feature.adresse_1 || "Adresse inconnue"}</p>
      <p>{feature.adresse_2 || ""}</p>
      <p>{feature.adresse_3 || ""}</p>

      <br />
      <p>
        {feature.nb_eleves ? (
          <>
            <span className="text-xl">{feature.nb_eleves}</span> élèves concernés
          </>
        ) : (
          `Nombre d'élèves concernés inconnu`
        )}
      </p>
      <br />
      <div className="flex gap-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path fill="currentColor" d="M15.815 0C17.575 0 19 1.45 19 3.235s-1.424 3.234-3.185 3.234a3.155 3.155 0 0 1-2.378-1.084l-6.284 3.44c.14.364.216.76.216 1.175c0 .542-.13 1.052-.363 1.501l6.008 3.725a3.177 3.177 0 0 1 2.801-1.695c1.76 0 3.185 1.45 3.185 3.234C19 18.55 17.576 20 15.815 20c-1.76 0-3.184-1.45-3.184-3.235l.003-.138l-6.53-4.046a3.138 3.138 0 0 1-1.92.654C2.425 13.235 1 11.785 1 10s1.424-3.235 3.185-3.235c.852 0 1.626.34 2.197.893l6.382-3.493a3.282 3.282 0 0 1-.133-.93C12.63 1.45 14.055 0 15.815 0Zm0 14.926c-.992 0-1.8.822-1.8 1.84c0 1.017.808 1.839 1.8 1.839c.993 0 1.8-.822 1.8-1.84c0-1.017-.807-1.839-1.8-1.839ZM4.185 8.161c-.993 0-1.8.822-1.8 1.839s.807 1.84 1.8 1.84c.992 0 1.8-.823 1.8-1.84c0-1.017-.808-1.84-1.8-1.84Zm11.63-6.766c-.992 0-1.8.822-1.8 1.84c0 1.017.808 1.839 1.8 1.839c.993 0 1.8-.822 1.8-1.84c0-1.017-.807-1.839-1.8-1.839Z"/></svg>
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 32 32"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 22V5M9 16l7 7l7-7M9 27h14"/></svg>
      </div>

      <hr className="my-4" />

      {/* Protection Card */}
      <div className={`flex gap-4 p-2 mb-4 ${feature.protection ? "bg-orange rounded-md" : "bg-green rounded-md"}`}>
      <svg xmlns="http://www.w3.org/2000/svg" className="pt-3" width="30" height="30" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 64a448 448 0 1 1 0 896a448 448 0 0 1 0-896zm0 832a384 384 0 0 0 0-768a384 384 0 0 0 0 768zm48-176a48 48 0 1 1-96 0a48 48 0 0 1 96 0zm-48-464a32 32 0 0 1 32 32v288a32 32 0 0 1-64 0V288a32 32 0 0 1 32-32z"/></svg>
        <p className="font-normal">
          {feature.protection
            ? "Une partie de cet établissement est située en zone protégée"
            : "Pas de zone protégée"}
        </p>
      </div>

      {/* Potentiel Solaire Card */}
      <div className="p-2 mb-4 bg-gray-100 rounded-2xl">
        <div className={feature.potentiel_solaire && feature.potentiel_solaire > 500000 ? "bg-green rounded-xl p-5" : "bg-yellow rounded-xl p-5"}>
          <p className="font-normal">
            {feature.potentiel_solaire && feature.potentiel_solaire > 500000
              ? "Le potentiel solaire de cet établissement me parait tout à-fait rayonnant"
              : "Des optimisations sont à prévoir pour un bon potentiel solaire"}
          </p>
        </div>
        <br />
        <div className="flex gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 14 14"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M11.5 5.031a4.5 4.5 0 1 0-6.5 4v1.5a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-1.5a4.48 4.48 0 0 0 2.5-4M5 13.5h4"/></svg>
          <p className="font-medium">Potentiel de production annuelle :</p>
        </div>
        <p className="font-medium">
        &nbsp;🟡 &nbsp;&nbsp;<span className="text-xl">
            {feature.potentiel_solaire !== undefined ? Math.round(feature.potentiel_solaire / 1000) : "ND"}
          </span> MWh/an
        </p>
        <div className="flex gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m15 11l-4 4l-2-2m-5 3.8v-5.348c0-.534 0-.801.065-1.05a2 2 0 0 1 .28-.617c.145-.213.346-.39.748-.741l4.801-4.202c.746-.652 1.119-.978 1.538-1.102c.37-.11.765-.11 1.135 0c.42.124.794.45 1.54 1.104l4.8 4.2c.403.352.603.528.748.74c.127.19.222.398.28.618c.065.249.065.516.065 1.05v5.352c0 1.118 0 1.677-.218 2.105a2 2 0 0 1-.875.873c-.427.218-.986.218-2.104.218H7.197c-1.118 0-1.678 0-2.105-.218a1.999 1.999 0 0 1-.874-.873C4 18.48 4 17.92 4 16.8Z"/></svg>
          <p className="font-medium">Equivalent à la consommation électrique annuelle de :</p>
        </div>
        <div className="flex items-center justify-between w-full ps-5 text-darkgreen">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-medium text-darkgreen">
              &nbsp;{feature.potentiel_solaire !== undefined ? Math.round(feature.potentiel_solaire / 2300 / 4) : "ND"}
            </span>
            <div className="flex flex-col text-sm leading-tight">
              <span className="font-medium">foyers de</span>
              <span className="font-medium">4 personnes</span>
            </div>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 32 32">
            <path fill="currentColor" d="M16 1.466C7.973 1.466 1.466 7.973 1.466 16c0 8.027 6.507 14.534 14.534 14.534c8.027 0 14.534-6.507 14.534-14.534c0-8.027-6.507-14.534-14.534-14.534zm1.328 22.905H14.62v-2.595h2.708v2.596zm0-5.367v.858H14.62v-1.056c0-3.19 3.63-3.696 3.63-5.963c0-1.033-.923-1.825-2.133-1.825c-1.254 0-2.354.924-2.354.924l-1.54-1.916S13.74 8.44 16.358 8.44c2.486 0 4.795 1.54 4.795 4.136c0 3.632-3.827 4.05-3.827 6.427z"/>
          </svg>
        </div>
      </div>

      <hr className="my-4" />
      <div className="ml-2">
        <div className="flex gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><g fill="none"><path d="M24 0v24H0V0h24ZM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035c-.01-.004-.019-.001-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427c-.002-.01-.009-.017-.017-.018Zm.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093c.012.004.023 0 .029-.008l.004-.014l-.034-.614c-.003-.012-.01-.02-.02-.022Zm-.715.002a.023.023 0 0 0-.027.006l-.006.014l-.034.614c0 .012.007.02.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01l-.184-.092Z"/><path fill="currentColor" d="M13 3a2 2 0 0 1 1.995 1.85L15 5v4h3a2 2 0 0 1 1.995 1.85L20 11v8h1a1 1 0 0 1 .117 1.993L21 21H3a1 1 0 0 1-.117-1.993L3 19h1V5a2 2 0 0 1 1.85-1.995L6 3h7Zm5 8h-3v8h3v-8Zm-5-6H6v14h7V5Zm-2 10v2H8v-2h3Zm0-4v2H8v-2h3Zm0-4v2H8V7h3Z"/></g></svg>
          <p className="font-medium">Superficie exploitable maximale: </p>
        </div>
        <p className="font-medium text-center">
          <span className="text-xl">{feature.surface_utile || "Non disponible"} </span> M²
        </p>

        {/* Placeholder for Graph */}
        <div className="flex  gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="M12 21.5a9.5 9.5 0 1 0 0-19a9.5 9.5 0 0 0 0 19"/><path d="M12 2.5V12l6.721-6.721"/></g></svg>
          <p className="font-medium">Estimation des revenus mensuels maximaux de l&apos;installation</p>
        </div>
        <div className="h-40 bg-gray-300 flex items-center justify-center my-4">Graphique ici</div>
      </div>

      {/* Accordions */}
      <hr className="my-4" />
      {["Je suis un élu et je veux agir", "Je suis un particulier et je veux agir"].map((title, index) => (
        <details key={index} className="border p-2 mb-2 bg-blue text-white rounded-md">
          <br />
          <summary className="cursor-pointer font-bold">{title} </summary>
          <p>Lorem ipsum dolor sit amet consectetur. Aliquet bibendum vitae eget tempor velit sit laoreet sed. Nec sit mi urna aenean morbi.</p>
          <br />
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
          <br />
          <p className="mt-2">Découvrez les projet de transition énergétique près de chez vous :</p>
          <p className="text-green">- Carte de l&apos;énergie citoyenne</p>
        </details>
      ))}
    </div>
  );
}
