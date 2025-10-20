import { Button } from "@/components/ui/button";
import { Sparkles } from "lucide-react";

interface AnalyzeButtonProps {
  onClick: () => void;
  disabled: boolean;
  isLoading: boolean;
}

/**
 * AnalyzeButton Component
 * 
 * The primary CTA - designed to feel satisfying and trustworthy.
 * Design choices:
 * - Gradient background: Adds depth and premium feel
 * - Hover lift: Physical feedback that it's clickable
 * - Subtle glow: Premium, high-tech feel
 * - Sparkles icon: Represents AI magic in a friendly way
 * - Disabled state: Clear visual feedback
 * - Size: Large enough to be prominent but not overwhelming
 */
const AnalyzeButton = ({ onClick, disabled, isLoading }: AnalyzeButtonProps) => {
  return (
    <Button
      onClick={onClick}
      disabled={disabled}
      size="lg"
      className="w-full sm:w-auto min-w-[200px] h-12 text-base font-semibold
                 bg-primary hover:bg-primary-hover
                 shadow-soft hover:shadow-card
                 transition-all duration-300
                 hover:-translate-y-0.5
                 active:translate-y-0
                 disabled:opacity-50 disabled:cursor-not-allowed
                 disabled:hover:translate-y-0
                 group relative overflow-hidden"
    >
      {/* Subtle gradient overlay for depth */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent 
                      opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      {/* Button content */}
      <div className="relative flex items-center gap-2">
        <Sparkles 
          className={`w-5 h-5 ${isLoading ? 'animate-pulse-soft' : 'group-hover:rotate-12 transition-transform duration-300'}`} 
        />
        <span>
          {isLoading ? 'Analyzing...' : 'Analyze with AI'}
        </span>
      </div>
    </Button>
  );
};

export default AnalyzeButton;
