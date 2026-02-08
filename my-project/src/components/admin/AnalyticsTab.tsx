"use client";

import { useState, useEffect } from "react";
import { SECTORS, CITIES } from "@/lib/constants";

interface Lead {
  sector: string;
  city: string;
}

export function AnalyticsTab() {
  const [leads, setLeads] = useState<Lead[]>([]);

  useEffect(() => {
    fetch("/api/leads").then((r) => r.json()).then(setLeads);
  }, []);

  const bySector = SECTORS.map((s) => ({
    name: s.name,
    icon: s.icon,
    count: leads.filter((l) => l.sector === s.slug).length,
  }));

  const byCity = CITIES.map((c) => ({
    name: c.name,
    count: leads.filter((l) => l.city === c.slug).length,
  }));

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div className="rounded-lg border bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold">Leads par secteur</h3>
        <div className="space-y-3">
          {bySector.map((item) => (
            <div key={item.name} className="flex items-center justify-between">
              <span className="text-sm">
                {item.icon} {item.name}
              </span>
              <div className="flex items-center gap-2">
                <div className="h-2 rounded-full bg-blue-200" style={{ width: `${Math.max(item.count * 30, 8)}px` }} />
                <span className="text-sm font-semibold">{item.count}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="rounded-lg border bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold">Leads par ville</h3>
        <div className="space-y-3">
          {byCity.map((item) => (
            <div key={item.name} className="flex items-center justify-between">
              <span className="text-sm">{item.name}</span>
              <div className="flex items-center gap-2">
                <div className="h-2 rounded-full bg-green-200" style={{ width: `${Math.max(item.count * 30, 8)}px` }} />
                <span className="text-sm font-semibold">{item.count}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="rounded-lg border bg-white p-6 md:col-span-2">
        <h3 className="mb-4 text-lg font-semibold">Statistiques générales</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-3xl font-bold text-blue-600">{leads.length}</p>
            <p className="text-sm text-gray-500">Total leads</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-green-600">9</p>
            <p className="text-sm text-gray-500">Secteurs actifs</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-purple-600">15</p>
            <p className="text-sm text-gray-500">Villes couvertes</p>
          </div>
        </div>
      </div>
    </div>
  );
}
