import { Textarea } from "@/components/ui/textarea";
import { FileText } from "lucide-react";

interface ClinicalNoteInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

/**
 * ClinicalNoteInput Component
 * 
 * The hero of the interface - designed to be inviting and easy to use.
 * Design choices:
 * - Large size: Makes it clear this is the main action
 * - Soft focus ring: Calming teal glow on focus
 * - Icon: Friendly file icon to reinforce what goes here
 * - Placeholder: Clear, gentle guidance
 * - Min height: Comfortable for pasting long notes
 */
const ClinicalNoteInput = ({ value, onChange, disabled }: ClinicalNoteInputProps) => {
  return (
    <div className="w-full space-y-3">
      {/* Label with icon for clear context */}
      <div className="flex items-center gap-2">
        <FileText className="w-5 h-5 text-primary" strokeWidth={2} />
        <label 
          htmlFor="clinical-note" 
          className="text-sm font-medium text-foreground"
        >
          Clinical Discharge Summary
        </label>
      </div>
      
      {/* Main textarea with lovable styling */}
      <Textarea
        id="clinical-note"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Paste the clinical discharge summary here...

Example: Patient presented with acute chest pain radiating to left arm. ECG showed ST elevation. Diagnosed with acute myocardial infarction..."
        className="min-h-[320px] text-base leading-relaxed resize-none 
                   shadow-soft hover:shadow-card transition-all duration-300
                   focus:shadow-card focus:border-primary/50
                   disabled:opacity-50 disabled:cursor-not-allowed
                   placeholder:text-muted-foreground/60"
      />
      
      {/* Character count for user feedback */}
      <p className="text-xs text-muted-foreground text-right">
        {value.length} characters
      </p>
    </div>
  );
};

export default ClinicalNoteInput;
