import Link from "next/link";
import { CITIES } from "@/lib/constants";

export function CitiesSection() {
  return (
    <section id="villes" className="bg-white py-16">
      <div className="mx-auto max-w-7xl px-4">
        <h2 className="mb-4 text-center text-3xl font-bold">15 Villes du Grand Est</h2>
        <p className="mb-12 text-center text-gray-600">
          Couverture dans un rayon de 150 km autour de Strasbourg
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          {CITIES.map((city) => (
            <Link
              key={city.slug}
              href={`/plombier/${city.slug}`}
              className="rounded-full border bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 transition hover:border-blue-300 hover:bg-blue-50 hover:text-blue-600"
            >
              {city.name}
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
