import cv2
import scenedetect
from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
import argparse
from omegaconf import OmegaConf
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(args):
    config = OmegaConf.load(f"../config/{args.config}.yaml")
    input_video_path = config.path.data.preprocessing_output
    output_scene_list_path = config.path.log.timeline_log
    
    # Create the output directory if it doesn't exist.
    os.makedirs(output_scene_list_path[:7], exist_ok=True)
    
    print(output_scene_list_path[:7])
    video_manager = VideoManager([input_video_path])

    # Create a SceneManager and add ContentDetector to it.
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    # Set the video manager and scene manager to process the video.
    video_manager.set_downscale_factor()

    logger.info("🔥 Scene detection starts.")
    video_manager.start() # Start the video manager.
    scene_manager.detect_scenes(frame_source=video_manager) # Perform scene detection.
    scene_list = scene_manager.get_scene_list() # Create the scene list.

    # Print the scene list.
    with open(output_scene_list_path, 'w') as f:
        for i, scene in enumerate(scene_list):
            f.write(f"Scene {i + 1}: Start frame {scene[0]} - End frame {scene[1]}\n")

    video_manager.release() # Release the video manager.

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, default="base_config")
    args, _ = parser.parse_known_args()
    main(args)