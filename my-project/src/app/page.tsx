import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { HeroSection } from "@/components/home/HeroSection";
import { StatsSection } from "@/components/home/StatsSection";
import { SectorsSection } from "@/components/home/SectorsSection";
import { CitiesSection } from "@/components/home/CitiesSection";
import { TestimonialsSection } from "@/components/home/TestimonialsSection";

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main>
        <HeroSection />
        <StatsSection />
        <SectorsSection />
        <CitiesSection />
        <TestimonialsSection />
      </main>
      <Footer />
    </>
  );
}
