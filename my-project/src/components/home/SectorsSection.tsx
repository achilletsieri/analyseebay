import Link from "next/link";
import { SECTORS } from "@/lib/constants";

export function SectorsSection() {
  return (
    <section id="secteurs" className="bg-gray-50 py-16">
      <div className="mx-auto max-w-7xl px-4">
        <h2 className="mb-4 text-center text-3xl font-bold">Nos Secteurs</h2>
        <p className="mb-12 text-center text-gray-600">
          Sites web sur mesure pour 9 secteurs de PME/TPE
        </p>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {SECTORS.map((sector) => (
            <Link
              key={sector.slug}
              href={`/${sector.slug}/strasbourg`}
              className="group rounded-xl border bg-white p-6 shadow-sm transition hover:shadow-md"
            >
              <span className="mb-3 block text-4xl">{sector.icon}</span>
              <h3 className="mb-2 text-lg font-semibold group-hover:text-blue-600">
                {sector.name}
              </h3>
              <p className="text-sm text-gray-500">{sector.description}</p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
