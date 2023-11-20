from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
import os
import tempfile

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(input_video_path):
    video_manager = VideoManager([input_video_path])

    # Create a temporary directory to store the output video and log file
    temp_dir = tempfile.mkdtemp()

    # Define the paths for the output video and log file within the temporary directory
    output_scene_list_path = os.path.join(temp_dir, 'output/')
    
    # Ensure the output directory exists
    os.makedirs(output_scene_list_path, exist_ok=True)
    
    # Create a SceneManager and add ContentDetector to it.
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    # Set the video manager and scene manager to process the video.
    video_manager.set_downscale_factor()

    logger.info("🔥 Scene detection starts.")
    video_manager.start() # Start the video manager.
    scene_manager.detect_scenes(frame_source=video_manager) # Perform scene detection.
    scene_list = scene_manager.get_scene_list() # Create the scene list.

    # TODO: 
    # 1. By using Google Speech-to-Text API, convert speech into text
    # 2. Summarize the alternative text for each timeline

    # TODO: 
    # 1. By using Pillow library, let's use screen capture to extract screen information as text
    # 2. Additionally, when extracting screen capture using the Pillow library, also use additional computer vision technology to better detect text or important objects on the screen. 
    # For example, use Tesseract OCR to extract text displayed on the screen.
    
    
    # Print the scene list.
    with open(output_scene_list_path, 'w') as f:
        for i, scene in enumerate(scene_list):
            f.write(f"Scene {i + 1}: Start frame {scene[0]} - End frame {scene[1]}\n")

    video_manager.release() # Release the video manager.
    logger.info("🔥 Scene detection ended.")
    return output_scene_list_path