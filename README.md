# NexusCare: AI-Powered Clinical Diagnosis Assistant

[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/Ayush-gitthub/Nexus-Care)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

NexusCare is a full-stack web application designed to assist healthcare professionals by rapidly analyzing unstructured clinical discharge summaries. It uses a custom-trained machine learning model to predict a patient's primary ailment and leverages the OpenAI API to provide a clear, concise explanation for its prediction, bridging the gap between complex data and actionable insights.

## Live Demo & Screenshots

Here is the application in action, from input to intelligent analysis.

| Input Interface                                        | Analysis Results                                            |
| ------------------------------------------------------ | ----------------------------------------------------------- |
|   |     |

*(A live demo GIF would be a great addition here to show the smooth user experience)*

---

## Key Features

-   **🤖 Custom-Trained ML Model:** Predicts from over 20 distinct clinical categories based on patterns learned from real-world (anonymized) medical notes.
-   **💡 Explainable AI (XAI):** Integrates with OpenAI's GPT-3.5-Turbo to provide human-readable explanations for *why* a certain diagnosis was predicted, enhancing trust and transparency.
-   **🌐 Modern Web Interface:** A clean, responsive, and intuitive interface built with React, Vite, and Tailwind CSS.
-   **⚡️ High-Performance Backend:** A robust and asynchronous API built with FastAPI (Python) ensures fast and reliable processing.
-   **🔒 Secure by Design:** Follows best practices by keeping sensitive API keys out of version control using a `.gitignore` and environment variables.

---

## The Machine Learning Model

The core of NexusCare is a custom text classification model built with a focus on data quality.

-   **Data Labeling:** A sophisticated **rule-based classifier** with a priority-ordered keyword mapping was developed to label the raw text data, ensuring high-quality, consistent training labels.
-   **Feature Extraction:** The clinical text was vectorized using `TfidfVectorizer`, considering both single words and two-word phrases (`ngram_range=(1,2)`) to capture more context.
-   **Algorithm:** A **Logistic Regression** model was trained using Scikit-learn. The `class_weight='balanced'` parameter was used to handle the natural class imbalance in the medical data.
-   **Performance:** The model achieved a promising baseline **accuracy of ~58%** on the multi-class problem. It demonstrates particularly strong **recall (>80%)** for critical and distinct conditions like **Coronary Artery Disease** and **Pregnancy/Gynecological** issues, proving its ability to identify key patterns in unseen data.

---

## Tech Stack & Architecture

-   **Frontend:** React, Vite, TypeScript, Tailwind CSS, Axios
-   **Backend:** FastAPI (Python), Uvicorn
-   **Machine Learning:** Scikit-learn, Pandas, Joblib
-   **AI Explanation:** OpenAI (GPT-3.5-Turbo)
-   **Deployment:** Designed for containerization (Docker) and deployment on services like Render (Backend) and Vercel (Frontend).

---

## Local Setup & Installation

Follow these instructions to get a local copy up and running.

### Prerequisites
-   Python 3.8+
-   Node.js v16+ and npm/yarn
-   Git
-   An OpenAI API Key

### 1. Clone the Repository
```bash
git clone https://github.com/Ayush-gitthub/Nexus-Care.git
cd Nexus-Care```

### 2. Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # (You may need to create this file first)
# Or run: pip install "fastapi[all]" openai python-dotenv scikit-learn

# Create a .env file for your secret keys
touch .env
```
Inside the `backend/.env` file, add your OpenAI API key:
```
OPENAI_API_KEY="sk-YourSecretKeyHere"
```

### 3. Frontend Setup
```bash
# Navigate to the frontend directory from the root
cd ../frontend # Make sure you go back to the root first

# Install dependencies
npm install
```

### 4. Running the Application
You will need two separate terminals to run the backend and frontend.

**Terminal 1: Start the Backend**
```bash
# In the /backend directory with its venv active
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

**Terminal 2: Start the Frontend**
```bash
# In the /frontend directory
npm run dev
```The React app will be available at `http://localhost:5173`.

---

## Project Structure
```
Nexus-Care/
├── .gitignore                # Crucial for ignoring secrets and node_modules
├── backend/
│   ├── ml_models/
│   │   ├── nexuscare_model.pkl   # The trained ML model
│   │   └── tfidf_vectorizer.pkl  # The trained vectorizer
│   ├── .env                  # Stores the secret API key (NEVER COMMIT)
│   ├── main.py               # The FastAPI application
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── ML libraries/             # Your data processing and training scripts
│   ├── rule_based_classifier.py
│   ├── train_model.py
│   └── ...
│
└── README.md                 # This file
```

---

## Future Work (Roadmap)
-   [ ] **Improve Model:** Transition from TF-IDF to a transformer-based model like `BioBERT` for higher accuracy and better contextual understanding.
-   [ ] **User Authentication:** Add user accounts to save and track analysis history.
-   [x] **Robust Error Handling:** Enhance frontend and backend error handling for a smoother user experience. *(Partially done)*
-   [ ] **CI/CD Pipeline:** Set up GitHub Actions for automated testing and deployment.
-   [ ] **Containerize:** Create a `Dockerfile` for the backend to simplify deployment.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
