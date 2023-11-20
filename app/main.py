import streamlit as st
from preprocessing import preprocessing
from timeline import timeline
from generate_shorts import generate_shorts
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
        timeline_output_path = timeline(preprocessing_output_video_path)
        print(timeline_output_path)
        # TODO: open timeline log and show text
        with open(timeline_output_path, 'r') as log_file:
            timeline_content = log_file.read()
            if timeline_content:
                st.text("Detected Timeline:")
                st.text(timeline_content)
            else:
                st.text("None of the part is excluded")  
                
        current_step += 1 

        if st.form_submit_button("Automatically moved to the Next Step"):
            st.write("Automatically moved to the category detection step!")
    
# ===================== Step 5: Generate shorts =====================
import zipfile
import os
if current_step == 5:
    with st.form("step_5_form"):
        st.success("Category detection has automatically started")
        st.header("STEP 4-1: Detect Category")
        # Add a message below the video
        st.markdown("**Category seems like Animal**", unsafe_allow_html=True)
        
        # Create radio options to choose from
        selected_category = st.radio("Select a category:", ("Animal", "Beauty", "Sports", "Food", "ETC"))
    
        if st.form_submit_button("Generate shots"):
            current_step +=1
            st.success("Category is selected!")


# ===================== Step 6: Download shorts =====================
if current_step == 6:
    videos = generate_shorts(timeline_output, preprocessing_output_video_path)
                
    # Display the generated video clips
    if videos:
        st.subheader("Generated Video Clips")
        for video_path in videos:
            st.video(video_path, format="video/mp4", start_time=0)

    download_button_clicked = st.form_submit_button("Download shorts")

    if download_button_clicked:
        # Add logic to create a zip file or download individual files
        # For example, you can use the following code to create a zip file and download it:
        zip_filename = "generated_shorts.zip"
        with st.spinner("Creating Zip file..."):
            # Add logic to create a zip file containing the generated shorts
            # You may need to modify this based on how your 'generate_shorts' function works
            # For example, you can use the zipfile library to create a zip file
            # and add the generated shorts to the zip file
            # After creating the zip file, provide a link for download
            # For demonstration purposes, I'm assuming 'videos' is a list of file paths
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                for video_path in videos:
                    zip_file.write(video_path, os.path.basename(video_path))

        st.success(f"[Download Zip File]({zip_filename})")
