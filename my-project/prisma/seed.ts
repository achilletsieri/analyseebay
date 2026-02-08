import "dotenv/config";
import { PrismaClient } from "../src/generated/prisma/client";
import { PrismaBetterSqlite3 } from "@prisma/adapter-better-sqlite3";

const adapter = new PrismaBetterSqlite3({
  url: process.env.DATABASE_URL ?? "file:./prisma/dev.db",
});
const prisma = new PrismaClient({ adapter });

const SECTORS = [
  { name: "Loueur auto", slug: "loueur-auto", icon: "🚗", description: "Location de véhicules pour particuliers et professionnels" },
  { name: "Vendeur auto", slug: "vendeur-auto", icon: "🚗", description: "Vente de véhicules neufs et d'occasion" },
  { name: "Garagiste", slug: "garagiste", icon: "🔧", description: "Réparation et entretien automobile" },
  { name: "Plombier", slug: "plombier", icon: "🔧", description: "Plomberie, chauffage et sanitaire" },
  { name: "Électricien", slug: "electricien", icon: "⚡", description: "Installation et dépannage électrique" },
  { name: "Menuisier", slug: "menuisier", icon: "🪵", description: "Menuiserie intérieure et extérieure" },
  { name: "Couvreur", slug: "couvreur", icon: "🏠", description: "Toiture, zinguerie et isolation" },
  { name: "Paysagiste", slug: "paysagiste", icon: "🌳", description: "Aménagement et entretien de jardins" },
  { name: "Peintre", slug: "peintre", icon: "🎨", description: "Peinture intérieure et extérieure" },
];

const CITIES = [
  { name: "Strasbourg", slug: "strasbourg", zipCode: "67000", region: "Grand Est", latitude: 48.5734, longitude: 7.7521 },
  { name: "Haguenau", slug: "haguenau", zipCode: "67500", region: "Grand Est", latitude: 48.8159, longitude: 7.7906 },
  { name: "Colmar", slug: "colmar", zipCode: "68000", region: "Grand Est", latitude: 48.0794, longitude: 7.358 },
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
];

