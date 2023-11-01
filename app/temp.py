import streamlit as st
import argparse
from preprocessing import main
from pytube import YouTube

# Streamlit UI
st.title("Video Editing Tool")
st.header("Please upload a video or enter a YouTube URL")

# ===================== Step 1: Upload Video or Enter YouTube URL =====================
upload_option = st.radio("Choose an option:", ("Upload Video", "YouTube URL"))
video_url = ""

if upload_option == "Upload Video":
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
    if uploaded_file:
        video_url = uploaded_file
        st.success("Video processing complete! Move onto processing step.")

elif upload_option == "YouTube URL":
    youtube_url = st.text_input("Enter YouTube URL")
    if youtube_url:
        video_url = youtube_url
        st.success("Video is uploaded! Move onto processing step.")

# Check if an option is selected before proceeding to Step 2
if video_url:
    # Clear the existing elements
    st.text("")  # Empty text element for spacing

    # Create an empty placeholder for Step 2
    step2_placeholder = st.empty()

    # ===================== Step 2: Set Preprocessing Parameters =====================
    step2_placeholder.header("Preprocessing Parameters")

    # Checkbox for Brightness
    brightness_bool = step2_placeholder.checkbox("Enable Brightness Filter", value=False)
    brightness_threshold = step2_placeholder.slider("Brightness Threshold", 0, 255, 30)

    # Checkbox for Motion
    motion_bool = step2_placeholder.checkbox("Enable Motion Filter", value=False)
    motion_threshold = step2_placeholder.slider("Motion Threshold", 0, 100, 30)

    # Checkbox for Noise
    noise_bool = step2_placeholder.checkbox("Enable Noise Filter", value=False)
    noise_threshold = step2_placeholder.slider("Noise Threshold", 0, 100, 30)

    if step2_placeholder.button("Process Video"):
        with st.spinner("Processing video..."):
            
            st.success("Video processing complete!")
