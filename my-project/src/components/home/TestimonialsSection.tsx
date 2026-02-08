const testimonials = [
  {
    name: "Jean-Pierre M.",
    role: "Plombier à Strasbourg",
    text: "Mon ancien site WordPress me coûtait 120€/mois et mettait 8 secondes à charger. Maintenant, mon site charge en moins d'une seconde pour seulement 33€/mois !",
  },
  {
    name: "Sophie L.",
    role: "Électricienne à Colmar",
    text: "Grâce à mon nouveau site, je reçois 3x plus de demandes de devis. Le SEO local fait vraiment la différence.",
  },
  {
    name: "Marc D.",
    role: "Paysagiste à Nancy",
    text: "Le rapport qualité-prix est imbattable. Mon site est professionnel, rapide et mes clients adorent.",
  },
];

export function TestimonialsSection() {
  return (
    <section className="bg-gray-50 py-16">
      <div className="mx-auto max-w-7xl px-4">
        <h2 className="mb-12 text-center text-3xl font-bold">Témoignages</h2>
        <div className="grid gap-6 md:grid-cols-3">
          {testimonials.map((t) => (
            <div key={t.name} className="rounded-xl border bg-white p-6 shadow-sm">
              <p className="mb-4 text-gray-600">&ldquo;{t.text}&rdquo;</p>
              <p className="font-semibold">{t.name}</p>
              <p className="text-sm text-gray-500">{t.role}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
