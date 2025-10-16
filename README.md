
# NexusCare: AI-Powered Clinical Diagnosis Assistant

[![Status](https://img.shields.io/badge/status-in%20development-green)](https://github.com/your-username/NexusCare)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

NexusCare is an intelligent web application designed to assist healthcare professionals by rapidly analyzing unstructured clinical discharge summaries. It uses a machine learning model to predict a primary patient ailment and leverages a Large Language Model (LLM) to provide a clear, concise explanation for its prediction, bridging the gap between complex data and actionable insights.

## Demo

*(Here you can add a GIF of the final application in action. A great demo would show pasting a clinical note, clicking "Analyze", and seeing the predicted diagnosis and the AI-generated explanation appear.)*

![NexusCare Demo GIF Placeholder](https://user-images.githubusercontent.com/10940574/203621852-5317b52c-5a23-452f-b40b-55442a8b3879.gif)
*(Replace this with your actual demo GIF)*

---

## The Problem

Clinical notes, such as discharge summaries, are dense with critical information but are often unstructured and time-consuming to parse. This can create a bottleneck for clinicians, reviewers, and researchers who need to quickly ascertain a patient's primary condition.

## The Solution

NexusCare provides a clean interface to an NLP pipeline that:
1.  **Reads** a complex, free-text clinical note.
2.  **Predicts** the primary ailment using a trained classification model.
3.  **Explains** the reasoning behind the prediction in natural language using the OpenAI API.

This turns a wall of text into a structured prediction with a justification, saving valuable time and effort.

---

## Core Features

-   **🤖 Ailment Prediction:** A Scikit-learn model trained on 999 real-world (anonymized) discharge summaries to perform multi-class text classification.
-   **💡 Explainable AI (XAI):** Integration with OpenAI's GPT models to provide human-readable explanations for *why* a certain diagnosis was predicted, enhancing trust and transparency.
-   **🌐 Modern Web Interface:** A clean, responsive, and easy-to-use interface built with React.
-   **⚡️ Fast & Scalable Backend:** An asynchronous API built with FastAPI (Python) ensures high performance.

---

## Tech Stack & Architecture

The project is built with a modern, decoupled architecture.

-   **Frontend:** React (with Vite), Axios, TailwindCSS
-   **Backend:** FastAPI (Python), Uvicorn
-   **Machine Learning:** Scikit-learn, Pandas, LIME
-   **AI Explanation:** OpenAI (GPT-4 / GPT-3.5-Turbo)
-   **Deployment:** Docker, Vercel (Frontend), Render (Backend)

### System Architecture

```
+----------------+      +-----------------------+      +----------------------+
|   User (UI)    |      |      FastAPI API      |      |   Machine Learning   |
|  (React App)   |----->| (Hosted on Render)    |----->|  (Scikit-learn Model)|
+----------------+      +-----------------------+      +----------------------+
                             |
                             |
                             v
                       +----------------------+
                       |  OpenAI API Service  |
                       | (For Explanations)   |
                       +----------------------+
```

---

## Getting Started

Follow these instructions to get a local copy up and running for development and testing.

### Prerequisites

-   Python 3.8+
-   Node.js v16+ and npm/yarn
-   Git
-   An OpenAI API Key

### Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/NexusCare.git
cd NexusCare
```

**2. Backend Setup:**
```bash
# Navigate to the backend directory
cd backend

# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file for your secret keys
touch .env
```
Inside the `.env` file, add your OpenAI API key:
```
OPENAI_API_KEY="sk-YourSecretKeyHere"
```

**3. Frontend Setup:**
```bash
# Navigate to the frontend directory from the root
cd frontend

# Install dependencies
npm install
```

### Running the Application

You will need to run the backend and frontend in separate terminals.

**1. Run the Backend Server:**
```bash
# In the /backend directory
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. You can test it at `http://localhost:8000/docs`.

**2. Run the Frontend Development Server:**
```bash
# In the /frontend directory
npm run dev
```
The React application will be available at `http://localhost:5173` (or another port if 5173 is busy).

---

## Project Structure

```
NexusCare/
├── backend/
│   ├── .env              # Secret keys (not committed)
│   ├── main.py           # FastAPI application entrypoint
│   ├── requirements.txt  # Python dependencies
│   ├── models/           # Saved ML model (e.g., model.pkl)
│   └── core/             # Core logic (prediction, openai calls)
│
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.jsx       # Main application component
│   │   └── index.css     # Styling
│   ├── package.json      # Node.js dependencies
│   └── vite.config.js    # Vite configuration
│
├── data_processing/
│   ├── parse_data.py     # Script to parse raw text files
│   └── clean_labels.py   # Script to clean and standardize labels
│
└── README.md             # This file```

---

## Future Work (Roadmap)

-   [ ] **Advanced NLP Models:** Transition from TF-IDF to a transformer-based model like `BioBERT` or `ClinicalBERT` for higher accuracy.
-   [ ] **User Authentication:** Add user accounts to save and track analysis history.
-   [ ] **Batch Processing:** Allow users to upload multiple files for batch analysis.
-   [ ] **Enhanced Explanations:** Use SHAP in addition to LIME for more robust feature importance to feed into the LLM prompt.
-   [ ] **CI/CD Pipeline:** Set up GitHub Actions for automated testing and deployment.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
