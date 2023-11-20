import streamlit as st
from preprocessing import preprocessing
from timeline import timeline
from io import BytesIO

st.title("Video Editing Tool")
st.header("STEP 1: Please upload a video or enter a YouTube URL")

# Initialize step variable
current_step = 1

# ===================== Step 1: Upload Video or Enter YouTube URL =====================
upload_option = st.radio("Choose an option:", ("Upload Video", "YouTube URL"))
video_url = ""

if upload_option == "Upload Video":
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
    if uploaded_file:
        video_url = uploaded_file
        current_step = 2
        st.success("Video processing complete! Move on to the processing step.")
        st.markdown('---')  # Add a horizontal rule

elif upload_option == "YouTube URL":
    youtube_url = st.text_input("Enter YouTube URL")
    if youtube_url:
        video_url = youtube_url
        current_step = 2
        st.success("Video processing complete! Move on to the processing step.")
        st.markdown('---')  # Add a horizontal rule

# Check if the current step is 2 (Detect timeline)
if current_step == 2:
    st.header("STEP 4-2: Generate shorts")
    # Display the video
    st.video(video_url)
    
    timeline_info = [
        "Scene 1: Start frame 00:00:00.000 - End frame 00:00:11.759",
        "Scene 2: Start frame 00:00:11.759 - End frame 00:00:33.138",
        "Scene 3: Start frame 00:00:33.138 - End frame 00:00:40.172"
    ]
    
    st.text("Recommended shorts are as below.")
    
    # Create checkboxes for each timeline to allow multiple selections
    selected_timelines = []
    for info in timeline_info:
        selected = st.checkbox(info)
        selected_timelines.append(selected)
    
    # Create a button to download the selected timelines
    if st.button("Download selected timelines"):
        # Process the selected timelines and perform the download
        # You can implement the download logic here
        selected_info = [info for info, selected in zip(timeline_info, selected_timelines) if selected]
        st.success(f"Downloading selected timelines: {', '.join(selected_info)}")
