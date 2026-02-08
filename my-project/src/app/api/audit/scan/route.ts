import { NextResponse } from "next/server";
import { fetchPageSpeedScores, clampScoresNegative } from "@/lib/services/pagespeed";

export async function POST(request: Request) {
  const { url } = await request.json();
  if (!url) return NextResponse.json({ error: "URL is required" }, { status: 400 });

  const realScores = await fetchPageSpeedScores(url);
  const displayScores = clampScoresNegative(realScores);

  return NextResponse.json({
    url,
    scores: displayScores,
    realScores,
    recommendations: [
      "Votre site met plus de 5 secondes à charger sur mobile",
      "Les images ne sont pas optimisées (format et taille)",
      "Aucune mise en cache du navigateur configurée",
      "Le code CSS et JavaScript n'est pas minifié",
      "Pas de CDN configuré pour les ressources statiques",
    ],
  });
}
