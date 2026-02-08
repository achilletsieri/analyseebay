import Link from "next/link";

export function Navbar() {
  return (
    <nav className="sticky top-0 z-50 border-b bg-white/95 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <Link href="/" className="text-xl font-bold text-blue-600">
          Astro Agency
        </Link>
        <div className="hidden items-center gap-6 md:flex">
          <Link href="/#secteurs" className="text-sm text-gray-600 hover:text-blue-600">
            Secteurs
          </Link>
          <Link href="/#villes" className="text-sm text-gray-600 hover:text-blue-600">
            Villes
          </Link>
          <Link href="/realisations" className="text-sm text-gray-600 hover:text-blue-600">
            Nos Réalisations
          </Link>
          <Link
            href="/audit"
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Audit Gratuit
          </Link>
        </div>
      </div>
    </nav>
  );
}
