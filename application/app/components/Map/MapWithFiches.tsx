"use client";

import { useState } from "react";
import FranceMap from "./FranceMap";
import Fiches from "./fiches/Fiches";
import { EtablissementsGeoJSON } from "@/app/models/etablissements";

export default function MapWithFiches() {
  const [selectedEtablissement, setSelectedEtablissement] = useState<EtablissementsGeoJSON["features"][number] | null>(null);

  return (
    <>
      <FranceMap onSelect={setSelectedEtablissement} />
      {selectedEtablissement && (
        <Fiches
          etablissement={{
            ...selectedEtablissement.properties,
            longitude: selectedEtablissement.geometry.coordinates[0],
            latitude: selectedEtablissement.geometry.coordinates[1],
          }}
          onClose={() => setSelectedEtablissement(null)}
        />
      )}
    </>
  );
}
