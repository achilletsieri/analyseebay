"use client";

import { useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";

interface Portfolio {
  id: string;
  title: string;
  description: string;
  sector: string;
  city: string;
  imageUrl: string | null;
  isFeatured: boolean;
}

interface Sector {
  name: string;
  slug: string;
  icon: string;
}

interface Props {
  portfolios: Portfolio[];
  sectors: Sector[];
}

export function PortfolioGrid({ portfolios, sectors }: Props) {
  const [filter, setFilter] = useState("all");
  const filtered = filter === "all" ? portfolios : portfolios.filter((p) => p.sector === filter);

  return (
    <div>
      <div className="mb-8 flex flex-wrap justify-center gap-2">
        <button
          onClick={() => setFilter("all")}
          className={`rounded-full px-4 py-2 text-sm font-medium transition ${
            filter === "all" ? "bg-blue-600 text-white" : "bg-white text-gray-700 hover:bg-gray-100"
          }`}
        >
          Tous
        </button>
        {sectors.map((s) => (
          <button
            key={s.slug}
            onClick={() => setFilter(s.slug)}
            className={`rounded-full px-4 py-2 text-sm font-medium transition ${
              filter === s.slug ? "bg-blue-600 text-white" : "bg-white text-gray-700 hover:bg-gray-100"
            }`}
          >
            {s.icon} {s.name}
          </button>
        ))}
      </div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((p) => (
          <Link
            key={p.id}
            href={`/realisations/${p.id}`}
            className="group overflow-hidden rounded-xl border bg-white shadow-sm transition hover:shadow-md"
          >
            <div className="relative h-48 bg-gradient-to-br from-blue-100 to-indigo-100">
              {p.imageUrl ? (
                <img src={p.imageUrl} alt={p.title} className="h-full w-full object-cover" />
              ) : (
                <div className="flex h-full items-center justify-center text-4xl text-blue-300">
                  {sectors.find((s) => s.slug === p.sector)?.icon ?? "🌐"}
                </div>
              )}
              {p.isFeatured && (
                <Badge variant="success" className="absolute right-2 top-2">En vedette</Badge>
              )}
            </div>
            <div className="p-4">
              <h3 className="font-semibold group-hover:text-blue-600">{p.title}</h3>
              <p className="mt-1 text-sm text-gray-500">{p.sector} &bull; {p.city}</p>
              <p className="mt-2 line-clamp-2 text-sm text-gray-600">{p.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
