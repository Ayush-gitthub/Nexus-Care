import { Loader2 } from "lucide-react";

/**
 * LoadingSpinner Component
 * 
 * Elegant loading state that feels calm and reassuring.
 * Design choices:
 * - Spinning icon: Clear indication of processing
 * - Teal color: Maintains brand consistency
 * - Soft pulse: Adds life without being distracting
 * - Descriptive text: Reduces anxiety by explaining what's happening
 * - Centered layout: Natural focal point
 */
const LoadingSpinner = () => {
  return (
    <div className="w-full py-16 flex flex-col items-center justify-center gap-4 animate-fade-in">
      {/* Spinning loader with soft glow */}
      <div className="relative">
        <Loader2 
          className="w-12 h-12 text-primary animate-spin" 
          strokeWidth={2.5}
        />
        {/* Subtle pulsing background for depth */}
        <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl animate-pulse-soft" />
      </div>
      
      {/* Reassuring message */}
      <div className="text-center space-y-1">
        <p className="text-base font-medium text-foreground">
          Analyzing clinical notes...
        </p>
        <p className="text-sm text-muted-foreground">
          Our AI is carefully reviewing the information
        </p>
      </div>
      
      {/* Progress dots for visual interest */}
      <div className="flex gap-2">
        <div className="w-2 h-2 bg-primary/40 rounded-full animate-pulse-soft" style={{ animationDelay: '0ms' }} />
        <div className="w-2 h-2 bg-primary/40 rounded-full animate-pulse-soft" style={{ animationDelay: '200ms' }} />
        <div className="w-2 h-2 bg-primary/40 rounded-full animate-pulse-soft" style={{ animationDelay: '400ms' }} />
      </div>
    </div>
  );
};

export default LoadingSpinner;
