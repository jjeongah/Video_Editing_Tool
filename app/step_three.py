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
    st.header("STEP 3: Detect timeline")
    
    # Display the video
    st.video(video_url)
    
    # Display timeline information in a vertical format
    timeline_info = """
    - Scene 1: Start frame 00:00:00.000 - End frame 00:00:11.759
    - Scene 2: Start frame 00:00:11.759 - End frame 00:00:33.138
    - Scene 3: Start frame 00:00:33.138 - End frame 00:00:40.172
    - Scene 4: Start frame 00:00:40.172 - End frame 00:00:44.862
    - Scene 5: Start frame 00:00:44.862 - End frame 00:00:48.207
    - Scene 6: Start frame 00:00:48.207 - End frame 00:00:51.793
    - Scene 7: Start frame 00:00:51.793 - End frame 00:00:58.586
    - Scene 8: Start frame 00:00:58.586 - End frame 00:01:04.448
    - Scene 9: Start frame 00:01:04.448 - End frame 00:01:08.759
    """
    st.markdown(timeline_info)

