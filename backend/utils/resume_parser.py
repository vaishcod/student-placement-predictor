import pypdf
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = None
if os.getenv("GEMINI_API_KEY"):
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing Gemini GenAI Client: {e}")

def extract_text_from_pdf(file_bytes) -> str:
    """Extract text from PDF file bytes."""
    try:
        reader = pypdf.PdfReader(file_bytes)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def parse_resume_text(text: str) -> dict:
    """Parse text using Google GenAI API or fallback to mock data."""
    global client
    if not client and os.getenv("GEMINI_API_KEY"):
        try:
            client = genai.Client()
        except Exception as e:
            print(f"Error initializing client on the fly: {e}")

    if not client:
        print("WARNING: GEMINI_API_KEY not set. Using mock resume parser.")
        return {
            "name": "Jane Developer (Demo Profile)",
            "email": "jane.dev@example.com",
            "cgpa": 8.5,
            "skills": ["Python", "JavaScript", "React", "HTML", "CSS", "FastAPI"],
            "internships": 1,
            "projects": 2,
            "communication": 4,
            "target_role": "Software Engineer",
            "education": "Bachelor of Technology in Computer Science",
            "experience": "Software Engineering Intern at TechCorp (3 months)",
            "projects_list": ["Personal Portfolio Website", "Task Management App"]
        }
    
    try:
        prompt = f"""
        You are an expert HR recruiter and parser. Analyze the following resume text and extract structured information in JSON format:
        - name: String (Candidate's full name)
        - email: String (Candidate's email address)
        - cgpa: Float (Academic CGPA or GPA out of 10. If the GPA is out of 4.0, scale it to 10.0 by multiplying by 2.5. If not found, return 7.5 as a sensible default)
        - skills: List of Strings (All technical skills, programming languages, databases, libraries, and frameworks mentioned)
        - internships: Integer (Count of internships. Count distinct internship roles/work experiences. If none, return 0)
        - projects: Integer (Count of distinct projects mentioned. If none, return 0)
        - communication: Integer (Rate the writing quality, formatting, and professionalism of the resume on a scale of 1 to 5. 1 being poor, 5 being exceptional)
        - target_role: String (Based on the resume content, categorize the best-fit role among these options: 'Software Engineer', 'Data Scientist', 'Web Developer', 'AI/ML Engineer')
        - education: String (Brief education summary, e.g., 'B.Tech in CS at University of State')
        - experience: String (Brief professional experience summary, e.g., 'Web Dev Intern at XYZ (2 months)')
        - projects_list: List of Strings (Names of distinct projects mentioned)
        
        Resume Text:
        {text}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing with Gemini: {e}")
        return {
            "name": "Error Parsing Resume",
            "email": "",
            "cgpa": 7.0,
            "skills": [],
            "internships": 0,
            "projects": 0,
            "communication": 3,
            "target_role": "Software Engineer",
            "education": "",
            "experience": "",
            "projects_list": []
        }
