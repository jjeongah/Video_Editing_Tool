from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
import os
import logging
from tqdm import tqdm
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def timeline(input_video_path):
    """
    Perform scene detection on a video and save the scene list to 'timeline_log.txt'.
    """
    scene_log = ""

    video_manager = VideoManager([input_video_path])

    # Create a SceneManager and add ContentDetector to it.
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    # Set the video manager and scene manager to process the video.
    video_manager.set_downscale_factor()

    logger.info("🔥 Scene detection starts.")
    video_manager.start()  # Start the video manager.
    scene_manager.detect_scenes(frame_source=video_manager)  # Perform scene detection.
    scene_list = scene_manager.get_scene_list()  # Create the scene list.

    total_scenes = len(scene_list)

    total_scenes = len(scene_list)
    for i, scene in tqdm(enumerate(scene_list), total=total_scenes, desc="Processing Scenes"):
        scene_log += f"Scene {i + 1}: Start frame {scene[0]} - End frame {scene[1]}\n"

        # Update Streamlit with progress information
        progress_percent = (i + 1) / total_scenes * 100
        if progress_percent == 25 or 50 or 75:  # Update at 25%, 50%, 75% completion
            
            st.text(f"Processing: {progress_percent:.2f}%")
    video_manager.release()  # Release the video manager.

    # Save the scene log to 'timeline_log.txt' in the 'data/log' folder
    log_folder = os.path.join('data', 'log')
    os.makedirs(log_folder, exist_ok=True)
    log_file_path = os.path.join(log_folder, 'timeline_log.txt')

    with open(log_file_path, 'w') as log_file:
        log_file.write(scene_log)

    return log_file_path
