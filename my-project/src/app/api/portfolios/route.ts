import { NextResponse } from "next/server";
import { prisma } from "@/lib/db";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const sector = searchParams.get("sector");
  const featured = searchParams.get("featured");

  const where: Record<string, unknown> = {};
  if (sector && sector !== "all") where.sector = sector;
  if (featured === "true") where.isFeatured = true;

  const portfolios = await prisma.portfolio.findMany({ where, orderBy: { createdAt: "desc" } });
  return NextResponse.json(portfolios);
}
