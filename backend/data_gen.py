import pandas as pd
import numpy as np
import random

def generate_placement_data(n=1500):
    data = []
    
    for _ in range(n):
        # Features
        cgpa = round(random.uniform(5.0, 10.0), 2)
        internships = random.randint(0, 4)
        projects = random.randint(0, 5)
        communication = random.randint(1, 5)
        
        # Skill set score (0-5)
        skills = random.randint(0, 5)
        
        # Heuristic for placement (Probability calculation)
        # Higher weight to CGPA, Projects, and Skills
        score = (cgpa * 10) + (internships * 15) + (projects * 12) + (communication * 8) + (skills * 15)
        
        # Base probability with some randomness
        prob = score / 250.0  # Max score is approx 100+60+60+40+75 = 335
        prob = min(0.95, prob) # Cap it
        
        # Add a bit of noise to make it realistic
        noise = random.uniform(-0.1, 0.1)
        prob += noise
        
        placed = 1 if prob > 0.6 else 0
        
        data.append([cgpa, skills, internships, projects, communication, placed])
    
    df = pd.DataFrame(data, columns=['CGPA', 'Skills', 'Internships', 'Projects', 'Communication', 'Placed'])
    df.to_csv('backend/synthetic_placement_data.csv', index=False)
    print(f"✅ Generated {n} rows of synthetic data at backend/synthetic_placement_data.csv")

if __name__ == "__main__":
    generate_placement_data()
