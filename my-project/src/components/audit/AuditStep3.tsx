"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { SECTORS, CITIES } from "@/lib/constants";

interface FormData {
  name: string;
  email: string;
  phone: string;
  sector: string;
  city: string;
  message: string;
  rgpd: boolean;
}

interface Props {
  form: FormData;
  setForm: (form: FormData) => void;
  onSubmit: () => void;
  loading: boolean;
}

export function AuditStep3({ form, setForm, onSubmit, loading }: Props) {
  const update = (field: keyof FormData, value: string | boolean) =>
    setForm({ ...form, [field]: value });

  const valid = form.name && form.email && form.sector && form.city && form.rgpd;

  return (
    <div className="mx-auto max-w-lg">
      <h2 className="mb-6 text-center text-2xl font-bold">Vos coordonnées</h2>
      <div className="space-y-4">
        <div>
          <Label htmlFor="name">Nom *</Label>
          <Input id="name" value={form.name} onChange={(e) => update("name", e.target.value)} />
        </div>
        <div>
          <Label htmlFor="email">Email *</Label>
          <Input id="email" type="email" value={form.email} onChange={(e) => update("email", e.target.value)} />
        </div>
        <div>
          <Label htmlFor="phone">Téléphone</Label>
          <Input id="phone" type="tel" value={form.phone} onChange={(e) => update("phone", e.target.value)} />
        </div>
        <div>
          <Label htmlFor="sector">Secteur d&apos;activité *</Label>
          <select
            id="sector"
            value={form.sector}
            onChange={(e) => update("sector", e.target.value)}
            className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          >
            <option value="">Sélectionnez</option>
            {SECTORS.map((s) => (
              <option key={s.slug} value={s.slug}>{s.icon} {s.name}</option>
            ))}
          </select>
        </div>
        <div>
          <Label htmlFor="city">Ville *</Label>
          <select
            id="city"
            value={form.city}
            onChange={(e) => update("city", e.target.value)}
            className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          >
            <option value="">Sélectionnez</option>
            {CITIES.map((c) => (
              <option key={c.slug} value={c.slug}>{c.name}</option>
            ))}
          </select>
        </div>
        <div>
          <Label htmlFor="message">Message (optionnel)</Label>
          <textarea
            id="message"
            rows={3}
            value={form.message}
            onChange={(e) => update("message", e.target.value)}
            className="flex w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          />
        </div>
        <label className="flex items-start gap-2 text-sm">
          <input
            type="checkbox"
            checked={form.rgpd}
            onChange={(e) => update("rgpd", e.target.checked)}
            className="mt-1"
          />
          <span>J&apos;accepte que mes données soient utilisées pour me recontacter. *</span>
        </label>
        <Button onClick={onSubmit} disabled={!valid || loading} className="w-full" size="lg">
          {loading ? "Envoi en cours..." : "Envoyer ma demande"}
        </Button>
      </div>
    </div>
  );
}
