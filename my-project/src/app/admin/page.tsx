"use client";

import { useState } from "react";
import Link from "next/link";
import { LeadsTab } from "@/components/admin/LeadsTab";
import { AuditsTab } from "@/components/admin/AuditsTab";
import { AnalyticsTab } from "@/components/admin/AnalyticsTab";
import { PortfoliosTab } from "@/components/admin/PortfoliosTab";

const tabs = [
  { id: "leads", label: "Leads" },
  { id: "audits", label: "Audits" },
  { id: "analytics", label: "Analytics" },
  { id: "portfolios", label: "Réalisations" },
];

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState("leads");

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b bg-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
          <div className="flex items-center gap-4">
            <Link href="/" className="text-xl font-bold text-blue-600">
              Astro Agency
            </Link>
            <span className="rounded-md bg-gray-100 px-2 py-1 text-xs font-medium text-gray-500">Admin</span>
          </div>
          <Link href="/" className="text-sm text-gray-500 hover:text-blue-600">
            Retour au site
          </Link>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-8">
        <h1 className="mb-6 text-2xl font-bold">Dashboard</h1>
        <div className="mb-6 flex gap-1 rounded-lg bg-gray-100 p-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`rounded-md px-4 py-2 text-sm font-medium transition ${
                activeTab === tab.id ? "bg-white text-blue-600 shadow-sm" : "text-gray-500 hover:text-gray-700"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
        {activeTab === "leads" && <LeadsTab />}
        {activeTab === "audits" && <AuditsTab />}
        {activeTab === "analytics" && <AnalyticsTab />}
        {activeTab === "portfolios" && <PortfoliosTab />}
      </main>
    </div>
  );
}
