import { notFound } from "next/navigation";
import Link from "next/link";
import { prisma } from "@/lib/db";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ProjectMockup } from "@/components/portfolio/ProjectMockup";
import { ProjectDetails } from "@/components/portfolio/ProjectDetails";

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const project = await prisma.portfolio.findUnique({ where: { id } });
  if (!project) return { title: "Projet non trouvé" };
  return {
    title: `${project.title} | Astro Agency`,
    description: project.description,
  };
}

export default async function ProjectPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const project = await prisma.portfolio.findUnique({ where: { id } });
  if (!project) notFound();

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gray-50 py-12">
        <div className="mx-auto max-w-5xl px-4">
          <nav className="mb-6 text-sm text-gray-500">
            <Link href="/" className="hover:text-blue-600">Accueil</Link>
            {" / "}
            <Link href="/realisations" className="hover:text-blue-600">Réalisations</Link>
            {" / "}
            <span className="text-gray-900">{project.title}</span>
          </nav>
          <div className="mb-4 flex items-center gap-3">
            <h1 className="text-3xl font-bold">{project.title}</h1>
            {project.isFeatured && <Badge variant="success">En vedette</Badge>}
          </div>
          <p className="mb-2 text-sm text-gray-500">{project.sector} &bull; {project.city}</p>
          <p className="mb-8 text-gray-600">{project.description}</p>
          <ProjectMockup project={project} />
          <ProjectDetails features={project.features} />
          <div className="mt-8 text-center">
            <Link href="/audit">
              <Button size="lg">Je veux un site comme celui-ci</Button>
            </Link>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
