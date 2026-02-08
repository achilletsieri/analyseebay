import Link from "next/link";
import { SECTORS, CITIES } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="border-t bg-gray-900 text-gray-300">
      <div className="mx-auto max-w-7xl px-4 py-12">
        <div className="grid gap-8 md:grid-cols-4">
          <div>
            <h3 className="mb-3 text-lg font-bold text-white">Astro Agency</h3>
            <p className="text-sm">Sites web ultra-performants pour PME/TPE du Grand Est.</p>
            <p className="mt-2 text-sm">33€/mois au lieu de 120€</p>
          </div>
          <div>
            <h4 className="mb-3 font-semibold text-white">Secteurs</h4>
            <ul className="space-y-1 text-sm">
              {SECTORS.slice(0, 5).map((s) => (
                <li key={s.slug}>
                  <Link href={`/${s.slug}/strasbourg`} className="hover:text-white">
                    {s.icon} {s.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="mb-3 font-semibold text-white">Villes</h4>
            <ul className="space-y-1 text-sm">
              {CITIES.slice(0, 5).map((c) => (
                <li key={c.slug}>
                  <Link href={`/plombier/${c.slug}`} className="hover:text-white">
                    {c.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="mb-3 font-semibold text-white">Contact</h4>
            <p className="text-sm">Strasbourg, Grand Est</p>
            <Link href="/audit" className="mt-2 inline-block text-sm text-blue-400 hover:text-blue-300">
              Demander un audit gratuit
            </Link>
            <div className="mt-4">
              <Link href="/admin" className="text-xs text-gray-500 hover:text-gray-400">
                Administration
              </Link>
            </div>
          </div>
        </div>
        <div className="mt-8 border-t border-gray-700 pt-8 text-center text-sm">
          © {new Date().getFullYear()} Astro Agency. Tous droits réservés.
        </div>
      </div>
    </footer>
  );
}
