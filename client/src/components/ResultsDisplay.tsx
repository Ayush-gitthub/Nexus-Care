import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertCircle, FileText } from "lucide-react";

interface ResultsDisplayProps {
  ailment: string;
  explanation: string;
}

/**
 * ResultsDisplay Component
 * 
 * Presents AI analysis results in a clear, trustworthy manner.
 * Design choices:
 * - Two-card layout: Clear hierarchy and separation of concerns
 * - Ailment card first: Most important info gets priority
 * - Icons: Visual anchors for quick scanning
 * - Generous spacing: Reduces cognitive load
 * - Rounded corners: Friendly, approachable
 * - Soft shadows: Cards feel elevated but not floating
 * - Smooth entrance: Results fade in naturally
 */
const ResultsDisplay = ({ ailment, explanation }: ResultsDisplayProps) => {
  return (
    <div className="w-full space-y-6 animate-fade-in">
      {/* Primary card - Predicted Ailment */}
      <Card className="border-2 border-primary/20 shadow-card hover:shadow-lg transition-all duration-300">
        <CardHeader className="space-y-2">
          <div className="flex items-center gap-2">
            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
              <AlertCircle className="w-5 h-5 text-primary" strokeWidth={2.5} />
            </div>
            <CardTitle className="text-xl">Predicted Ailment</CardTitle>
          </div>
          <CardDescription className="text-sm">
            Based on the clinical notes provided
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="p-4 rounded-lg bg-accent/50 border border-primary/10">
            <p className="text-lg font-semibold text-foreground leading-relaxed">
              {ailment}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Secondary card - AI Explanation */}
      <Card className="shadow-soft hover:shadow-card transition-all duration-300">
        <CardHeader className="space-y-2">
          <div className="flex items-center gap-2">
            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-muted">
              <FileText className="w-5 h-5 text-foreground/70" strokeWidth={2} />
            </div>
            <CardTitle className="text-xl">AI Explanation</CardTitle>
          </div>
          <CardDescription className="text-sm">
            How we arrived at this prediction
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="prose prose-sm max-w-none">
            <p className="text-base text-foreground/80 leading-relaxed whitespace-pre-wrap">
              {explanation}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Disclaimer for medical context */}
      <div className="p-4 rounded-lg bg-muted/50 border border-border">
        <p className="text-xs text-muted-foreground text-center">
          <strong className="font-medium">Disclaimer:</strong> This AI analysis is for informational purposes only 
          and should not replace professional medical diagnosis or treatment.
        </p>
      </div>
    </div>
  );
};

export default ResultsDisplay;
