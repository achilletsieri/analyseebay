"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface Props {
  sector: string;
  city: string;
}

export function SeoContactForm({ sector, city }: Props) {
  const [form, setForm] = useState({ name: "", email: "", phone: "", message: "" });
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  const update = (field: string, value: string) => setForm({ ...form, [field]: value });

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, sector, city }),
      });
      setSent(true);
    } catch {
      alert("Erreur. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  if (sent) {
    return (
      <div className="rounded-xl border bg-green-50 p-6 text-center">
        <p className="text-lg font-semibold text-green-700">Merci ! Nous vous recontacterons rapidement.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border bg-white p-6">
      <h3 className="mb-4 text-xl font-bold">Contactez-nous</h3>
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <Label htmlFor="seo-name">Nom</Label>
          <Input id="seo-name" value={form.name} onChange={(e) => update("name", e.target.value)} />
        </div>
        <div>
          <Label htmlFor="seo-email">Email</Label>
          <Input id="seo-email" type="email" value={form.email} onChange={(e) => update("email", e.target.value)} />
        </div>
        <div>
          <Label htmlFor="seo-phone">Téléphone</Label>
          <Input id="seo-phone" type="tel" value={form.phone} onChange={(e) => update("phone", e.target.value)} />
        </div>
        <div>
          <Label htmlFor="seo-message">Message</Label>
          <Input id="seo-message" value={form.message} onChange={(e) => update("message", e.target.value)} />
        </div>
      </div>
      <Button
        onClick={handleSubmit}
        disabled={!form.name || !form.email || loading}
        className="mt-4 w-full"
        size="lg"
      >
        {loading ? "Envoi..." : "Envoyer"}
      </Button>
    </div>
  );
}
