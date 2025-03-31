import { useState } from "react";
import FicheEtablissement from "./ficheEtablissement";

interface Etablissement {
  properties: EtablissementProperties;
}

interface EtablissementProperties {
  nom_etablissement?: string;
  adresse_1?: string | null;
  adresse_2?: string | null;
  adresse_3?: string | null;
  nb_eleves?: number | null;
  protection?: boolean;
  potentiel_solaire?: number;
  surface_utile?: number;
}

interface FichesProps {
  etablissement?: Etablissement;
  onClose: () => void;
}

export default function Fiches({ etablissement, onClose }: FichesProps) {
  const [activeTab, setActiveTab] = useState<string>("etablissement");

  if (!etablissement) return null;

  const tabs = [
    { id: "region", label: "Région" },
    { id: "departement", label: "Département" },
    { id: "commune", label: "Commune" },
    { id: "etablissement", label: "Établissement" },
  ];

  return (
    <div className="fixed right-0 top-0 w-full max-w-sm md:w-96 h-full bg-white shadow-lg overflow-y-auto pt-1 pl-5 z-50">
      <button
        onClick={onClose}
        className="absolute top-4 left-1 text-xl text-gray-500 hover:text-black"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 304 384"><path fill="currentColor" d="M299 73L179 192l120 119l-30 30l-120-119L30 341L0 311l119-119L0 73l30-30l119 119L269 43z"/></svg>
      </button>

      <div className="flex border-b pl-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`w-1/4 py-2 px-4 text-sm md:text-base truncate rounded-md ${activeTab === tab.id ? "bg-gray-500 text-green font-bold" : "bg-green text-gray-500"}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="p-4">
        {activeTab === "region" && <div>Contenu onglet région</div>}
        {activeTab === "departement" && <div>Contenu onglet département</div>}
        {activeTab === "commune" && <div>Contenu onglet commune</div>}
        {activeTab === "etablissement" && <FicheEtablissement feature={etablissement.properties} onClose={onClose} />}
      </div>
    </div>
  );
}
