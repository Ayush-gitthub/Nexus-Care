import pandas as pd
import re
import matplotlib.pyplot as plt
from tqdm import tqdm

tqdm.pandas()

# --- Configuration ---
INPUT_FILE = "discharge_summaries.csv"
OUTPUT_FILE = "final_labeled_dataset.csv" # New name for the final output
SPLIT_KEYWORD = "Discharge Diagnosis:"

# --- PRIORITY-ORDERED MAPPING (FINAL VERSION) ---
# This is our most comprehensive mapping, including new categories from the 'Other' analysis.
LABEL_MAPPING_RULES = [
    # --- Critical & Life-Threatening (Highest Priority) ---
    ('deceased', 'Deceased / Expired'), ('expired', 'Deceased / Expired'), ('death', 'Deceased / Expired'),
    ('sepsis', 'Sepsis'), ('bacteremia', 'Sepsis'), ('septic shock', 'Sepsis'),
    ('stroke', 'Stroke'), ('infarct', 'Stroke'), ('hemorrhage', 'Stroke'), ('sah', 'Stroke'), ('cva', 'Stroke'),
    ('subdural hematoma', 'Stroke'), ('sdh', 'Stroke'), ('aneurysm', 'Stroke'), ('tia', 'Stroke'), ('transient ischemic attack', 'Stroke'),
    ('pulmonary embolism', 'Pulmonary Embolism'), ('pe', 'Pulmonary Embolism'), ('pulmonary emboli', 'Pulmonary Embolism'),
    ('myocardial infarction', 'Coronary Artery Disease'), ('stemi', 'Coronary Artery Disease'), ('nstemi', 'Coronary Artery Disease'), ('acute coronary syndrome', 'Coronary Artery Disease'),
    ('cardiogenic shock', 'Heart Failure'),

    # --- Major Organ System Disease ---
    ('heart failure', 'Heart Failure'), ('cardiomyopathy', 'Heart Failure'), ('chf', 'Heart Failure'),
    ('coronary artery disease', 'Coronary Artery Disease'), ('cad', 'Coronary Artery Disease'), ('angina', 'Coronary Artery Disease'), ('cabg', 'Coronary Artery Disease'),
    ('atrial fibrillation', 'Atrial Fibrillation'), ('a-fib', 'Atrial Fibrillation'), ('a fib', 'Atrial Fibrillation'), ('flutter', 'Atrial Fibrillation'),
    ('valvular', 'Valvular Heart Disease'), ('aortic stenosis', 'Valvular Heart Disease'), ('mitral', 'Valvular Heart Disease'), ('aortic insufficiency', 'Valvular Heart Disease'), ('aortic regurgitation', 'Valvular Heart Disease'), ('endocarditis', 'Valvular Heart Disease'),
    ('respiratory failure', 'Respiratory Failure'), ('ards', 'Respiratory Failure'), ('hypoxia', 'Respiratory Failure'),
    ('pneumonia', 'Pneumonia'), ('pna', 'Pneumonia'),
    ('kidney disease', 'Kidney Disease'), ('renal', 'Kidney Disease'), ('ckd', 'Kidney Disease'), ('esrd', 'Kidney Disease'), ('nephrolithiasis', 'Kidney Disease'), ('glomerulonephritis', 'Kidney Disease'),
    ('liver disease', 'Liver Disease'), ('cirrhosis', 'Liver Disease'), ('hepatic', 'Liver Disease'), ('hepatitis', 'Liver Disease'), ('hcv', 'Liver Disease'),
    ('pancreatitis', 'Pancreatitis'),
    ('bowel obstruction', 'Bowel Obstruction'), ('sbo', 'Bowel Obstruction'), ('volvulus', 'Bowel Obstruction'),
    ('gi bleed', 'GI Bleed'), ('gastrointestinal bleed', 'GI Bleed'), ('melena', 'GI Bleed'), ('hematemesis', 'GI Bleed'),

    # --- Cancer / Oncology ---
    ('cancer', 'Cancer'), ('carcinoma', 'Cancer'), ('metastatic', 'Cancer'), ('tumor', 'Cancer'), ('mass', 'Cancer'),
    ('lymphoma', 'Cancer'), ('leukemia', 'Cancer'), ('melanoma', 'Cancer'), ('liposarcoma', 'Cancer'),

    # --- Infection (Non-Sepsis) ---
    ('uti', 'Urinary Tract Infection'), ('urinary tract infection', 'Urinary Tract Infection'), ('urosepsis', 'Urinary Tract Infection'), ('pyelonephritis', 'Urinary Tract Infection'),
    ('cellulitis', 'Cellulitis/Abscess'), ('abscess', 'Cellulitis/Abscess'), ('osteomyelitis', 'Cellulitis/Abscess'),
    ('meningitis', 'Meningitis'),
    ('colitis', 'Colitis'), ('c. diff', 'Colitis'),
    ('influenza', 'Viral/Specific Infection'), ('vzv', 'Viral/Specific Infection'), ('malaria', 'Viral/Specific Infection'), ('syphilis', 'Viral/Specific Infection'), ('pharyngitis', 'Viral/Specific Infection'),

    # --- Trauma & Musculoskeletal ---
    ('fracture', 'Fracture'), ('fx', 'Fracture'),
    ('fall', 'Fall/Trauma'), ('trauma', 'Fall/Trauma'), ('assault', 'Fall/Trauma'), ('gunshot', 'Fall/Trauma'), ('mvc', 'Fall/Trauma'), ('dislocation', 'Fall/Trauma'), ('laceration', 'Fall/Trauma'),
    ('hematoma', 'Hematoma'),('arthritis','arthritis'),
    ('osteoarthritis', 'Osteoarthritis'), ('oa', 'Osteoarthritis'),
    ('herniated disc', 'Spinal/Back Issue'), ('spinal stenosis', 'Spinal/Back Issue'), ('cord compression', 'Spinal/Back Issue'), ('back pain', 'Spinal/Back Issue'),
    ('gout', 'Gout'), ('gouty arthritis', 'Gout'),

    # --- Pregnancy & Gynecological ---
    ('pregnancy', 'Pregnancy/Gynecological'), ('cesarean', 'Pregnancy/Gynecological'), ('fibroid', 'Pregnancy/Gynecological'),
    ('ovarian', 'Pregnancy/Gynecological'), ('ectopic', 'Pregnancy/Gynecological'), ('endometriomas', 'Pregnancy/Gynecological'), ('placenta', 'Pregnancy/Gynecological'),

    # --- Psychiatric Conditions ---
    ('bipolar', 'Psychiatric Condition'), ('schizophrenia', 'Psychiatric Condition'), ('depression', 'Psychiatric Condition'), ('psychosis', 'Psychiatric Condition'), ('anxiety', 'Psychiatric Condition'),
    ('alcohol withdrawal', 'Substance-related'), ('overdose', 'Substance-related'), ('toxicity', 'Substance-related'), ('alcohol abuse', 'Substance-related'),

    # --- Symptom-Based Categories ---
    ('chest pain', 'Chest Pain'),
    ('abdominal pain', 'Abdominal Pain'),
    ('dysphagia', 'Dysphagia'),
    ('dizziness', 'Dizziness / Vertigo'), ('vertigo', 'Dizziness / Vertigo'),
    ('weakness', 'Weakness'),
    ('nausea', 'Nausea / Vomiting'), ('vomiting', 'Nausea / Vomiting'),

    # --- Other Specific Diagnoses ---
    ('hernia', 'Hernia'),
    ('dvt', 'Deep Vein Thrombosis'), ('deep vein thrombosis', 'Deep Vein Thrombosis'), ('thrombus', 'Deep Vein Thrombosis'),
    ('seizure', 'Seizure'),
    ('dementia', 'Dementia'),
    ('altered mental status', 'Altered Mental Status'), ('ams', 'Altered Mental Status'), ('encephalopathy', 'Altered Mental Status'), ('delirium', 'Altered Mental Status'),
    ('copd', 'COPD'),
    ('gallbladder disease', 'Gallbladder Disease'), ('cholecystitis', 'Gallbladder Disease'), ('cholelithiasis', 'Gallbladder Disease'), ('cholangitis', 'Gallbladder Disease'),
    ('diverticulitis', 'Diverticulitis'),
    ('appendicitis', 'Appendicitis'),
    ('diabetes', 'Diabetes'), ('dm', 'Diabetes'), ('dka', 'Diabetes'), ('hypoglycemia', 'Diabetes'),
    ('hypertension', 'Hypertension'), ('htn', 'Hypertension'),
    ('syncope', 'Syncope'),
    ('anemia', 'Anemia'),
    ('gastroenteritis', 'Gastroenteritis'), ('diarrhea', 'Gastroenteritis'),
    ('gastritis', 'Gastritis'), ('gerd', 'Gastritis'),
    ('dehydration', 'Dehydration'),
    ('headache', 'Headache'), ('migraine', 'Headache'),
    ('bradycardia', 'Arrhythmia'), ('tachycardia', 'Arrhythmia'), ('svt', 'Arrhythmia'),
    ('obesity', 'Obesity'),
    ('crohn', 'Inflammatory Bowel Disease'), ('ibd', 'Inflammatory Bowel Disease'),
    ('hyponatremia', 'Electrolyte Imbalance'),
    ('hypothyroidism', 'Endocrine Disorder'),
    ('ulcer', 'Ulcer'),
    ('urinary retention', 'Urinary Retention'),
    ('pleural effusion', 'Pleural Effusion'),
]

