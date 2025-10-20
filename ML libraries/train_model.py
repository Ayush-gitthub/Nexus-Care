import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# --- Configuration ---
INPUT_FILE = "final_labeled_dataset.csv" # Our final, high-quality dataset
MODEL_OUTPUT_PATH = "nexuscare_model.pkl"
VECTORIZER_OUTPUT_PATH = "tfidf_vectorizer.pkl"

def train_model():
    """
    Loads the cleaned data, trains a multi-class text classification model,
    evaluates its performance, and saves the final model artifacts.
    """
    # --- 1. Load Data ---
    print("--- Step 1: Loading and Preparing Data ---")
    try:
        df = pd.read_csv(INPUT_FILE)
        # Ensure there are no empty rows which can cause errors
        df.dropna(subset=['clinical_text', 'diagnosis'], inplace=True)
    except FileNotFoundError:
        print(f"ERROR: The file '{INPUT_FILE}' was not found.")
        print("Please ensure the final labeled dataset exists.")
        return

    print("Final distribution of labels being used for training:")
    print(df['diagnosis'].value_counts())
    
    X = df['clinical_text']
    y = df['diagnosis']

    # --- 2. Split Data for Training and Testing ---
    # We'll use 75% for training and 25% for testing.
    # stratify=y is crucial for imbalanced datasets. It ensures that the
    # proportion of each diagnosis is the same in both the train and test sets.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    print(f"\nData split complete: {len(X_train)} training samples, {len(X_test)} testing samples.")

    # --- 3. Vectorize Text ---
    print("\n--- Step 2: Vectorizing Text using TF-IDF ---")
    # TF-IDF converts text into numerical data based on word frequency.
    # stop_words='english' ignores common words like 'the', 'is', 'a'.
    # ngram_range=(1, 2) lets the model consider both single words ("stroke") and two-word phrases ("atrial fibrillation").
    vectorizer = TfidfVectorizer(stop_words='english', max_features=7000, ngram_range=(1, 2))
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print("Text vectorization complete.")

    # --- 4. Train the Machine Learning Model ---
    print("\n--- Step 3: Training the Logistic Regression Model ---")
    # class_weight='balanced' is the most important parameter here. It automatically adjusts
    # for the imbalance in our data, giving more weight to less frequent categories.
    model = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
    model.fit(X_train_tfidf, y_train)
    print("Model training complete.")

    # --- 5. Evaluate Model Performance ---
    print("\n--- Step 4: Evaluating Model Performance on Unseen Test Data ---")
    y_pred = model.predict(X_test_tfidf)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nOverall Model Accuracy: {accuracy:.4f}")
    
    print("\n--- Classification Report ---")
    # This report is the model's "report card".
    # Precision: Of all the times it predicted a diagnosis, how often was it correct?
    # Recall: Of all the actual instances of a diagnosis, how many did it find?
    # F1-Score: A balanced measure of Precision and Recall.
    print(classification_report(y_test, y_pred, zero_division=0))

    # --- 6. Save the Final Model and Vectorizer ---
    print("\n--- Step 5: Saving Model and Vectorizer to Disk ---")
    joblib.dump(model, MODEL_OUTPUT_PATH)
    joblib.dump(vectorizer, VECTORIZER_OUTPUT_PATH)
    print(f"Model saved to: {MODEL_OUTPUT_PATH}")
    print(f"Vectorizer saved to: {VECTORIZER_OUTPUT_PATH}")
    print("\n--- TRAINING PIPELINE COMPLETE! ---")

if __name__ == "__main__":
    train_model()