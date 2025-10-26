import { useState } from "react";
import axios from "axios";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";

// --- Import your custom components ---
import LiquidEther from "@/components/LiquidEther";
import TextTrail from "@/components/TextTrail";
import TiltedCard from "@/components/TiltedCard";

// --- Assuming you have these basic components ---
// If not, I've included simple versions below this main component
import Header from "@/components/Header";
import ClinicalNoteInput from "@/components/ClinicalNoteInput";
import AnalyzeButton from "@/components/AnalyzeButton";
import LoadingSpinner from "@/components/LoadingSpinner";
import ResultsDisplay from "@/components/ResultsDisplay";

const API_URL = "http://127.0.0.1:8000/predict";

interface AnalysisResults {
  predicted_ailment: string;
  explanation: string;
}

const Index = () => {
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResults | null>(null);

  const handleAnalyze = async () => { /* ... (your function remains the same) ... */ };
  const handleInputChange = (value: string) => { /* ... (your function remains the same) ... */ };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', backgroundColor: '#0D1117', color: 'white', position: 'relative' }}>
      
      {/* --- BACKGROUND: LiquidEther --- */}
      <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: -1, opacity: 0.3 }}>
          <LiquidEther
    colors={[ '#5227FF', '#FF9FFC', '#B19EEF' ]}
    mouseForce={20}
    cursorSize={100}
    isViscous={false}
    viscous={30}
    iterationsViscous={32}
    iterationsPoisson={32}
    resolution={0.5}
    isBounce={false}
    autoDemo={true}
    autoSpeed={0.5}
    autoIntensity={2.2}
    takeoverDuration={0.25}
    autoResumeDelay={3000}
    autoRampDuration={0.6}
  />
      </div>

      <Header />
      
      <main style={{ flex: 1, width: '100%', maxWidth: '896px', margin: '0 auto', padding: '48px 24px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
          
          <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {/* --- TITLE: TextTrail --- */}
            <TextTrail 
              text="NexusCare AI"
              textColor="#ffffff"
              backgroundColor="transparent"
              noiseScale={0.001}
            />
            <p style={{ fontSize: '1.125rem', color: '#8892b0', maxWidth: '42rem', margin: '0 auto' }}>
              Paste a clinical discharge summary below. Our AI will predict the primary ailment and provide a detailed explanation.
            </p>
          </div>
          
          <ClinicalNoteInput value={inputText} onChange={handleInputChange} disabled={isLoading} />
          
          <div style={{ display: 'flex', justifyContent: 'center', paddingTop: '8px' }}>
            <AnalyzeButton onClick={handleAnalyze} disabled={!inputText.trim() || isLoading} isLoading={isLoading} />
          </div>

          <AnimatePresence>
            {isLoading && <LoadingSpinner />}
            
            {results && !isLoading && (
              // --- RESULTS: TiltedCard ---
              <TiltedCard
                containerHeight="auto"
                containerWidth="100%"
                rotateAmplitude={8}
                scaleOnHover={1.03}
                displayOverlayContent={true}
                showTooltip={false}
                overlayContent={
                  <ResultsDisplay
                    ailment={results.predicted_ailment}
                    explanation={results.explanation}
                  />
                }
              />
            )}
          </AnimatePresence>
        </div>
      </main>

      <footer style={{ borderTop: '1px solid rgba(255, 255, 255, 0.1)'}}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '24px' }}>
          <p style={{ textAlign: 'center', fontSize: '0.875rem', color: '#8892b0' }}>
            NexusCare AI Assistant • For informational purposes only.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;

// --- If you don't have these components, here are simple, styled versions ---
// You can create these as separate files in your /components folder.

/*
// src/components/Header.tsx
const Header = () => (
  <header style={{ padding: '1rem 2rem', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
    <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>NexusCare</h1>
  </header>
);

// src/components/ClinicalNoteInput.tsx
const ClinicalNoteInput = ({ value, onChange, disabled }) => (
  <textarea
    value={value}
    onChange={(e) => onChange(e.target.value)}
    disabled={disabled}
    placeholder="Paste the clinical discharge summary here..."
    style={{
      width: '100%',
      minHeight: '250px',
      padding: '1rem',
      borderRadius: '12px',
      border: '1px solid #30363d',
      backgroundColor: '#0D1117',
      color: 'white',
      fontSize: '1rem',
      resize: 'vertical'
    }}
  />
);

// src/components/AnalyzeButton.tsx
const AnalyzeButton = ({ onClick, disabled, isLoading }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    style={{
      padding: '0.75rem 1.5rem',
      borderRadius: '999px',
      border: 'none',
      backgroundColor: isLoading ? '#008075' : '#00a99d',
      color: 'white',
      fontSize: '1rem',
      fontWeight: '600',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.6 : 1,
      transition: 'background-color 0.2s'
    }}
  >
    {isLoading ? 'Analyzing...' : 'Analyze with AI'}
  </button>
);

// src/components/LoadingSpinner.tsx
const LoadingSpinner = () => <div style={{ textAlign: 'center', padding: '2rem' }}>Loading results...</div>;

// src/components/ResultsDisplay.tsx
const ResultsDisplay = ({ ailment, explanation }) => (
  <div style={{ backgroundColor: 'rgba(255, 255, 255, 0.05)', padding: '2rem', borderRadius: '16px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
    <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>Predicted Ailment:</h3>
    <p style={{ fontSize: '1.5rem', color: '#58a6ff', margin: '0.5rem 0 1.5rem 0' }}>{ailment}</p>
    <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>AI Explanation:</h3>
    <p style={{ color: '#c9d1d9', lineHeight: 1.6 }}>{explanation}</p>
  </div>
);
*/