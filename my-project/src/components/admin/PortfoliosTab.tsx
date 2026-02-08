"use client";

import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDate } from "@/lib/utils";

interface Portfolio {
  id: string;
  title: string;
  sector: string;
  city: string;
  isFeatured: boolean;
  imageUrl: string | null;
  createdAt: string;
}

export function PortfoliosTab() {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetch("/api/portfolios").then((r) => r.json()).then(setPortfolios);
  }, []);

  const generateImages = async () => {
    setGenerating(true);
    try {
      const res = await fetch("/api/portfolio/generate", { method: "POST" });
      const data = await res.json();
      alert(`${data.generated} images générées avec succès !`);
      const updated = await fetch("/api/portfolios").then((r) => r.json());
      setPortfolios(updated);
    } catch {
      alert("Erreur lors de la génération.");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold">Réalisations ({portfolios.length})</h3>
        <Button onClick={generateImages} disabled={generating}>
          {generating ? "Génération en cours..." : "Générer les images des sites"}
        </Button>
      </div>
      <div className="overflow-x-auto rounded-lg border bg-white">
        <table className="w-full text-left text-sm">
          <thead className="border-b bg-gray-50">
            <tr>
              <th className="p-3">Titre</th>
              <th className="p-3">Secteur</th>
              <th className="p-3">Ville</th>
              <th className="p-3">Statut</th>
              <th className="p-3">Image</th>
              <th className="p-3">Date</th>
            </tr>
          </thead>
          <tbody>
            {portfolios.map((p) => (
              <tr key={p.id} className="border-b">
                <td className="p-3 font-medium">{p.title}</td>
                <td className="p-3">{p.sector}</td>
                <td className="p-3">{p.city}</td>
                <td className="p-3">
                  {p.isFeatured ? (
                    <Badge variant="success">En vedette</Badge>
                  ) : (
                    <Badge variant="secondary">Standard</Badge>
                  )}
                </td>
                <td className="p-3">
                  {p.imageUrl ? (
                    <Badge variant="success">Générée</Badge>
                  ) : (
                    <Badge variant="destructive">En attente</Badge>
                  )}
                </td>
                <td className="p-3 text-gray-500">{formatDate(p.createdAt)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
