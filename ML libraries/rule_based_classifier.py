import pandas as pd
import re
import matplotlib.pyplot as plt
from tqdm import tqdm

# Allow progress bars to work with pandas' .apply() method
tqdm.pandas()

# --- Configuration ---
INPUT_FILE = "discharge_summaries.csv"
OUTPUT_FILE = "labeled_training_dataset.csv"
SPLIT_KEYWORD = "Discharge Diagnosis:"

# --- PRIORITY-ORDERED MAPPING ---
# We check for keywords in this specific order. The first match determines the label.
# More severe/specific conditions are placed higher up.
LABEL_MAPPING = {
    # --- Critical & Life-Threatening ---
    'sepsis': 'Sepsis', 'bacteremia': 'Sepsis',
    'stroke': 'Stroke', 'infarct': 'Stroke', 'hemorrhage': 'Stroke', 'sah': 'Stroke', 'cva': 'Stroke',
    'pulmonary embolism': 'Pulmonary Embolism', 'pe': 'Pulmonary Embolism',
    'myocardial infarction': 'Coronary Artery Disease', 'stemi': 'Coronary Artery Disease', 'nstemi': 'Coronary Artery Disease',

    # --- Major Organ System Disease ---
    'heart failure': 'Heart Failure', 'cardiomyopathy': 'Heart Failure', 'chf': 'Heart Failure',
    'coronary artery disease': 'Coronary Artery Disease', 'cad': 'Coronary Artery Disease', 'angina': 'Coronary Artery Disease',
    'atrial fibrillation': 'Atrial Fibrillation', 'a-fib': 'Atrial Fibrillation', 'a fib': 'Atrial Fibrillation', 'flutter': 'Atrial Fibrillation',
    'respiratory failure': 'Respiratory Failure',
    'pneumonia': 'Pneumonia', 'pna': 'Pneumonia',
    'kidney failure': 'Kidney Disease', 'renal': 'Kidney Disease', 'ckd': 'Kidney Disease',
    'cirrhosis': 'Liver Disease', 'hepatic': 'Liver Disease',
    'pancreatitis': 'Pancreatitis',
    'bowel obstruction': 'Bowel Obstruction', 'sbo': 'Bowel Obstruction',
    'gi bleed': 'GI Bleed', 'gastrointestinal bleed': 'GI Bleed',

    # --- Cancer / Oncology ---
    'cancer': 'Cancer', 'carcinoma': 'Cancer', 'metastatic': 'Cancer', 'tumor': 'Cancer', 'mass': 'Cancer',
    'lymphoma': 'Cancer', 'leukemia': 'Cancer', 'melanoma': 'Cancer',
    
    # --- Infection (Non-Sepsis) ---
    'uti': 'Urinary Tract Infection', 'urinary tract infection': 'Urinary Tract Infection', 'urosepsis': 'Urinary Tract Infection', 'pyelonephritis': 'Urinary Tract Infection',
    'cellulitis': 'Cellulitis/Abscess', 'abscess': 'Cellulitis/Abscess',
    'meningitis': 'Meningitis',
    'colitis': 'Colitis',

    # --- Trauma & Musculoskeletal ---
    'fracture': 'Fracture', 'fx': 'Fracture',
    'fall': 'Fall/Trauma', 'trauma': 'Fall/Trauma',
    'osteoarthritis': 'Osteoarthritis', 'oa': 'Osteoarthritis',

    # --- Other Common Conditions ---
    'dvt': 'Deep Vein Thrombosis', 'deep vein thrombosis': 'Deep Vein Thrombosis',
    'seizure': 'Seizure',
    'dementia': 'Dementia',
    'altered mental status': 'Altered Mental Status', 'ams': 'Altered Mental Status', 'encephalopathy': 'Altered Mental Status',
    'copd': 'COPD',
    'gallbladder disease': 'Gallbladder Disease', 'cholecystitis': 'Gallbladder Disease', 'cholelithiasis': 'Gallbladder Disease',
    'diverticulitis': 'Diverticulitis',
    'appendicitis': 'Appendicitis',
    'diabetes': 'Diabetes', 'dm': 'Diabetes', 'dka': 'Diabetes',
    'hypertension': 'Hypertension', 'htn': 'Hypertension',
    'syncope': 'Syncope',
    'anemia': 'Anemia',
    'deceased': 'Deceased/Expired', 'expired': 'Deceased/Expired'
}

def extract_raw_diagnosis(text):
    """Finds the keyword and extracts the first line after it."""
    if not isinstance(text, str): return None
    if SPLIT_KEYWORD in text:
        try:
            parts = text.split(SPLIT_KEYWORD, 1)
            diagnosis_section = parts[1].strip()
            return diagnosis_section.split('\n')[0].strip()
        except: return None
    return None

def classify_diagnosis(raw_diagnosis_text):
    """
    Applies the priority-ordered rule mapping to a single diagnosis string.
    Returns the first category that matches.
    """
    if not isinstance(raw_diagnosis_text, str): return 'Other'
    
    # Standardize the text for matching
    clean_text = raw_diagnosis_text.lower()
    
    # Iterate through the ordered rules
    for keyword, category in LABEL_MAPPING.items():
        if keyword in clean_text:
            return category # Return the first match we find
            
    return 'Other' # If no keywords match, classify as 'Other'

def main():
    """Main function to run the entire data labeling pipeline."""
    try:
        print(f"--- Step 1: Loading '{INPUT_FILE}' ---")
        df = pd.read_csv(INPUT_FILE, usecols=['text'])
        print(f"Successfully loaded {len(df)} records.")
    except Exception as e:
        print(f"ERROR loading CSV: {e}")
        return

    print("\n--- Step 2: Extracting raw diagnosis text from each record ---")
    df['raw_diagnosis'] = df['text'].progress_apply(extract_raw_diagnosis)
    df.dropna(subset=['raw_diagnosis'], inplace=True)
    print(f"Found diagnosis text in {len(df)} records.")

    print("\n--- Step 3: Applying rule-based classifier to create labels ---")
    df['diagnosis'] = df['raw_diagnosis'].progress_apply(classify_diagnosis)

    print("\n--- Distribution of Final Labels ---")
    print(df['diagnosis'].value_counts())

    print("\n--- Step 4: Finalizing and saving the dataset for training ---")
    final_df = df[['text', 'diagnosis']].rename(columns={'text': 'clinical_text'})

    min_samples = 20
    value_counts = final_df['diagnosis'].value_counts()
    to_remove = value_counts[value_counts < min_samples].index
    final_df = final_df[~final_df['diagnosis'].isin(to_remove)]
    
    final_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n--- COMPLETE! ---")
    print(f"Labeled training dataset saved to '{OUTPUT_FILE}'.")
    print(f"This final dataset has {len(final_df)} records and is ready for model training.")
    
    plt.figure(figsize=(10, 10))
    final_df['diagnosis'].value_counts().sort_values().plot(kind='barh')
    plt.title('Final Distribution of Labels for Model Training')
    plt.xlabel('Number of Records')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()