def extract_primary_diagnosis(text_block):
    """
    Intelligently extracts the primary diagnosis, handling headers like 'Primary Diagnosis:'.
    """
    if not isinstance(text_block, str): return None
    
    # Define a pattern to find variations of "Primary Diagnosis" and capture what follows
    # This looks for "primary", "principal", etc., followed by any characters, then a colon,
    # and captures the text after the colon on the same line.
    pattern = re.compile(r'(primary|principal|major|final)[\s\w]*:\s*(.*)', re.IGNORECASE)
    
    lines = text_block.split('\n')
    for i, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            # If we find a match and there's text on the same line, use it
            diagnosis_on_line = match.group(2).strip()
            if diagnosis_on_line:
                return diagnosis_on_line
            # If the line is just a header, the diagnosis is likely on the next line
            elif i + 1 < len(lines):
                return lines[i+1].strip()
    
    # Fallback for simple cases: return the first non-empty line
    for line in lines:
        if line.strip():
            return line.strip()
            
    return None


def get_diagnosis_section(text):
    """Splits the text and returns only the section after the main keyword."""
    if not isinstance(text, str): return None
    if SPLIT_KEYWORD in text:
        try:
            return text.split(SPLIT_KEYWORD, 1)[1]
        except: return None
    return None

def classify_diagnosis(raw_diagnosis_text):
    """Applies the priority-ordered rule mapping to a single diagnosis string."""
    if not isinstance(raw_diagnosis_text, str): return 'Other'
    clean_text = raw_diagnosis_text.lower()
    for keyword, category in LABEL_MAPPING_RULES:
        if keyword in clean_text:
            return category
    print(clean_text)
    return 'Other'

