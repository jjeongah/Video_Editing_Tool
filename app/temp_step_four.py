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
    st.header("STEP 4-1: Detect Category")
    
    # Display the video
    st.video(video_url)
    
    # Add a message below the video
    st.markdown("**Category seems like Animal**", unsafe_allow_html=True)
    
    # Create radio options to choose from
    selected_category = st.radio("Select a category:", ("Animal", "Beauty", "Sports", "Food"))
    
    # Button to proceed
    if st.button("Make shorts based on the Category"):
        # Perform the desired action when the button is clicked
        st.success(f"Creating shorts based on the {selected_category} category...")
