# =========================
# 🔥 ULTRA PRO MAX: SKILL-BASED PLACEMENT + ROLE MATCH SYSTEM
# =========================

import streamlit as st
import pickle
import numpy as np

model = pickle.load(open('model.pkl', 'rb'))

st.title("🚀 AI Placement + Skill Match Analyzer")

# -----------------------------
# ROLE SELECTION
# -----------------------------
role = st.selectbox("Select Target Role", [
    "Software Engineer",
    "Data Scientist",
    "Web Developer",
    "AI/ML Engineer"
])

company = st.selectbox("Target Company", ["Startup", "MNC", "Product-Based"])

# -----------------------------
# ROLE SKILLS DATABASE
# -----------------------------
skill_map = {
    "Software Engineer": ["DSA", "OOP", "DBMS", "System Design", "OS"],
    "Data Scientist": ["Python", "Pandas", "ML", "Statistics", "SQL"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "AI/ML Engineer": ["Python", "Deep Learning", "TensorFlow", "NLP", "Math"]
}

# -----------------------------
# INPUTS
# -----------------------------
st.subheader("📊 Academic + Profile Inputs")

cgpa = st.slider("CGPA", 0.0, 10.0, 5.0)
internships = st.slider("Internships", 0, 5, 1)
projects = st.slider("Projects", 0, 5, 1)
communication = st.slider("Communication", 0, 5, 2)
resume = st.slider("Resume Strength (0-100)", 0, 100, 50)

# -----------------------------
# SKILL SELECTION
# -----------------------------
st.subheader("🧠 Select Your Skills")
selected_skills = st.multiselect("Choose your skills", skill_map[role])

skill_score = len(selected_skills)
skills = min(skill_score, 5)

# -----------------------------
# SKILL MATCH %
# -----------------------------
match_percent = (len(selected_skills) / len(skill_map[role])) * 100

st.subheader("🎯 Skill Match Percentage")
st.progress(int(match_percent))
st.write(f"You match {match_percent:.2f}% of required skills for {role}")

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("Predict Placement"):

    data = np.array([[cgpa, skills, internships, projects, communication]])
    result = model.predict(data)
    prob = model.predict_proba(data)[0][1]

    # ---------------- SIMULATION ----------------
    st.subheader("🎮 What If Simulation")

    if st.button("Simulate Improvement"):
        improved_prob = model.predict_proba([[cgpa, 5, internships, projects, communication]])[0][1]
        st.write(f"📈 If skills improve → Chances: {improved_prob*100:.2f}%")

    # ---------------- RESULT ----------------
    if result[0] == 1:
        st.success(f"✅ High Chances ({prob*100:.2f}%)")
    else:
        st.error(f"❌ Low Chances ({prob*100:.2f}%)")

    st.progress(int(prob*100))

    # ---------------- GAP ANALYSIS ----------------
    st.subheader("📉 Skill Gap Analysis")

    missing_skills = list(set(skill_map[role]) - set(selected_skills))

    if missing_skills:
        st.write("❗ You need to learn:")
        for skill in missing_skills:
            st.write(f"👉 {skill}")
    else:
        st.success("🔥 You have all required skills!")

    # ---------------- SCORE ----------------
    final_score = (prob*100 * 0.4) + (match_percent * 0.4) + (resume * 0.2)

    # Company logic
    if company == "Startup":
        final_score += skills * 2
    elif company == "MNC":
        final_score += cgpa * 2
    elif company == "Product-Based":
        final_score += projects * 2

    # Display score
    st.subheader("🏆 Overall Placement Score")
    st.progress(int(final_score))
    st.write(f"Final Score: {final_score:.2f}/100")

    # ---------------- ROLE FIT SCORE ----------------
    role_fit = (match_percent * 0.6) + (skills * 10 * 0.4)

    st.subheader("🎯 Role Fit Score")
    st.progress(int(role_fit))
    st.write(f"You are {role_fit:.2f}% fit for {role}")

    # ---------------- FINAL SUGGESTIONS ----------------
    st.subheader("📌 Final Recommendations")
    st.subheader("⏳ Placement Readiness Timeline")

    if final_score < 50:
        st.write("⏳ 4-6 months needed")
    elif final_score < 75:
        st.write("⏳ 2-3 months needed")
    else:
        st.write("🚀 You are ready for placements now!")

    if final_score > 75:
        st.success("🚀 You are placement ready!")
    elif final_score > 50:
        st.warning("⚡ You are close! Improve a few areas.")
    else:
        st.error("❗ You need significant improvement.")
