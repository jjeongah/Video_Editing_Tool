import streamlit as st
import cv2
import numpy as np
import os
import tempfile
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions

# Load InceptionV3 model pre-trained on ImageNet data
model = InceptionV3(weights='imagenet')

# Map ImageNet class indices to human-readable labels
imagenet_labels = {
    'n02342885': 'Animal',
    'n03814639': 'Beauty',
    'n04118538': 'Sports',
    'n07697537': 'Food'
}

def predict_category(img_array):
    # Make predictions
    predictions = model.predict(img_array)

    # Decode predictions and get the top predicted class
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    top_class_index = decoded_predictions[0][0]

    # Map ImageNet class index to human-readable label
    category = imagenet_labels.get(top_class_index, 'Unknown')

    return category

def process_video(video_path, num_frames=10):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get random frames
    random_frame_indices = np.random.choice(total_frames, size=num_frames, replace=False)

    categories = []

    for frame_index in random_frame_indices:
        # Set the frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        # Read the frame
        ret, frame = cap.read()

        if ret:
            # Preprocess the frame for prediction
            img_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_array = cv2.resize(img_array, (299, 299))
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            # Predict category
            category = predict_category(img_array)
            categories.append(category)

    # Release the video capture object
    cap.release()

    return categories

# Streamlit UI
st.title("Video Category Detection")

uploaded_file = st.file_uploader("Choose a video file...", type=["mp4"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        temp_video_path = temp_video.name

    st.video(uploaded_file, format="video/mp4")

    # Process video and detect categories
    categories = process_video(temp_video_path)
    
    # Find the most common category
    most_common_category = max(set(categories), key=categories.count)
    st.success(f"Most Common Category: {most_common_category}")
