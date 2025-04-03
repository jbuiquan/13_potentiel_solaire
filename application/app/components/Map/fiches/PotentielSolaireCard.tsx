import { Zap, HousePlug, CircleHelp } from "lucide-react";

const UNKNOWN_TEXTS = {
  potentiel_solaire: "ND",
};

const SOLAR_TEXT = {
  high: "Le potentiel solaire de cet établissement me paraît tout à fait rayonnant",
  low: "Des optimisations sont à prévoir pour un bon potentiel solaire",
};

interface PotentielSolaireCardProps {
  potentiel_solaire?: number;
}

const PotentielSolaireCard = ({ potentiel_solaire }: PotentielSolaireCardProps) => {
  const isHigh = (potentiel_solaire ?? 0) > 500000;

  return (
    <div className="p-2 mb-4 bg-gray-100 rounded-2xl">
      {/* Indicateur de potentiel solaire */}
      <div className={isHigh ? "bg-green rounded-xl p-5" : "bg-yellow rounded-xl p-5"}>
        <p className="font-normal">{isHigh ? SOLAR_TEXT.high : SOLAR_TEXT.low}</p>
      </div>
      <br />

      {/* Production annuelle */}
      <div className="flex gap-1">
        <Zap />
        <p className="font-medium">Potentiel de production annuelle :</p>
      </div>
      <p className="font-medium">
        &nbsp;🟡 &nbsp;&nbsp;
        <span className="text-xl">
          {potentiel_solaire !== undefined ? Math.round(potentiel_solaire / 1000) : UNKNOWN_TEXTS.potentiel_solaire}
        </span>{" "}
        MWh/an
      </p>

      {/* Équivalence en foyers */}
      <div className="flex gap-1">
        <HousePlug />
        <p className="font-medium">Équivalent à la consommation électrique annuelle de :</p>
      </div>
      <div className="flex items-center justify-between w-full ps-7 text-darkgreen">
        <div className="flex items-center gap-2">
          <span className="text-2xl font-medium text-darkgreen">
            {potentiel_solaire !== undefined ? Math.round(potentiel_solaire / 2300 / 4) : UNKNOWN_TEXTS.potentiel_solaire}
          </span>
          <div className="flex flex-col text-sm leading-tight">
            <span className="font-medium">foyers de</span>
            <span className="font-medium">4 personnes</span>
          </div>
        </div>
        <CircleHelp />
      </div>
    </div>
  );
};

export default PotentielSolaireCard;
