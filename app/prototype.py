import streamlit as st
from preprocessing import preprocessing
from timeline import timeline
from generate_shorts import generate_shorts
from io import BytesIO
import time

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
        st.success("Video processing complete! Move onto processing step.")
        st.markdown('---')  # Add a horizontal rule

elif upload_option == "YouTube URL":
    youtube_url = st.text_input("Enter YouTube URL")
    if youtube_url:
        video_url = youtube_url
        current_step = 2
        st.success("Video processing complete! Move onto processing step.")
        st.markdown('---')  # Add a horizontal rule

        
# ===================== Step 2: Set Preprocessing Parameters =====================
if current_step == 2:
    st.header("STEP 2-1: Choose preprocessing parameters")

    # Load the video for preview
    st.subheader("Raw Video Preview")
    
    # Check if video_url is a file or a YouTube URL
    if isinstance(video_url, BytesIO):
        # User uploaded a file
        video_preview = st.video(video_url, format="video/mp4", start_time=0)
    else:
        # User entered a YouTube URL
        # You can add code here to fetch and display the YouTube video
        st.write("YouTube video will be displayed here")
    
    # Initialize a flag to keep track of whether processing has started
    processing_started = False
    
    # Checkbox for Noise
    quality_bool = st.checkbox("Enable Quality Filter", value=True)
    quality_threshold = st.slider("Quality Threshold", 0, 100, 30)
    
    # Checkbox for Brightness
    brightness_bool = st.checkbox("Enable Brightness Filter", value=False)
    brightness_threshold = st.slider("Brightness Threshold", 0, 255, 30)

    # Checkbox for Motion
    motion_bool = st.checkbox("Enable Motion Filter", value=False)
    motion_threshold = st.slider("Motion Threshold", 0, 100, 30)

    # Checkbox for Noise
    noise_bool = st.checkbox("Enable Noise Filter", value=False)
    noise_threshold = st.slider("Noise Threshold", 0, 100, 30)
    
    # Check if processing has started
    if not processing_started:
        if st.button("Process Video"):
            processing_started = True  # Set the flag to True
            # Add your video processing code here
            # You can update the current_step to navigate to the next step if needed
            current_step = 3

    # Disable UI elements if processing has started
    if processing_started:
        st.subheader("Processing has started. Parameters cannot be modified.")
    
    # TODO: show tdqm in the screen
        
# ===================== Step 3: Display Processed Video or Results =====================
if current_step == 3:
    # Display selected parameter information
    st.subheader("Selected Parameters")
    
    st.write(f"Quality Threshold: {quality_threshold}")
    st.write(f"Brightness Filter: {brightness_bool} (Threshold: {brightness_threshold})")
    st.write(f"Motion Filter: {motion_bool} (Threshold: {motion_threshold})")
    st.write(f"Noise Filter: {noise_bool} (Threshold: {noise_threshold})")
    
    preprocessing_output_video_path, log_file_path = preprocessing(video_url, quality_bool, quality_threshold, brightness_bool, brightness_threshold, motion_bool, motion_threshold, noise_bool, noise_threshold)
    st.header("STEP 2-2: Processed Video (Results)")

    # Display the processed video
    st.video(preprocessing_output_video_path, format="video/mp4", start_time=0)

    # Display frame exclusion reasons from the log file
    with open(log_file_path, 'r') as log_file:
        reasons = log_file.read()
        st.text("Deleted frame at 2.97 seconds. Reason: Quality below threshold")

# ===================== Step 4: Detect timeline =====================
# TODO: enable the button to move next step
    st.button("Detect Timeline")
    st.markdown('---')
    st.header("STEP 3: Detect Timeline")
    # Add a sleep-like behavior using the st.empty() placeholder
    progress_placeholder = st.empty()
    
    for _ in range(3):
        time.sleep(1)  # Simulating a delay (replace with actual timeline detection logic)
        progress_placeholder.text("Timeline detection is in progress...")
    st.subheader("Timeline detection is completed")
    st.video(preprocessing_output_video_path, format="video/mp4", start_time=0)
    timeline_info = """
    - Scene 1: Start frame 00:00:00.000 - End frame 00:00:05.759
    - Scene 2: Start frame 00:00:05.759 - End frame 00:00:11
    """
    st.markdown(timeline_info)
    
    
# ===================== Step 5: Generate shorts =====================
# TODO: enable the button to move next step
    st.button("Detect Category")
    st.header("STEP 4-1: Detect Category")
    st.subheader("Category detection is in progress")
    st.subheader("Category detection is completed")
    st.markdown("**Category seems like Animal**", unsafe_allow_html=True)
    st.video(preprocessing_output_video_path, format="video/mp4", start_time=0)
    # Create radio options to choose from
    selected_category = st.radio("Select a category:", ("Animal", "Beauty", "Sports", "Food"))
    
    st.button("STEP 4-2: Generate shorts")
    st.markdown('---')
    st.header("Generate shorts")
    
    timeline_info = [
        "Scene 1: Start frame 00:00:00.000 - End frame 00:00:05.759",
        "Scene 2: Start frame 00:00:05.759 - End frame 00:00:11"
    ]
    
    st.subheader("Highlight Recommendation is in progress...")
    st.subheader("Highlight Recommendationis completed")
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
