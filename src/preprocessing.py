import cv2
import argparse
from omegaconf import OmegaConf
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(args):
    config = OmegaConf.load(f"../config/{args.config}.yaml")
    input_video_path = config.path.data.input
    output_video_path = config.path.data.preprocessing_output
    log_file_path = config.path.log.preprocessing_log  # Path to the text log file

    # Create the output directory if it doesn't exist.
    os.makedirs(output_video_path[:15], exist_ok=True)
    os.makedirs(log_file_path[:7], exist_ok=True)
    
    # Load the video file
    cap = cv2.VideoCapture(input_video_path)
    ret, frame = cap.read()
    if not cap.isOpened():
        logger.warning(f"Unable to load the video. File path: {input_video_path}")
        return

    ret, frame = cap.read()
    if not ret:
        logger.warning(f"Reached the end of the video or encountered an issue while reading the video. Folder name: {input_video_path}")
        return
    
    # Create an output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(5))  # Get the frames per second of the input video
    frame_size = (int(cap.get(3)), int(cap.get(4)))  # Get the frame size
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    # Threshold for frame quality (adjust as needed)
    quality_threshold = 50

    frame_count = 0
    saved_frame_count = 0

    logger.info("🔥 Processing starts.")

    # Open a text log file for writing
    with open(log_file_path, 'w') as log_file:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break

            # Calculate the frame quality (you can use different metrics)
            frame_quality = cv2.mean(frame)[0]

            # Check if the frame quality is above the threshold
            if frame_quality >= quality_threshold:
                out.write(frame)
                saved_frame_count += 1
                # Log the saved frame's time and reason for saving
                log_file.write(f"Saved frame at time {frame_count / fps} seconds. Reason: Quality above threshold.\n")
            else:
                # Log the deleted frame's time and reason for deletion
                log_file.write(f"Deleted frame at time {frame_count / fps} seconds. Reason: Quality below threshold.\n")

            frame_count += 1

            # Log progress every 10 frames
            if frame_count % 10 == 0:
                logger.info(f"Processed {frame_count} frames, Saved {saved_frame_count} frames")

    logger.info("🔥 Processing complete.")
    logger.info(f"Processed {frame_count} frames, Saved {saved_frame_count} frames")

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, default="base_config")
    args, _ = parser.parse_known_args()
    main(args)
