import { Ruler, ChartPie } from "lucide-react"

const UNKNOWN_TEXTS = {
  surface_utile: "Non disponible"
};

interface InstallationCardProps {
  surface_utile?: number;
}

const InstallationCard = ({surface_utile}: InstallationCardProps) => {
  return (
    <div>
      <div className="flex gap-1">
          <Ruler />
          <p className="font-medium">Superficie exploitable maximale: </p>
        </div>
        <p className="font-medium text-center">
          <span className="text-xl">≈{surface_utile || UNKNOWN_TEXTS.surface_utile}</span> M²
        </p>
        <div className="flex  gap-1">
          <ChartPie />
          <p className="font-medium">Estimation des revenus mensuels maximaux de l&apos;installation</p>
        </div>
    </div>
  );
};
export default InstallationCard;
