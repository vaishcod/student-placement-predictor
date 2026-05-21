from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import os
import io
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from backend.utils.resume_parser import extract_text_from_pdf, parse_resume_text
from backend.utils.roadmap_generator import generate_roadmap

app = FastAPI(title="CareerLens AI API", description="AI-driven Career Prediction and Placement Roadmap Architect")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML model
MODEL_PATH = "backend/placement_model.pkl"
model = None
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("✅ ML model loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
else:
    print(f"⚠️ Model path {MODEL_PATH} not found. Running without predictor capabilities.")

# Standard Skill Map
SKILL_MAP = {
    "Software Engineer": ["DSA", "OOP", "DBMS", "System Design", "OS"],
    "Data Scientist": ["Python", "Pandas", "ML", "Statistics", "SQL"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "AI/ML Engineer": ["Python", "Deep Learning", "TensorFlow", "NLP", "Math"]
}

class PredictionRequest(BaseModel):
    cgpa: float
    skills: int
    internships: int
    projects: int
    communication: int
    role: str
    company: str
    resume_strength: int
    selected_skills_list: List[str]

class RoadmapRequest(BaseModel):
    role: str
    current_skills: List[str]
    missing_skills: List[str]

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to CareerLens AI API",
        "endpoints": {
            "/skills": "GET - Fetch available roles and skill maps",
            "/predict": "POST - Placement probability and analytics prediction",
            "/parse-resume": "POST - Upload PDF resume and extract details",
            "/generate-roadmap": "POST - Create custom 4-week learning roadmap"
        }
    }

@app.get("/skills")
async def get_skills():
    return SKILL_MAP

@app.post("/predict")
async def predict_placement(req: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Prediction model is not initialized/loaded on backend.")
    
    # 1. Base ML model prediction
    # Predict using features: CGPA, SkillsCount (max 5), Internships, Projects, Communication
    skills_count = min(req.skills, 5)
    input_data = np.array([[req.cgpa, skills_count, req.internships, req.projects, req.communication]])
    
    try:
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")
    
    # 2. Skill Match calculation
    role_required_skills = SKILL_MAP.get(req.role, [])
    matched_skills = [s for s in req.selected_skills_list if s in role_required_skills]
    missing_skills = [s for s in role_required_skills if s not in req.selected_skills_list]
    
    match_percent = 0.0
    if role_required_skills:
        match_percent = (len(matched_skills) / len(role_required_skills)) * 100
        
    # 3. Overall placement score (incorporating model, resume strength, skills match)
    final_score = (probability * 100 * 0.4) + (match_percent * 0.4) + (req.resume_strength * 0.2)
    
    # Apply company weighting logic
    if req.company == "Startup":
        final_score += req.skills * 2
    elif req.company == "MNC":
        final_score += req.cgpa * 2
    elif req.company == "Product-Based":
        final_score += req.projects * 2
        
    # Clamp final score to 100
    final_score = min(100.0, max(0.0, final_score))
    
    # 4. Role Fit score
    role_fit = (match_percent * 0.6) + (skills_count * 10 * 0.4)
    role_fit = min(100.0, role_fit)
    
    # 5. Timeline preparation
    if final_score < 50:
        readiness_timeline = "4-6 months of focused learning needed"
        readiness_status = "needs_improvement"
    elif final_score < 75:
        readiness_timeline = "2-3 months of polish needed"
        readiness_status = "close"
    else:
        readiness_timeline = "Ready for placements now!"
        readiness_status = "ready"
        
    # 6. What-if simulation
    # What if the user gets max skills (5)?
    improved_input = np.array([[req.cgpa, 5, req.internships, req.projects, req.communication]])
    improved_prob = model.predict_proba(improved_input)[0][1]
    
    return {
        "placed_prediction": int(prediction),
        "placement_probability": round(float(probability) * 100, 2),
        "match_percentage": round(match_percent, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "overall_placement_score": round(final_score, 2),
        "role_fit_score": round(role_fit, 2),
        "readiness_timeline": readiness_timeline,
        "readiness_status": readiness_status,
        "simulation": {
            "max_skills_probability": round(float(improved_prob) * 100, 2)
        }
    }

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        # Let's support txt file parsing too just in case
        if file.filename.endswith(".txt"):
            content = await file.read()
            text = content.decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Only PDF and TXT resumes are supported.")
    else:
        content = await file.read()
        file_io = io.BytesIO(content)
        text = extract_text_from_pdf(file_io)
        
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from the resume. Please check if the PDF contains readable text.")
        
    parsed_data = parse_resume_text(text)
    return parsed_data

@app.post("/generate-roadmap")
async def get_roadmap(req: RoadmapRequest):
    roadmap = generate_roadmap(req.role, req.current_skills, req.missing_skills)
    return roadmap

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
