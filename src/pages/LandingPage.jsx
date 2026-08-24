import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import FeatureHighlights from '../components/FeatureHighlights';
import HowItWorks from '../components/HowItWorks';
import Footer from '../components/Footer';

export default function LandingPage() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <FeatureHighlights />
        <HowItWorks />
      </main>
      <Footer />
    </>
  );
}
