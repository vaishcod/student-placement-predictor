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

def generate_roadmap(role: str, current_skills: list, missing_skills: list) -> dict:
    """Generate a 4-week learning roadmap using Gemini or fallback to a standard plan."""
    global client
    if not client and os.getenv("GEMINI_API_KEY"):
        try:
            client = genai.Client()
        except Exception as e:
            print(f"Error initializing client on the fly: {e}")

    if not client:
        print("WARNING: GEMINI_API_KEY not set. Using fallback roadmap generator.")
        # Fallback roadmap
        weeks = []
        skills_chunk_size = max(1, len(missing_skills) // 3)
        for i in range(4):
            week_num = i + 1
            if week_num == 4:
                topic = "Mock Interviews & Projects"
                desc = f"Build a project integrating your skills. Prepare for technical interviews tailored to {role} roles."
                task = f"Complete a portfolio-ready project showcasing your new skills: {', '.join(current_skills[:3])}."
                res = ["LeetCode", "InterviewBit Placement Guides", "GitHub Mock Repos"]
            else:
                chunk = missing_skills[i*skills_chunk_size : (i+1)*skills_chunk_size]
                chunk_str = ", ".join(chunk) if chunk else "Core technologies and architectures"
                topic = f"Mastering {chunk_str}" if chunk else f"Advanced {role} Design"
                desc = f"Deep dive into {chunk_str}. Focus on both theoretical understanding and coding implementations."
                task = f"Build 2 mini-projects implementing {chunk_str}."
                res = ["FreeCodeCamp Tutorials", "Official Documentation", "MDN Web Docs"]
            
            weeks.append({
                "week": week_num,
                "topic": topic,
                "description": desc,
                "task": task,
                "resources": res
            })
        return {"weeks": weeks}
    
    try:
        prompt = f"""
        You are an expert technical mentor and career architect. Create a highly personalized 4-week learning roadmap for a student.
        Target Role: {role}
        Student's Current Skills: {', '.join(current_skills) if current_skills else 'None'}
        Missing Skills to learn: {', '.join(missing_skills) if missing_skills else 'None'}
        
        Structure a 4-week plan. For each week, specify:
        - week: Integer (1 to 4)
        - topic: String (Focus topic of the week, e.g., 'Mastering REST APIs and FastAPI')
        - description: String (Clear explanation of concepts to learn and build familiarity with)
        - task: String (A concrete programming challenge or mini-project to build to prove proficiency)
        - resources: List of Strings (Specific links or high-quality free study paths, e.g., 'freeCodeCamp Node.js tutorial on YouTube', 'Official React documentation')
        
        Return this as a JSON object with a single root key "weeks", containing the list of 4 week objects.
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
        print(f"Error generating roadmap with Gemini: {e}")
        # Simplistic fallback
        return {
            "weeks": [
                {
                    "week": 1,
                    "topic": f"Getting Started with {role}",
                    "description": "Establish basic setup and foundational components.",
                    "task": "Set up project repositories.",
                    "resources": ["Official Documentation"]
                }
            ]
        }
