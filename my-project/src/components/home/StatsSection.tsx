const stats = [
  { value: "135+", label: "Pages SEO optimisées" },
  { value: "9", label: "Secteurs couverts" },
  { value: "15", label: "Villes du Grand Est" },
  { value: "< 1s", label: "Temps de chargement" },
];

export function StatsSection() {
  return (
    <section className="bg-white py-16">
      <div className="mx-auto max-w-7xl px-4">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <p className="text-4xl font-extrabold text-blue-600">{stat.value}</p>
              <p className="mt-2 text-sm text-gray-600">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
