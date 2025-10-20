import { Activity } from "lucide-react";

/**
 * Header Component
 * 
 * Simple, clean header that establishes trust and professionalism.
 * - Activity icon: Represents health/medical monitoring in a friendly way
 * - Teal color: Calming, medical association, trustworthy
 * - Spacing: Generous padding for breathing room
 */
const Header = () => {
  return (
    <header className="w-full border-b border-border bg-card">
      <div className="container mx-auto px-6 py-5">
        <div className="flex items-center gap-3">
          {/* Icon with subtle teal glow for brand recognition */}
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-primary/10">
            <Activity className="w-6 h-6 text-primary" strokeWidth={2.5} />
          </div>
          
          {/* Brand name with clean typography */}
          <h1 className="text-2xl font-semibold text-foreground tracking-tight">
            NexusCare
          </h1>
          
          {/* Subtle badge to communicate AI assistance */}
          <span className="ml-2 px-2.5 py-1 text-xs font-medium text-primary bg-primary/10 rounded-full">
            AI Assistant
          </span>
        </div>
      </div>
    </header>
  );
};

export default Header;
