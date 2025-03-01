import streamlit as st
from transformers import pipeline

# Load the Hugging Face AI model
study_planner = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

# Streamlit UI
st.title("StudBud: AI Study Planner")
st.subheader("Generate a study plan based on your needs!")

# User Inputs
subject = st.text_input("Enter the subject you want to study:")
hours = st.slider("How many hours per day?", 1, 10, 2)

if st.button("Generate Study Plan"):
    prompt = f"Create a {hours}-hour daily study plan for learning {subject}."
    response = study_planner(prompt, max_length=100, do_sample=True)
    st.write(response[0]["generated_text"])
