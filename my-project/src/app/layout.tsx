import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Astro Agency | Sites Web Ultra-Performants pour PME/TPE",
  description:
    "Remplacez vos sites WordPress lents et coûteux par des sites ultra-performants. Spécialistes du Grand Est, 33€/mois au lieu de 120€.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
