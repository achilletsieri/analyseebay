"use client";

import { useState, useEffect } from "react";
import { getScoreBadgeColor, formatDate } from "@/lib/utils";

interface Audit {
  id: string;
  url: string;
  contactName: string;
  contactEmail: string;
  performanceScore: number;
  accessibilityScore: number;
  bestPracticesScore: number;
  seoScore: number;
  createdAt: string;
}

function ScoreBadge({ score }: { score: number }) {
  return (
    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-bold ${getScoreBadgeColor(score)}`}>
      {score}
    </span>
  );
}

export function AuditsTab() {
  const [audits, setAudits] = useState<Audit[]>([]);

  useEffect(() => {
    fetch("/api/audits").then((r) => r.json()).then(setAudits);
  }, []);

  return (
    <div className="overflow-x-auto rounded-lg border bg-white">
      <table className="w-full text-left text-sm">
        <thead className="border-b bg-gray-50">
          <tr>
            <th className="p-3">URL</th>
            <th className="p-3">Contact</th>
            <th className="p-3">Email</th>
            <th className="p-3">Date</th>
            <th className="p-3">Perf.</th>
            <th className="p-3">Access.</th>
            <th className="p-3">BP</th>
            <th className="p-3">SEO</th>
          </tr>
        </thead>
        <tbody>
          {audits.map((audit) => (
            <tr key={audit.id} className="border-b">
              <td className="max-w-[200px] truncate p-3 font-medium">{audit.url}</td>
              <td className="p-3">{audit.contactName}</td>
              <td className="p-3">{audit.contactEmail}</td>
              <td className="p-3 text-gray-500">{formatDate(audit.createdAt)}</td>
              <td className="p-3"><ScoreBadge score={audit.performanceScore} /></td>
              <td className="p-3"><ScoreBadge score={audit.accessibilityScore} /></td>
              <td className="p-3"><ScoreBadge score={audit.bestPracticesScore} /></td>
              <td className="p-3"><ScoreBadge score={audit.seoScore} /></td>
            </tr>
          ))}
          {audits.length === 0 && (
            <tr><td colSpan={8} className="p-6 text-center text-gray-400">Aucun audit</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
