"use client";

import { useState, useEffect, useCallback } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { LEAD_STATUSES } from "@/lib/constants";
import { formatDate } from "@/lib/utils";

interface Lead {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  sector: string;
  city: string;
  status: string;
  source: string;
  createdAt: string;
}

const statusColors: Record<string, string> = {
  PENDING: "bg-yellow-100 text-yellow-800",
  CONTACTED: "bg-blue-100 text-blue-800",
  QUALIFIED: "bg-purple-100 text-purple-800",
  CONVERTED: "bg-green-100 text-green-800",
  LOST: "bg-red-100 text-red-800",
};

export function LeadsTab() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  const fetchLeads = useCallback(async () => {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (statusFilter !== "all") params.set("status", statusFilter);
    const res = await fetch(`/api/leads?${params}`);
    setLeads(await res.json());
  }, [search, statusFilter]);

  useEffect(() => { fetchLeads(); }, [fetchLeads]);

  const updateStatus = async (id: string, status: string) => {
    await fetch(`/api/leads/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    fetchLeads();
  };

  const deleteLead = async (id: string) => {
    if (!confirm("Supprimer ce lead ?")) return;
    await fetch(`/api/leads/${id}`, { method: "DELETE" });
    fetchLeads();
  };

  const stats = {
    total: leads.length,
    qualified: leads.filter((l) => l.status === "QUALIFIED").length,
    converted: leads.filter((l) => l.status === "CONVERTED").length,
  };

  return (
    <div>
      <div className="mb-6 grid grid-cols-4 gap-4">
        <Stat label="Total" value={stats.total} />
        <Stat label="Qualifiés" value={stats.qualified} />
        <Stat label="Convertis" value={stats.converted} />
        <Stat label="Taux" value={stats.total > 0 ? `${Math.round((stats.converted / stats.total) * 100)}%` : "0%"} />
      </div>
      <div className="mb-4 flex gap-4">
        <Input placeholder="Rechercher..." value={search} onChange={(e) => setSearch(e.target.value)} className="max-w-xs" />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="rounded-md border px-3 py-2 text-sm"
        >
          <option value="all">Tous les statuts</option>
          {LEAD_STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>
      <div className="overflow-x-auto rounded-lg border bg-white">
        <table className="w-full text-left text-sm">
          <thead className="border-b bg-gray-50">
            <tr>
              <th className="p-3">Nom</th><th className="p-3">Email</th><th className="p-3">Secteur</th>
              <th className="p-3">Ville</th><th className="p-3">Statut</th><th className="p-3">Date</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {leads.map((lead) => (
              <tr key={lead.id} className="border-b">
                <td className="p-3 font-medium">{lead.name}</td>
                <td className="p-3">{lead.email}</td>
                <td className="p-3">{lead.sector}</td>
                <td className="p-3">{lead.city}</td>
                <td className="p-3">
                  <select
                    value={lead.status}
                    onChange={(e) => updateStatus(lead.id, e.target.value)}
                    className={`rounded-full px-2 py-1 text-xs font-semibold ${statusColors[lead.status] ?? ""}`}
                  >
                    {LEAD_STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                </td>
                <td className="p-3 text-gray-500">{formatDate(lead.createdAt)}</td>
                <td className="p-3">
                  <Button variant="destructive" size="sm" onClick={() => deleteLead(lead.id)}>
                    Suppr.
                  </Button>
                </td>
              </tr>
            ))}
            {leads.length === 0 && (
              <tr><td colSpan={7} className="p-6 text-center text-gray-400">Aucun lead</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-lg border bg-white p-4 text-center">
      <p className="text-2xl font-bold text-blue-600">{value}</p>
      <p className="text-sm text-gray-500">{label}</p>
    </div>
  );
}
