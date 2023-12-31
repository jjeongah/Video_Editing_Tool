import streamlit as st
from preprocessing import preprocessing
from timeline import timeline
from generate_shorts import generate_shorts
from detect_category import detect_category
from io import BytesIO

# Define the steps
STEPS = {
    1: "Upload Video or Enter YouTube URL",
    2: "Set Preprocessing Parameters",
    3: "Display Processed Video or Results",
    4: "Detect Timeline",
    5: "Generate Shorts",
}

st.title("Video Editing Tool")

# Initialize step variable
current_step = 1

# ===================== Step 1: Upload Video or Enter YouTube URL =====================
st.header(f"STEP {current_step}: {STEPS[current_step]}")

# Use st.form for better organization
with st.form("step_1_form"):
    upload_option = st.radio("Choose an option:", ("Upload Video", "YouTube URL"))
    video_url = ""

    if upload_option == "Upload Video":
        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
        if uploaded_file:
            video_url = uploaded_file
            st.success("Video processing complete! Move onto processing step.")
            current_step += 1

    elif upload_option == "YouTube URL":
        youtube_url = st.text_input("Enter YouTube URL")
        if youtube_url:
            video_url = youtube_url
            st.success("Uploading video is complete! Move onto processing step.")
            current_step += 1

    # Add a submit button to move to the next step
    if st.form_submit_button("Next Step"):
        st.write("Moved to the processing step!")

        
# ===================== Step 2: Set Preprocessing Parameters =====================
if current_step == 2:
    st.header("STEP 2-1: Choose preprocessing parameters")

    # Use st.form for better organization
    with st.form("step_2_1_form"):
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
        
        # Add a submit button to move to the next step
        if st.form_submit_button("Next Step"):
            current_step += 1

# ===================== Step 3: Display Processed Video or Results =====================
if current_step == 3:
    # Display selected parameter information
    st.subheader("Selected Parameters")

    info_text = (
        f"Quality Threshold: {quality_threshold},\n"
        f"Brightness Filter: {brightness_bool} (Threshold: {brightness_threshold}),\n"
        f"Motion Filter: {motion_bool} (Threshold: {motion_threshold}),\n"
        f"Noise Filter: {noise_bool} (Threshold: {noise_threshold})"
    )

    st.info(info_text)
    preprocessing_output_video_path, log_file_path = preprocessing(video_url, quality_bool, quality_threshold, brightness_bool, brightness_threshold, motion_bool, motion_threshold, noise_bool, noise_threshold)
    st.success("Video processing complete! Show the result below")
        
    with st.form("step_3_2_form"):
        st.subheader("Processed Video (Results)")

        # Display the processed video
        st.video(preprocessing_output_video_path, format="video/mp4", start_time=0)

        # Display frame exclusion reasons from the log file
        with open(log_file_path, 'r') as log_file:
            reasons = log_file.read()
            if reasons:
                st.text("Frame Exclusion Reasons:")
                st.text(reasons)
            else:
                st.text("None of the part is excluded")  
                
        if st.form_submit_button("Automatically moved to the Next Step"):
            st.write("Automatically moved to the timeline detection step!")
        current_step += 1
            
# ===================== Step 4: Detect timeline =====================
if current_step == 4:
    with st.form("step_4_form"):
        st.header("STEP 3: Detect Timeline")
        st.success("Timeline detection has automatically started")
        timeline_output_dir = timeline(preprocessing_output_video_path)
        print("timeline_output_dir:", timeline_output_dir)
        with open(timeline_output_dir, 'r') as log_file:
            timeline_content = log_file.read()
            if timeline_content:
                st.text("Detected Timeline:")
                st.text(timeline_content)
            else:
                st.error("Error: Timeline log not found. Please check if video is too short. Please upload new video.")
                current_step = 1
                
        current_step += 1 

        if st.form_submit_button("Automatically moved to the Next Step"):
            st.write("Automatically moved to the category detection step!")
    
# ===================== Step 5: Generate shorts =====================
import zipfile
import os
if current_step == 5:
    with st.form("step_5_form"):
        st.header("STEP 4-1: Detect Category")
        st.success("Category detection has automatically started. 10 random scenes are extracted from video to detect category.")
        # TODO: detect category
        most_common_category = detect_category(preprocessing_output_video_path)
        
        # Add a message below the video
        st.markdown(f"**Most Common Detected Category: {most_common_category}**", unsafe_allow_html=True)
        
        # Create radio options to choose from
        # TODO: button bug
        selected_category = st.radio("Select a category:", ("Animal", "Beauty", "Sports", "Food", "ETC"))
        
        # TODO: each category characteristic func

        current_step +=1
        if st.form_submit_button("Generate shots"):
            st.success("Category is selected!")

        
# ===================== Step 6: Download shorts =====================
import tempfile
import shutil

if current_step == 6:
    with st.form("step_6_form"):
        st.header("STEP 5: Download shorts")
        st.success("Shorts are generating!")
        videos = generate_shorts(timeline_content, preprocessing_output_video_path)
                    
        # Display the generated video clips
        if videos:
            st.subheader("Generated Video Clips")
            selected_videos = st.multiselect("Select videos to download", videos)

            for video_path in selected_videos:
                st.video(video_path, format="video/mp4", start_time=0)

            download_button_clicked = st.form_submit_button("Download shorts")

            if download_button_clicked and selected_videos:
                # Create a temporary directory to store selected videos
                temp_dir = tempfile.mkdtemp()

                # Copy selected videos to the temporary directory
                for video_path in selected_videos:
                    video_name = os.path.basename(video_path)
                    temp_video_path = os.path.join(temp_dir, video_name)
                    shutil.copy(video_path, temp_video_path)

                # Create a zip file
                zip_filename = "selected_shorts.zip"
                with st.spinner("Creating Zip file..."):
                    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                        for video_path in selected_videos:
                            video_name = os.path.basename(video_path)
                            zip_file.write(video_path, video_name)

                # Provide a link for download
                st.success(f"[Download Zip File]({zip_filename})")

                # Cleanup: Delete the temporary directory
                shutil.rmtree(temp_dir)