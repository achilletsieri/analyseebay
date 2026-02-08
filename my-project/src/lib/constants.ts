export const SECTORS = [
  { name: "Loueur auto", slug: "loueur-auto", icon: "🚗", description: "Location de véhicules pour particuliers et professionnels" },
  { name: "Vendeur auto", slug: "vendeur-auto", icon: "🚗", description: "Vente de véhicules neufs et d'occasion" },
  { name: "Garagiste", slug: "garagiste", icon: "🔧", description: "Réparation et entretien automobile" },
  { name: "Plombier", slug: "plombier", icon: "🔧", description: "Plomberie, chauffage et sanitaire" },
  { name: "Électricien", slug: "electricien", icon: "⚡", description: "Installation et dépannage électrique" },
  { name: "Menuisier", slug: "menuisier", icon: "🪵", description: "Menuiserie intérieure et extérieure" },
  { name: "Couvreur", slug: "couvreur", icon: "🏠", description: "Toiture, zinguerie et isolation" },
  { name: "Paysagiste", slug: "paysagiste", icon: "🌳", description: "Aménagement et entretien de jardins" },
  { name: "Peintre", slug: "peintre", icon: "🎨", description: "Peinture intérieure et extérieure" },
] as const;

export const CITIES = [
  { name: "Strasbourg", slug: "strasbourg", zipCode: "67000", region: "Grand Est", latitude: 48.5734, longitude: 7.7521 },
  { name: "Haguenau", slug: "haguenau", zipCode: "67500", region: "Grand Est", latitude: 48.8159, longitude: 7.7906 },
  { name: "Colmar", slug: "colmar", zipCode: "68000", region: "Grand Est", latitude: 48.0794, longitude: 7.3580 },
  { name: "Mulhouse", slug: "mulhouse", zipCode: "68100", region: "Grand Est", latitude: 47.7508, longitude: 7.3359 },
  { name: "Sélestat", slug: "selestat", zipCode: "67600", region: "Grand Est", latitude: 48.2598, longitude: 7.4528 },
  { name: "Saverne", slug: "saverne", zipCode: "67700", region: "Grand Est", latitude: 48.7413, longitude: 7.3626 },
  { name: "Obernai", slug: "obernai", zipCode: "67210", region: "Grand Est", latitude: 48.4614, longitude: 7.4829 },
  { name: "Saint-Dié", slug: "saint-die", zipCode: "88100", region: "Grand Est", latitude: 48.2866, longitude: 6.9499 },
  { name: "Épinal", slug: "epinal", zipCode: "88000", region: "Grand Est", latitude: 48.1725, longitude: 6.4502 },
  { name: "Nancy", slug: "nancy", zipCode: "54000", region: "Grand Est", latitude: 48.6921, longitude: 6.1844 },
  { name: "Metz", slug: "metz", zipCode: "57000", region: "Grand Est", latitude: 49.1193, longitude: 6.1757 },
  { name: "Sarreguemines", slug: "sarreguemines", zipCode: "57200", region: "Grand Est", latitude: 49.1098, longitude: 7.0684 },
  { name: "Forbach", slug: "forbach", zipCode: "57600", region: "Grand Est", latitude: 49.1856, longitude: 6.9013 },
  { name: "Lunéville", slug: "luneville", zipCode: "54300", region: "Grand Est", latitude: 48.5936, longitude: 6.4967 },
  { name: "Wissembourg", slug: "wissembourg", zipCode: "67160", region: "Grand Est", latitude: 49.0396, longitude: 7.9456 },
] as const;

export const LEAD_STATUSES = ["PENDING", "CONTACTED", "QUALIFIED", "CONVERTED", "LOST"] as const;

export const PRICING = {
  wordpress: { monthly: 120, threeYears: 4320 },
  ours: { monthly: 33, threeYears: 1188 },
  savings: 3132,
} as const;
