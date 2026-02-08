import Link from "next/link";
import { Button } from "@/components/ui/button";

export function AuditStep4() {
  return (
    <div className="mx-auto max-w-lg text-center">
      <div className="mb-6 text-6xl">&#x2705;</div>
      <h2 className="mb-4 text-2xl font-bold text-green-700">Demande envoyée avec succès !</h2>
      <p className="mb-8 text-gray-600">
        Merci pour votre demande. Notre équipe vous recontactera dans les 24 heures
        avec un devis personnalisé pour votre activité.
      </p>
      <Link href="/realisations">
        <Button size="lg">Découvrir nos réalisations</Button>
      </Link>
    </div>
  );
}