const PORTFOLIOS = [
  { title: "AutoLoc Strasbourg", description: "Site vitrine pour une agence de location de véhicules avec système de réservation en ligne et catalogue de véhicules.", sector: "loueur-auto", city: "Strasbourg", isFeatured: true, features: "Réservation en ligne,Catalogue véhicules,Tarifs dynamiques,Responsive design" },
  { title: "AutoLoc Colmar", description: "Plateforme de location de voitures avec gestion de flotte et paiement en ligne.", sector: "loueur-auto", city: "Colmar", isFeatured: false, features: "Gestion de flotte,Paiement en ligne,GPS intégré,Avis clients" },
  { title: "AutoVente Mulhouse", description: "Site e-commerce automobile avec fiches véhicules détaillées et estimation de reprise.", sector: "vendeur-auto", city: "Mulhouse", isFeatured: true, features: "Fiches véhicules,Estimation reprise,Financement,Comparateur" },
  { title: "AutoVente Nancy", description: "Vitrine en ligne pour concessionnaire avec configurateur et prise de rendez-vous.", sector: "vendeur-auto", city: "Nancy", isFeatured: false, features: "Configurateur,Prise de RDV,Stock temps réel,Newsletter" },
  { title: "Garage Express Metz", description: "Site pour garage automobile avec prise de rendez-vous en ligne et devis instantané.", sector: "garagiste", city: "Metz", isFeatured: false, features: "Devis en ligne,Prise de RDV,Suivi réparations,Avis Google" },
  { title: "Garage Pro Haguenau", description: "Plateforme complète pour garagiste avec gestion de rendez-vous et historique véhicules.", sector: "garagiste", city: "Haguenau", isFeatured: false, features: "Historique véhicules,Planning,SMS rappels,Facturation" },
  { title: "Plomberie Martin Strasbourg", description: "Site professionnel pour artisan plombier avec zone d'intervention et urgences 24h.", sector: "plombier", city: "Strasbourg", isFeatured: true, features: "Urgence 24h,Zone d'intervention,Devis gratuit,Galerie photos" },
  { title: "SOS Plombier Épinal", description: "Site d'intervention rapide avec formulaire de demande et tarifs transparents.", sector: "plombier", city: "Épinal", isFeatured: false, features: "Intervention rapide,Tarifs clairs,Formulaire devis,Témoignages" },
  { title: "Élec Plus Colmar", description: "Site vitrine pour électricien avec présentation des services et certifications.", sector: "electricien", city: "Colmar", isFeatured: false, features: "Certifications,Services détaillés,Devis en ligne,Photos chantiers" },
  { title: "Flash Élec Saverne", description: "Plateforme pour électricien avec calculateur de consommation et conseils énergie.", sector: "electricien", city: "Saverne", isFeatured: false, features: "Calculateur énergie,Domotique,LED,Panneaux solaires" },
  { title: "Bois & Style Obernai", description: "Vitrine élégante pour menuisier ébéniste avec portfolio de réalisations sur mesure.", sector: "menuisier", city: "Obernai", isFeatured: true, features: "Portfolio,Sur mesure,Essences de bois,Devis 3D" },
  { title: "Menuiserie Alsace Sélestat", description: "Site pour menuisier spécialisé fenêtres et portes avec configurateur en ligne.", sector: "menuisier", city: "Sélestat", isFeatured: false, features: "Configurateur,Fenêtres,Portes,Isolation" },
  { title: "Toitures Grand Est Nancy", description: "Site professionnel pour couvreur avec visualiseur de toitures et matériaux.", sector: "couvreur", city: "Nancy", isFeatured: false, features: "Visualiseur,Matériaux,Isolation,Garantie décennale" },
  { title: "Couvreur Express Forbach", description: "Site d'urgence toiture avec intervention rapide et devis photo.", sector: "couvreur", city: "Forbach", isFeatured: false, features: "Urgence tempête,Devis photo,Zinguerie,Démoussage" },
  { title: "Jardins d'Alsace Strasbourg", description: "Site vitrine paysagiste avec galerie avant/après et conception 3D de jardins.", sector: "paysagiste", city: "Strasbourg", isFeatured: false, features: "Avant/Après,Conception 3D,Entretien,Arrosage auto" },
  { title: "Vert Espace Lunéville", description: "Plateforme pour paysagiste avec abonnements entretien et conseils saisonniers.", sector: "paysagiste", city: "Lunéville", isFeatured: false, features: "Abonnements,Conseils,Élagage,Clôtures" },
  { title: "Peinture Prestige Metz", description: "Site élégant pour peintre décorateur avec nuancier interactif et simulation couleurs.", sector: "peintre", city: "Metz", isFeatured: false, features: "Nuancier,Simulation couleurs,Décoration,Ravalement" },
  { title: "Colors Pro Wissembourg", description: "Vitrine pour entreprise de peinture avec galerie de chantiers et avis clients.", sector: "peintre", city: "Wissembourg", isFeatured: false, features: "Galerie chantiers,Peinture éco,Papier peint,Enduits" },
  { title: "Garage Alsace Strasbourg", description: "Site complet pour centre auto avec prise de rendez-vous et forfaits entretien.", sector: "garagiste", city: "Strasbourg", isFeatured: false, features: "Forfaits,Pneus,Contrôle technique,Climatisation" },
  { title: "AutoPremium Sarreguemines", description: "Site pour vendeur automobile premium avec visite virtuelle 360° des véhicules.", sector: "vendeur-auto", city: "Sarreguemines", isFeatured: false, features: "Visite 360°,Premium,Livraison,Garantie étendue" },
];

const DEMO_LEADS = [
  { name: "Jean Dupont", email: "jean.dupont@email.com", phone: "0612345678", sector: "plombier", city: "Strasbourg", status: "PENDING", source: "website" },
  { name: "Marie Martin", email: "marie.martin@email.com", phone: "0623456789", sector: "electricien", city: "Colmar", status: "CONTACTED", source: "audit" },
  { name: "Pierre Durand", email: "pierre.durand@email.com", phone: "0634567890", sector: "menuisier", city: "Nancy", status: "QUALIFIED", source: "website" },
];

async function main() {
  console.log("Seeding database...");

  // Clear existing data
  await prisma.portfolio.deleteMany();
  await prisma.lead.deleteMany();
  await prisma.audit.deleteMany();
  await prisma.sector.deleteMany();
  await prisma.city.deleteMany();

  // Seed sectors
  for (const sector of SECTORS) {
    await prisma.sector.create({ data: sector });
  }
  console.log(`Created ${SECTORS.length} sectors`);

  // Seed cities
  for (const city of CITIES) {
    await prisma.city.create({ data: city });
  }
  console.log(`Created ${CITIES.length} cities`);

  // Seed portfolios
  for (const portfolio of PORTFOLIOS) {
    await prisma.portfolio.create({ data: portfolio });
  }
  console.log(`Created ${PORTFOLIOS.length} portfolios`);

  // Seed demo leads
  for (const lead of DEMO_LEADS) {
    await prisma.lead.create({ data: lead });
  }
  console.log(`Created ${DEMO_LEADS.length} demo leads`);

  console.log("Seeding complete!");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
