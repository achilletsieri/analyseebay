import { notFound } from "next/navigation";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { SECTORS, CITIES, PRICING } from "@/lib/constants";
import { SeoContactForm } from "@/components/seo/SeoContactForm";

export async function generateStaticParams() {
  const params: { secteur: string; ville: string }[] = [];
  for (const s of SECTORS) {
    for (const c of CITIES) {
      params.push({ secteur: s.slug, ville: c.slug });
    }
  }
  return params;
}

export async function generateMetadata({ params }: { params: Promise<{ secteur: string; ville: string }> }) {
  const { secteur, ville } = await params;
  const sector = SECTORS.find((s) => s.slug === secteur);
  const city = CITIES.find((c) => c.slug === ville);
  if (!sector || !city) return {};
  return {
    title: `Site Web pour ${sector.name} à ${city.name} | Astro Agency`,
    description: `Création de site web professionnel pour ${sector.name} à ${city.name}. Sites ultra-rapides à ${PRICING.ours.monthly}€/mois. Audit gratuit.`,
  };
}

export default async function SeoPage({ params }: { params: Promise<{ secteur: string; ville: string }> }) {
  const { secteur, ville } = await params;
  const sector = SECTORS.find((s) => s.slug === secteur);
  const city = CITIES.find((c) => c.slug === ville);
  if (!sector || !city) notFound();

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50">
        <section className="bg-gradient-to-br from-blue-600 to-indigo-800 py-16 text-white">
          <div className="mx-auto max-w-4xl px-4 text-center">
            <nav className="mb-4 text-sm text-blue-200">
              <Link href="/" className="hover:text-white">Accueil</Link> / {sector.name} / {city.name}
            </nav>
            <h1 className="mb-4 text-4xl font-extrabold">
              Site Web pour {sector.name} à {city.name}
            </h1>
            <p className="mb-8 text-lg text-blue-100">
              {sector.icon} Création de site web professionnel pour votre activité de {sector.name.toLowerCase()} à {city.name} et ses environs.
            </p>
            <Link href="/audit">
              <Button size="lg" className="bg-yellow-400 text-gray-900 hover:bg-yellow-300">
                Demander un Audit Gratuit
              </Button>
            </Link>
          </div>
        </section>
        <section className="py-12">
          <div className="mx-auto max-w-4xl px-4">
            <div className="mb-8 grid gap-4 md:grid-cols-2">
              <div className="rounded-xl border bg-red-50 p-6 text-center">
                <p className="text-sm text-red-600">WordPress</p>
                <p className="text-3xl font-bold text-red-700">{PRICING.wordpress.threeYears.toLocaleString()}€</p>
                <p className="text-sm text-red-500">sur 3 ans</p>
              </div>
              <div className="rounded-xl border bg-green-50 p-6 text-center">
                <p className="text-sm text-green-600">Notre solution</p>
                <p className="text-3xl font-bold text-green-700">{PRICING.ours.threeYears.toLocaleString()}€</p>
                <p className="text-sm text-green-500">sur 3 ans</p>
              </div>
            </div>
            <div className="mb-8 rounded-xl border bg-white p-6">
              <h2 className="mb-4 text-2xl font-bold">
                Pourquoi choisir Astro Agency pour votre site de {sector.name.toLowerCase()} ?
              </h2>
              <ul className="space-y-3 text-gray-600">
                <li>&#x2713; Site ultra-rapide (chargement &lt; 1 seconde)</li>
                <li>&#x2713; Optimisé SEO pour {city.name} et le Grand Est</li>
                <li>&#x2713; Design moderne et professionnel</li>
                <li>&#x2713; Responsive (mobile, tablette, desktop)</li>
                <li>&#x2713; Formulaire de contact et demande de devis</li>
                <li>&#x2713; Économisez {PRICING.savings.toLocaleString()}€ sur 3 ans</li>
              </ul>
            </div>
            <SeoContactForm sector={secteur} city={ville} />
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
