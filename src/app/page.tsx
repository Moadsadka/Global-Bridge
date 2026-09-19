import { Nav } from "@/components/Nav";
import { Hero } from "@/components/Hero";
import { ServiceCards } from "@/components/ServiceCards";
import { FeatureBlock } from "@/components/FeatureBlock";
import { StatsRow } from "@/components/StatsRow";
import { ImageBreak } from "@/components/ImageBreak";
import { SocialProof } from "@/components/SocialProof";
import { FinalCta } from "@/components/FinalCta";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Nav />
      <main className="flex-1">
        <Hero />
        <ServiceCards />
        <FeatureBlock />
        <StatsRow />
        <ImageBreak />
        <SocialProof />
        <FinalCta />
      </main>
      <Footer />
    </>
  );
}
