import streamlit as st

# Step 1: Upload Video or Enter YouTube URL
st.title("Video Uploader")

upload_option = st.radio("Choose an option:", ("Upload Video", "YouTube URL"))
video_url = ""

if upload_option == "Upload Video":
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
    if uploaded_file:
        st.success("Video uploaded successfully!")
        video_url = uploaded_file

elif upload_option == "YouTube URL":
    youtube_url = st.text_input("Enter YouTube URL")
    if youtube_url:
        st.success("YouTube URL entered successfully!")
        video_url = youtube_url

# Step 2: Display Uploaded Video
st.title("Uploaded Video")
if video_url:
    st.video(video_url)
else:
    st.info("Please upload a video or enter a YouTube URL.")
