"use client";

import { Button } from "@/components/ui/button";
import { getScoreBadgeColor } from "@/lib/utils";

interface Scores {
  performance: number;
  accessibility: number;
  bestPractices: number;
  seo: number;
}

interface Props {
  url: string;
  scores: Scores;
  recommendations: string[];
  onNext: () => void;
}

function ScoreCircle({ label, score }: { label: string; score: number }) {
  return (
    <div className="flex flex-col items-center">
      <div className={`flex h-20 w-20 items-center justify-center rounded-full text-xl font-bold ${getScoreBadgeColor(score)}`}>
        {score}
      </div>
      <p className="mt-2 text-sm font-medium text-gray-700">{label}</p>
    </div>
  );
}

export function AuditStep2({ url, scores, recommendations, onNext }: Props) {
  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-6 rounded-lg border-l-4 border-red-500 bg-red-50 p-4">
        <h2 className="text-xl font-bold text-red-800">Ce n&apos;est vraiment pas terrible !</h2>
        <p className="text-sm text-red-600">Résultats pour : {url}</p>
      </div>
      <div className="mb-8 flex flex-wrap justify-center gap-6">
        <ScoreCircle label="Performance" score={scores.performance} />
        <ScoreCircle label="Accessibilité" score={scores.accessibility} />
        <ScoreCircle label="Bonnes Pratiques" score={scores.bestPractices} />
        <ScoreCircle label="SEO" score={scores.seo} />
      </div>
      <div className="mb-8 rounded-lg border bg-white p-6">
        <h3 className="mb-3 font-semibold text-gray-900">Recommandations critiques :</h3>
        <ul className="space-y-2">
          {recommendations.map((r, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
              <span className="mt-0.5 text-red-500">&#x2717;</span> {r}
            </li>
          ))}
        </ul>
      </div>
      <Button onClick={onNext} size="lg" className="w-full">
        Obtenir mon devis gratuit
      </Button>
    </div>
  );
}
