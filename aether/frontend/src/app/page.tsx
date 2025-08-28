import HeroSection from '@/components/HeroSection'
import Navigation from '@/components/Navigation'
import FeaturesSection from '@/components/FeaturesSection'
import PricingSection from '@/components/PricingSection'
import InteractiveDemo from '@/components/InteractiveDemo'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation />
      <HeroSection />
      <FeaturesSection />
      <InteractiveDemo />
      <PricingSection />
      <Footer />
    </main>
  )
}