def main():
    print(f"--- Step 1: Loading '{INPUT_FILE}' ---")
    df = pd.read_csv(INPUT_FILE, usecols=['text'])
    print(f"Successfully loaded {len(df)} records.")

    print("\n--- Step 2: Extracting diagnosis SECTION from each record ---")
    df['diagnosis_section'] = df['text'].progress_apply(get_diagnosis_section)
    df.dropna(subset=['diagnosis_section'], inplace=True)
    print(f"Found diagnosis section in {len(df)} records.")

    print("\n--- Step 3: Intelligently extracting PRIMARY diagnosis from section ---")
    df['primary_diagnosis_raw'] = df['diagnosis_section'].progress_apply(extract_primary_diagnosis)
    df.dropna(subset=['primary_diagnosis_raw'], inplace=True)
    print(f"Successfully extracted a primary diagnosis from {len(df)} records.")

    print("\n--- Step 4: Applying rule-based classifier to create final labels ---")
    df['diagnosis'] = df['primary_diagnosis_raw'].progress_apply(classify_diagnosis)

    print("\n--- Distribution of Final Labels ---")
    print(df['diagnosis'].value_counts())

    print("\n--- Step 5: Finalizing and saving the dataset for training ---")
    final_df = df[['text', 'diagnosis']].rename(columns={'text': 'clinical_text'})

    min_samples = 5 # We keep this filter to ensure model quality
    value_counts = final_df['diagnosis'].value_counts()
    to_remove = value_counts[value_counts < min_samples].index
    final_df = final_df[~final_df['diagnosis'].isin(to_remove)]
    
    final_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n--- COMPLETE! ---")
    print(f"Labeled training dataset saved to '{OUTPUT_FILE}'.")
    print(f"This final dataset has {len(final_df)} records.")
    
    plt.figure(figsize=(10, 12))
    final_df['diagnosis'].value_counts().sort_values().plot(kind='barh')
    plt.title('Final Distribution of Labels for Model Training')
    plt.xlabel('Number of Records')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()