import { NextResponse } from "next/server";
import { prisma } from "@/lib/db";

export async function GET() {
  const audits = await prisma.audit.findMany({ orderBy: { createdAt: "desc" } });
  return NextResponse.json(audits);
}

export async function POST(request: Request) {
  const body = await request.json();
  const audit = await prisma.audit.create({ data: body });
  return NextResponse.json(audit, { status: 201 });
}
