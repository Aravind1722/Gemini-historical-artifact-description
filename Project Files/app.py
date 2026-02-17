import streamlit as st
import os
from google import genai
from PIL import Image
from dotenv import load_dotenv

# Load Environment & Setup Client
load_dotenv()
# The new SDK uses a Client object for all interactions
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the latest stable "Flash" model as of Feb 2026
MODEL_ID = "gemini-2.5-flash" 

def get_gemini_response(user_input, image, system_prompt):
    """Uses the new SDK to generate multimodal content."""
    # The new SDK structure: client.models.generate_content
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[system_prompt, user_input, image]
    )
    return response.text

# --- Streamlit UI ---
st.set_page_config(page_title="Historical Explorer", page_icon="🏛️")
st.header("Gemini historical artifact description")

user_prompt = st.text_input("Enter Prompt:")
uploaded_file = st.file_uploader("Upload Artifact Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Open image for UI display
    img = Image.open(uploaded_file)
    st.image(img, caption="Target Artifact", use_container_width=True)

if st.button("Generate Description"):
    if uploaded_file:
        with st.spinner("Gemini  is analyzing the artifact..."):
            # Pass the PIL Image directly; the new SDK handles it!
            system_instruction = "You are a historian. Please describe the historical artifact in the image and provide detailed information, including its name, origin, time period , historical significance,interesting facts"
            description = get_gemini_response(user_prompt, img, system_instruction)
            
            st.subheader("Historical Description")
            st.markdown(description)
    else:
        st.error("Please upload an image first.")