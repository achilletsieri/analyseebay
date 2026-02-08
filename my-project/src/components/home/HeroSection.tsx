import Link from "next/link";
import { PRICING } from "@/lib/constants";

export function HeroSection() {
  return (
    <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 py-20 text-white">
      <div className="mx-auto max-w-7xl px-4 text-center">
        <h1 className="mb-6 text-4xl font-extrabold leading-tight md:text-6xl">
          Remplacez vos sites WordPress
          <br />
          <span className="text-yellow-300">lents et coûteux</span>
          <br />
          par des sites ultra-performants
        </h1>
        <p className="mx-auto mb-8 max-w-2xl text-lg text-blue-100">
          Spécialistes de la création de sites web pour PME/TPE du Grand Est.
          Des sites rapides, modernes et optimisés SEO.
        </p>
        <div className="mb-8 flex flex-col items-center justify-center gap-6 md:flex-row">
          <div className="rounded-xl bg-red-500/20 px-6 py-4 backdrop-blur">
            <p className="text-sm text-red-200">WordPress</p>
            <p className="text-3xl font-bold">{PRICING.wordpress.threeYears.toLocaleString()}€</p>
            <p className="text-sm text-red-200">sur 3 ans ({PRICING.wordpress.monthly}€/mois)</p>
          </div>
          <span className="text-2xl font-bold">VS</span>
          <div className="rounded-xl bg-green-500/20 px-6 py-4 backdrop-blur">
            <p className="text-sm text-green-200">Notre solution</p>
            <p className="text-3xl font-bold">{PRICING.ours.threeYears.toLocaleString()}€</p>
            <p className="text-sm text-green-200">sur 3 ans ({PRICING.ours.monthly}€/mois)</p>
          </div>
        </div>
        <p className="mb-8 text-xl font-semibold text-yellow-300">
          Économisez {PRICING.savings.toLocaleString()}€ sur 3 ans !
        </p>
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Link
            href="/audit"
            className="rounded-lg bg-yellow-400 px-8 py-3 text-lg font-bold text-gray-900 hover:bg-yellow-300"
          >
            Demander un Audit Gratuit
          </Link>
          <Link
            href="/realisations"
            className="rounded-lg border-2 border-white px-8 py-3 text-lg font-bold hover:bg-white/10"
          >
            Nos Réalisations
          </Link>
        </div>
      </div>
    </section>
  );
}
