import cv2
import argparse
from omegaconf import OmegaConf
import os
from tqdm import tqdm 

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_dark(frame, brightness_threshold):
    """
    Check if a frame is dark based on its brightness.

    Args:
        frame (numpy.ndarray): Input frame.
        brightness_threshold (float): Threshold for darkness.

    Returns:
        bool: True if the frame is dark, False otherwise.
    """
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate the average brightness
    avg_brightness = cv2.mean(gray_frame)[0]
    return avg_brightness < brightness_threshold

def is_shaky(frame, prev_frame, motion_threshold):
    """
    Check if a frame is shaky based on motion analysis with the previous frame.

    Args:
        frame (numpy.ndarray): Current frame.
        prev_frame (numpy.ndarray): Previous frame.
        motion_threshold (float): Threshold for shakiness.

    Returns:
        bool: True if the frame is shaky, False otherwise.
    """
    # Convert frames to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Calculate dense optical flow using Farneback method
    flow = cv2.calcOpticalFlowFarneback(gray_prev_frame, gray_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Compute the magnitude of the motion vectors
    motion_magnitude = cv2.norm(flow, cv2.NORM_L2)

    return motion_magnitude > motion_threshold

def is_noisy(frame, noise_threshold):
    """
    Check if a frame is noisy based on image noise analysis.

    Args:
        frame (numpy.ndarray): Input frame.
        noise_threshold (float): Threshold for noise.

    Returns:
        bool: True if the frame is noisy, False otherwise.
    """
    # Apply Gaussian blur to the frame
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Calculate the absolute difference between the original frame and the blurred frame
    frame_diff = cv2.absdiff(frame, blurred_frame)

    # Calculate the mean pixel difference
    mean_diff = cv2.mean(frame_diff)[0]

    return mean_diff > noise_threshold

def main(args):
    """
    Process a video, saving frames that meet a quality threshold and logging the process.

    Args:
        args (argparse.Namespace): Command-line arguments.
    """
    config = OmegaConf.load(f"../config/{args.config}.yaml")
    input_video_path = config.path.data.input
    output_video_path = config.path.data.preprocessing_output
    log_file_path = config.path.log.preprocessing_log  # Path to the text log file

    # Create the output directory if it doesn't exist.
    os.makedirs(output_video_path[:15], exist_ok=True)
    os.makedirs(log_file_path[:7], exist_ok=True)

    # TODO: Handle threshold values and boolean info through config file
    brightness_bool = False
    motion_bool = False
    noise_bool = False
    
    quality_threshold = 50
    brightness_threshold = 100
    motion_threshold = 5
    noise_threshold = 50

    cap = cv2.VideoCapture(input_video_path)
    ret, frame = cap.read()
    prev_frame = frame

    if not cap.isOpened():
        logger.warning(f"Unable to load the video. File path: {input_video_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(5))
    frame_size = (int(cap.get(3)), int(cap.get(4)))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    frame_count = 0
    saved_frame_count = 0

    logger.info("🔥 Processing starts.")

    with open(log_file_path, 'w') as log_file:
        for _ in tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
            ret, frame = cap.read()

            if not ret:
                logger.warning(f"Reached the end of the video or encountered an issue while reading the video. Folder name: {input_video_path}")
                break

            frame_quality = cv2.mean(frame)[0]
            exclude_reasons = []  # Store reasons for frame exclusion

            if frame_quality < quality_threshold:
                exclude_reasons.append("Quality below threshold")
            
            if brightness_bool and is_dark(frame, brightness_threshold):
                exclude_reasons.append("Dark frame")
            
            if motion_bool and is_shaky(frame, prev_frame, motion_threshold):
                exclude_reasons.append("Shaky frame")
            
            if noise_bool and is_noisy(frame, noise_threshold):
                exclude_reasons.append("Noisy frame")

            if exclude_reasons:
                # Log exclusion reasons
                log_file.write(f"Deleted frame at time {frame_count / fps} seconds. Reasons: {', '.join(exclude_reasons)}\n")
            else:
                out.write(frame)
                saved_frame_count += 1
                log_file.write(f"Saved frame at time {frame_count / fps} seconds. Reason: Quality above threshold.\n")

            frame_count += 1
            prev_frame = frame

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