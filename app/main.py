import streamlit as st
import cv2
from preprocessing import main
from PIL import Image

# Streamlit UI
st.title("Video Preprocessing App")

# Step 1: Upload Video or Enter YouTube URL
upload_option = st.radio("Choose an option:", ("Upload Video", "YouTube URL"))
video_url = ""

if upload_option == "Upload Video":
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
    if uploaded_file:
        video_url = uploaded_file
        if st.button("Process Video"):
            # Move to the next page when the button is clicked
            st.experimental_rerun()
            st.experimental_show(next_page)

elif upload_option == "YouTube URL":
    youtube_url = st.text_input("Enter YouTube URL")
    if youtube_url:
        video_url = youtube_url
        if st.button("Process Video"):
            # Move to the next page when the button is clicked
            st.experimental_rerun()
            st.experimental_show(next_page)

# Second Page
if st.session_state.next_page:
    with st.spinner("Processing video..."):
        if upload_option == "Upload Video":
            video_path = f"temp_video.mp4"
            with open(video_path, 'wb') as f:
                f.write(video_url.read())
        else:
            # Download YouTube video using pytube
            from pytube import YouTube
            yt = YouTube(video_url)
            video_path = yt.streams.get_highest_resolution().download(filename="temp_video")

        main(video_path)  # Call the preprocessing function
        st.success("Video processing complete!")

        # Display the processed video or other results
        processed_video = "path_to_processed_video.mp4"
        st.title("Processed Video")
        st.video(processed_video)
