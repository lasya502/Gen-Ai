import streamlit as st
from transformers import pipeline

# Load the Hugging Face AI model
st.write("Loading AI model... (This might take a while)")
try:
    study_planner = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {e}")
    study_planner = None

# Streamlit UI
st.title("StudBud: AI Study Planner")
st.subheader("Generate a study plan based on your needs!")

# User Inputs
subject = st.text_input("Enter the subject you want to study:")
hours = st.slider("How many hours per day?", 1, 10, 2)

# Function to generate the study plan
def generate_study_plan():
    if not study_planner:
        st.error("AI model is not available. Try restarting the app.")
        return

    st.write("Generating study plan... Please wait!")
    try:
        prompt = f"Create a {hours}-hour daily study plan for learning {subject}."
        response = study_planner(prompt, max_length=100, do_sample=True)
        st.session_state["generated_output"] = response[0]["generated_text"]
    except Exception as e:
        st.error(f"Error generating study plan: {e}")

# Initialize session state for output
if "generated_output" not in st.session_state:
    st.session_state["generated_output"] = ""

# Generate button
if st.button("Generate Study Plan"):
    generate_study_plan()

# Display output
if st.session_state["generated_output"]:
    st.subheader("Generated Study Plan:")
    st.write(st.session_state["generated_output"])
