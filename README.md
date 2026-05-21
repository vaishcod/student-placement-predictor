# CareerLens AI: Advanced Placement Predictor & Career Roadmap Architect

CareerLens AI is a professional, full-stack career readiness platform. It bridges the gap between predictive ML diagnostics and actionable career pathing by providing real-time placement prediction, automated resume parsing, and personalized 4-week learning roadmaps.

## 🚀 Key Features

1. **AI Resume Parser**: Upload a PDF or plain text resume; the system extracts key metrics (CGPA, skills, projects, internships, and communication ratings) via the Gemini API.
2. **Predictive Analytics Engine**: Driven by an optimized Random Forest Classifier trained on synthetic student profile data, predicting job placement probability.
3. **What-If Simulation Sandbox**: A dynamic playground where users can visually estimate placement probability gains by mastering recommended skills.
4. **Custom 4-Week Roadmaps**: The app performs a skill gap analysis against role requirements (e.g., Software Engineer, Data Scientist, AI/ML Engineer, Web Developer) and builds weekly study blocks with concrete tasks and curated free study references using Gemini.

---

## 🛠️ Tech Stack

- **Frontend**: Next.js 14+ (App Router), Tailwind CSS v4, Lucide React, Framer Motion (for animations).
- **Backend**: FastAPI (Python 3.10+), Uvicorn.
- **ML & Data Sciences**: Scikit-Learn, Pandas, NumPy.
- **AI Integrations**: Gemini API (via `google-generativeai`).

---

## 📂 Project Structure

```
placement_predictor/
│
├── backend/
│   ├── main.py                  # FastAPI Application router & controller
│   ├── data_gen.py              # Synthetic placement dataset generator (1500+ rows)
│   ├── train_model.py           # Trains the Random Forest placement model
│   ├── placement_model.pkl      # Saved trained model
│   └── utils/
│       ├── resume_parser.py     # Extracts PDF text and uses Gemini to structure it
│       └── roadmap_generator.py # Generates week-by-week roadmaps using Gemini
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── globals.css      # Custom styling sheets
│   │       ├── layout.tsx       # Metadata & fonts wrapping
│   │       └── page.tsx         # Dashboard UI & React State Engine
│   └── package.json
│
├── .env.example                 # Environment variables reference template
└── run_dev.bat                  # Double-click startup script for Windows
```

---

## 🚦 Getting Started

### 1. Prerequisites
- **Python**: Make sure Python 3.10+ is installed and added to your path.
- **Node.js**: Install Node.js 18+ (comes with npm).

### 2. Configuration Setup
Create a `.env` file in the root directory and add your Google AI Studio Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

### 3. Running Dev Server (Windows)
Simply double-click the **`run_dev.bat`** file in the project root. This launches both the FastAPI server (`http://localhost:8080`) and the Next.js App (`http://localhost:3080`) in separate command prompt windows.

### 4. Running Dev Server (Manual Commands)

**Start FastAPI Backend:**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload
```

**Start Next.js Frontend:**
```bash
cd frontend
npm run dev
```

Open [http://localhost:3080](http://localhost:3080) in your web browser.