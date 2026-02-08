interface Props {
  features: string;
}

const performances = [
  { label: "Vitesse de chargement", value: "< 1s" },
  { label: "Score PageSpeed", value: "95/100" },
  { label: "Mobile-friendly", value: "100%" },
];

export function ProjectDetails({ features }: Props) {
  const featureList = features ? features.split(",").map((f) => f.trim()) : [];

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div className="rounded-xl border bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold">Design &amp; Branding</h3>
        <ul className="space-y-2 text-sm text-gray-600">
          <li>Palette de couleurs personnalisée</li>
          <li>Style visuel moderne et épuré</li>
          <li>Site vitrine professionnel</li>
          <li>Identité visuelle cohérente</li>
        </ul>
      </div>
      <div className="rounded-xl border bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold">Fonctionnalités</h3>
        <ul className="space-y-2 text-sm text-gray-600">
          {featureList.length > 0 ? (
            featureList.map((f) => <li key={f}>&#x2713; {f}</li>)
          ) : (
            <>
              <li>&#x2713; Responsive design</li>
              <li>&#x2713; Navigation intuitive</li>
              <li>&#x2713; SEO optimisé</li>
              <li>&#x2713; Formulaire de contact</li>
            </>
          )}
        </ul>
      </div>
      <div className="rounded-xl border bg-white p-6 md:col-span-2">
        <h3 className="mb-4 text-lg font-semibold">Performances</h3>
        <div className="grid grid-cols-3 gap-4">
          {performances.map((p) => (
            <div key={p.label} className="text-center">
              <p className="text-2xl font-bold text-green-600">{p.value}</p>
              <p className="text-sm text-gray-500">{p.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
