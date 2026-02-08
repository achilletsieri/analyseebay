"use client";

import { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { AuditStep1 } from "@/components/audit/AuditStep1";
import { AuditStep2 } from "@/components/audit/AuditStep2";
import { AuditStep3 } from "@/components/audit/AuditStep3";
import { AuditStep4 } from "@/components/audit/AuditStep4";

interface Scores {
  performance: number;
  accessibility: number;
  bestPractices: number;
  seo: number;
}

const defaultForm = { name: "", email: "", phone: "", sector: "", city: "", message: "", rgpd: false };

export default function AuditPage() {
  const [step, setStep] = useState(1);
  const [url, setUrl] = useState("");
  const [scores, setScores] = useState<Scores | null>(null);
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [form, setForm] = useState(defaultForm);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/audit/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      setScores(data.scores);
      setRecommendations(data.recommendations);
      setStep(2);
    } catch {
      alert("Erreur lors de l'analyse. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await fetch("/api/audits", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url,
          contactName: form.name,
          contactEmail: form.email,
          contactPhone: form.phone,
          sector: form.sector,
          city: form.city,
          ...scores,
          performanceScore: scores?.performance ?? 0,
          accessibilityScore: scores?.accessibility ?? 0,
          bestPracticesScore: scores?.bestPractices ?? 0,
          seoScore: scores?.seo ?? 0,
        }),
      });
      await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name,
          email: form.email,
          phone: form.phone,
          sector: form.sector,
          city: form.city,
          message: form.message,
          website: url,
          source: "audit",
        }),
      });
      setStep(4);
    } catch {
      alert("Erreur lors de l'envoi. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  const steps = ["Analyse", "Rapport", "Contact", "Confirmation"];

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50 py-12">
        <div className="mx-auto max-w-4xl px-4">
          <div className="mb-8 flex items-center justify-center gap-2">
            {steps.map((s, i) => (
              <div key={s} className="flex items-center gap-2">
                <div
                  className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold ${
                    i + 1 <= step ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-500"
                  }`}
                >
                  {i + 1}
                </div>
                <span className="hidden text-sm sm:inline">{s}</span>
                {i < 3 && <div className="h-0.5 w-8 bg-gray-200" />}
              </div>
            ))}
          </div>
          <div className="rounded-xl border bg-white p-8 shadow-sm">
            {step === 1 && <AuditStep1 url={url} setUrl={setUrl} onAnalyze={handleAnalyze} loading={loading} />}
            {step === 2 && scores && (
              <AuditStep2 url={url} scores={scores} recommendations={recommendations} onNext={() => setStep(3)} />
            )}
            {step === 3 && <AuditStep3 form={form} setForm={setForm} onSubmit={handleSubmit} loading={loading} />}
            {step === 4 && <AuditStep4 />}
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
