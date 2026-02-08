import { prisma } from "@/lib/db";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { PortfolioGrid } from "@/components/portfolio/PortfolioGrid";
import { SECTORS } from "@/lib/constants";

export const metadata = {
  title: "Nos Réalisations | Astro Agency",
  description: "Découvrez nos 20+ réalisations de sites web pour PME/TPE du Grand Est.",
};

export default async function RealisationsPage() {
  const portfolios = await prisma.portfolio.findMany({ orderBy: { createdAt: "desc" } });

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50 py-12">
        <div className="mx-auto max-w-7xl px-4">
          <h1 className="mb-4 text-center text-4xl font-bold">Nos Réalisations</h1>
          <p className="mb-12 text-center text-gray-600">
            Découvrez les sites web que nous avons créés pour des PME/TPE du Grand Est
          </p>
          <PortfolioGrid portfolios={portfolios} sectors={[...SECTORS]} />
        </div>
      </main>
      <Footer />
    </>
  );
}
