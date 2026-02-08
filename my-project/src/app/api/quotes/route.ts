import { NextResponse } from "next/server";
import { prisma } from "@/lib/db";

export async function POST(request: Request) {
  const body = await request.json();
  const { name, email, phone, sector, city, website, message } = body;

  const lead = await prisma.lead.create({
    data: { name, email, phone, sector, city, website, message, source: "quote" },
  });

  return NextResponse.json({ success: true, leadId: lead.id }, { status: 201 });
}
