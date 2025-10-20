import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import numpy as np # Add numpy for easier data handling

# --- 1. INITIALIZATION ---
load_dotenv()
app = FastAPI(
    title="NexusCare API",
    description="API for the NexusCare Ailment Prediction and Explanation Service.",
    version="1.1.0 (Debug Mode)" # Updated version
)

# --- 2. CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. LOAD MACHINE LEARNING MODELS ---
MODEL_PATH = os.path.join("ml_models", "nexuscare_model.pkl")
VECTORIZER_PATH = os.path.join("ml_models", "tfidf_vectorizer.pkl")
model = None
vectorizer = None

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("✅ ML Model and Vectorizer loaded successfully.")
    # Print the model's classes to confirm it's the right one
    print(f"Model classes: {model.classes_}")
except FileNotFoundError:
    print("❌ ERROR: Model or vectorizer not found. Please ensure the .pkl files are in 'ml_models'.")
except Exception as e:
    print(f"❌ ERROR: An unexpected error occurred while loading models: {e}")

# --- 4. INITIALIZE OPENAI CLIENT ---
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- 5. DEFINE DATA MODELS ---
class ClinicalNoteRequest(BaseModel):
    text: str

# --- NEW: Add a probabilities field to the response model ---
class PredictionResponse(BaseModel):
    predicted_ailment: str
    explanation: str
    probabilities: dict[str, float] # This will hold the confidence scores

# --- 6. DEFINE API ENDPOINTS ---
@app.get("/", summary="Root endpoint to check API status")
def read_root():
    return {"status": "NexusCare API is running."}


@app.post("/predict", response_model=PredictionResponse, summary="Predict Ailment and Generate Explanation")
async def predict(request: ClinicalNoteRequest):
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Model not loaded. Check server logs.")

    try:
        # --- Step A: Get the ML Model's Prediction and Probabilities ---
        text_vectorized = vectorizer.transform([request.text])
        
        # Get the prediction
        prediction = model.predict(text_vectorized)[0]
        
        # --- NEW: Get the probabilities for ALL classes ---
        # model.predict_proba returns an array of probabilities for each class
        probabilities_raw = model.predict_proba(text_vectorized)[0]
        
        # Create a user-friendly dictionary of {class_name: probability}
        # We round the probabilities to 4 decimal places for readability
        probabilities_dict = {
            cls: round(prob, 4) for cls, prob in zip(model.classes_, probabilities_raw)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during model prediction: {e}")

    # --- Step B: Generate an Explanation with the LLM (no changes here) ---
    try:
        prompt = f"""
        A machine learning model analyzed a clinical note and predicted the primary ailment is: "{prediction}".
        Based on the full clinical note provided below, please act as a medical expert and write a concise, easy-to-understand explanation (2-3 sentences) for another healthcare professional.
        Your explanation should justify why this prediction is plausible by highlighting the most likely key symptoms, findings, or lab results from the note that support this diagnosis. Do not question the model's prediction, just explain it.
        ---
        Clinical Note:
        {request.text[:4000]} 
        ---
        Explanation:
        """
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful medical expert providing clear explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        explanation = response.choices[0].message.content.strip()
    except Exception as e:
        explanation = f"Could not generate explanation due to an error: {e}"

    # --- Step C: Return the Final Response with the new probabilities ---
    return PredictionResponse(
        predicted_ailment=prediction,
        explanation=explanation,
        probabilities=probabilities_dict
    )