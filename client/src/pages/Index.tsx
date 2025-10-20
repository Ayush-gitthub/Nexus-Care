import { useState } from "react";
import axios from "axios"; // <-- ADD THIS LINE
import { toast } from "sonner";
import Header from "@/components/Header";
import ClinicalNoteInput from "@/components/ClinicalNoteInput";
import AnalyzeButton from "@/components/AnalyzeButton";
import LoadingSpinner from "@/components/LoadingSpinner";
import ResultsDisplay from "@/components/ResultsDisplay";

// --- ADD THIS LINE ---
// Define the API endpoint URL. In development, it points to your local FastAPI server.
const API_URL = "http://127.0.0.1:8000/predict";

interface AnalysisResults {
  // --- MODIFY THIS INTERFACE TO MATCH THE API RESPONSE ---
  predicted_ailment: string;
  explanation: string;
}

const Index = () => {
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResults | null>(null);

  /**
   * Handle AI analysis by calling the backend API.
   */
  const handleAnalyze = async () => {
    if (!inputText.trim()) {
      toast.error("Please enter a clinical note to analyze");
      return;
    }

    setIsLoading(true);
    setResults(null);

    try {
      // --- REMOVE THE MOCK SIMULATION ---
      // await new Promise((resolve) => 
      //   setTimeout(resolve, 1500 + Math.random() * 1000)
      // );
      // const mockResults: AnalysisResults = { ... };

      // --- ADD THE REAL API CALL ---
      const response = await axios.post<AnalysisResults>(API_URL, {
        text: inputText, // The request body must match what the API expects
      });

      // The 'data' from the response will have our ailment and explanation
      setResults(response.data); 
      toast.success("Analysis complete!");

    } catch (error) {
      console.error("Analysis error:", error);
      // --- ADD MORE SPECIFIC ERROR HANDLING ---
      if (axios.isAxiosError(error) && error.response) {
        // If the API returns a specific error message, show it
        toast.error(`Analysis failed: ${error.response.data.detail || 'Server error'}`);
      } else {
        // For network errors or other issues
        toast.error("Failed to connect to the analysis service. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (value: string) => {
    setInputText(value);
    if (results) {
      setResults(null);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />
      
      <main className="flex-1 container mx-auto px-6 py-12">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Hero section with input */}
          <div className="space-y-4 animate-fade-in">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold text-foreground tracking-tight">
                AI-Powered Clinical Analysis
              </h2>
              <p className="text-base text-muted-foreground max-w-2xl">
                Paste a clinical discharge summary below and our AI will analyze it to predict 
                the primary ailment and provide a detailed explanation.
              </p>
            </div>
            
            <ClinicalNoteInput
              value={inputText}
              onChange={handleInputChange}
              disabled={isLoading}
            />
            
            <div className="flex justify-center pt-2">
              <AnalyzeButton
                onClick={handleAnalyze}
                disabled={!inputText.trim() || isLoading}
                isLoading={isLoading}
              />
            </div>
          </div>

          {/* Loading state */}
          {isLoading && <LoadingSpinner />}

          {/* Results */}
          {results && !isLoading && (
            // --- UPDATE PROPS TO MATCH THE NEW INTERFACE ---
            <ResultsDisplay
              ailment={results.predicted_ailment}
              explanation={results.explanation}
            />
          )}

          {/* ... The rest of your component remains the same ... */}
          {!results && !isLoading && !inputText && (
             <div className="py-12 text-center space-y-3 animate-fade-in">
               <div className="w-16 h-16 mx-auto rounded-full bg-muted flex items-center justify-center">
                 <span className="text-2xl">🏥</span>
               </div>
               <p className="text-sm text-muted-foreground max-w-md mx-auto">
                 Get started by pasting a clinical discharge summary above. 
                 Our AI will analyze it and provide insights in seconds.
               </p>
             </div>
           )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card">
        <div className="container mx-auto px-6 py-6">
          <p className="text-center text-sm text-muted-foreground">
            NexusCare AI Assistant • Built with care for healthcare professionals
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;