import streamlit as st
from model import predict_placement

st.title("🎓 AI Student Placement Predictor")
st.write("Predict placement chances using Machine Learning")

cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
skills = st.slider("Skills", 1, 5, 3)
internships = st.slider("Internships", 0, 5, 1)
projects = st.slider("Projects", 0, 5, 2)
communication = st.slider("Communication", 1, 5, 3)

if st.button("Predict Placement"):
    prediction, probability, accuracy = predict_placement(
        [cgpa, skills, internships, projects, communication]
    )

    st.subheader("📊 Prediction Result")

    if prediction == 1:
        st.success(f"🎉 Likely to get placed ({probability*100:.2f}% chance)")
    else:
        st.error(f"❌ Less chance of placement ({probability*100:.2f}% chance)")

    st.info(f"Model Accuracy: {accuracy*100:.2f}%")