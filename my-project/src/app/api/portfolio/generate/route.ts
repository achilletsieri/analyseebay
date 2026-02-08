import { NextResponse } from "next/server";
import { prisma } from "@/lib/db";

export async function POST() {
  const portfolios = await prisma.portfolio.findMany();
  const results: { id: string; title: string; status: string }[] = [];

  for (const p of portfolios) {
    // Placeholder: in production, use z-ai-web-dev-sdk to generate images
    const imageUrl = `/portfolio-images/${p.sector}-${p.city.toLowerCase().replace(/\s+/g, "-")}.webp`;
    await prisma.portfolio.update({ where: { id: p.id }, data: { imageUrl } });
    results.push({ id: p.id, title: p.title, status: "generated" });
  }

  return NextResponse.json({ success: true, generated: results.length, results });
}
