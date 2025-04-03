const UNKNOWN_TEXTS = {
  name: "Nom inconnu",
  adresse: "Adresse inconnue",
  nb_eleves: "Nombre d'élèves concernés inconnus",
};

interface EtablissementCardProps {
  nom_etablissement?: string;
  adresse_1?: string | null;
  adresse_2?: string | null;
  adresse_3?: string | null;
  nb_eleves?: number | null;
}

const EtablissementCard = ({
  nom_etablissement,
  adresse_1,
  adresse_2,
  adresse_3,
  nb_eleves,
}: EtablissementCardProps) => {
  return (
    <div>
      <h1 className="font-bold text-2xl">{nom_etablissement || UNKNOWN_TEXTS.name}</h1>
      <p>{adresse_1 || UNKNOWN_TEXTS.adresse}</p>
      <p>{adresse_2 || ""}</p>
      <p>{adresse_3 || ""}</p>

      <br />
      <p>
        {nb_eleves !== null && nb_eleves !== undefined ? (
          <>
            <span className="text-xl">{nb_eleves}</span> élèves concernés
          </>
        ) : (
          UNKNOWN_TEXTS.nb_eleves
        )}
      </p>
    </div>
  );
};

export default EtablissementCard;
