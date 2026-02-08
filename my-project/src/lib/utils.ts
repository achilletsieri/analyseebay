import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getScoreBadgeColor(score: number): string {
  if (score < 50) return "bg-red-100 text-red-800";
  if (score < 75) return "bg-orange-100 text-orange-800";
  return "bg-green-100 text-green-800";
}

export function formatDate(date: Date | string): string {
  return new Date(date).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
