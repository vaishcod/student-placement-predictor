import streamlit as st
from model import predict_placement

st.title("🎓 Student Placement Predictor")

cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
skills = st.slider("Skills", 1, 5, 3)
internships = st.slider("Internships", 0, 5, 1)
projects = st.slider("Projects", 0, 5, 2)
communication = st.slider("Communication", 1, 5, 3)

if st.button("Predict"):
    result = predict_placement([cgpa, skills, internships, projects, communication])

    if result == 1:
        st.success("🎉 Likely to get placed")
    else:
        st.error("❌ Not likely to get placed")