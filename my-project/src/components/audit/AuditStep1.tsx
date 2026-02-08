"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface Props {
  url: string;
  setUrl: (url: string) => void;
  onAnalyze: () => void;
  loading: boolean;
}

export function AuditStep1({ url, setUrl, onAnalyze, loading }: Props) {
  return (
    <div className="mx-auto max-w-lg text-center">
      <h2 className="mb-2 text-2xl font-bold">Analysez votre site web</h2>
      <p className="mb-8 text-gray-600">
        Entrez l&apos;URL de votre site actuel pour obtenir un rapport de performance détaillé.
      </p>
      <div className="space-y-4">
        <div className="text-left">
          <Label htmlFor="url">URL de votre site</Label>
          <Input
            id="url"
            type="url"
            placeholder="https://www.monsite.fr"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>
        <Button onClick={onAnalyze} disabled={!url || loading} className="w-full" size="lg">
          {loading ? "Analyse en cours..." : "Analyser mon site"}
        </Button>
      </div>
    </div>
  );
}
