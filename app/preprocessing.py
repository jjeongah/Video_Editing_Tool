import cv2
import os
from tqdm import tqdm 
import tempfile

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

def preprocessing(uploaded_file, quality_bool, quality_threshold, brightness_bool, brightness_threshold, motion_bool, motion_threshold, noise_bool, noise_threshold):
    """
    Process a video, saving frames that meet a quality threshold and logging the process.

    Args:
        uploaded_file (UploadedFile): Uploaded video file.
        quality_threshold (float): Threshold for quality.
        brightness_bool (bool): Enable brightness filter.
        brightness_threshold (float): Threshold for brightness.
        motion_bool (bool): Enable motion filter.
        motion_threshold (float): Threshold for motion.
        noise_bool (bool): Enable noise filter.
        noise_threshold (float): Threshold for noise.
    """
    # Create a temporary directory to store the output video and log file
    temp_dir = tempfile.mkdtemp()

    # Define the paths for the output video and log file within the temporary directory
    output_video_path = os.path.join(temp_dir, 'output_video.mp4')
    log_file_path = os.path.join(temp_dir, 'processing_log.txt')

    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    cap = cv2.VideoCapture(temp_file_path)

    if not cap.isOpened():
        print(f"Unable to load the video. File path: {temp_file_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(5))
    frame_size = (int(cap.get(3)), int(cap.get(4)))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    frame_count = 0
    saved_frame_count = 0
    frame_interval = 1.0 / fps  # Time duration per frame

    # Create a tqdm progress bar
    progress_bar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
                    
    logger.info("🔥 Processing starts.")

    with open(log_file_path, 'w') as log_file:
        while True:
            ret, frame = cap.read()

            if not ret:
                logger.warning(f"Reached the end of the video or encountered an issue while reading the video. File path: {temp_file_path}")
                break

            frame_quality = cv2.mean(frame)[0]
            exclude_reasons = []  # Store reasons for frame exclusion

            if quality_bool and frame_quality < quality_threshold:
                exclude_reasons.append("Quality below threshold")

            if brightness_bool and is_dark(frame, brightness_threshold):
                exclude_reasons.append("Dark frame")

            if motion_bool and is_shaky(frame, prev_frame, motion_threshold):
                exclude_reasons.append("Shaky frame")

            if noise_bool and is_noisy(frame, noise_threshold):
                exclude_reasons.append("Noisy frame")

            if not exclude_reasons:
                out.write(frame)
                saved_frame_count += 1
            else:
                log_file.write(f"Deleted frame at time {frame_count * frame_interval:.2f} seconds. Reasons: {', '.join(exclude_reasons)}\n")

            frame_count += 1
            prev_frame = frame

            if frame_count % 10 == 0:
                logger.info(f"Processed {frame_count} frames, Saved {saved_frame_count} frames")

            # Update the tqdm progress bar
            progress_bar.update(1)

        # Close the tqdm progress bar
        progress_bar.close()

    logger.info("🔥 Processing complete.")
    logger.info(f"Output video duration: {saved_frame_count * frame_interval:.2f} seconds")
    logger.info(f"Processed {frame_count} frames, Saved {saved_frame_count} frames")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    return output_video_path, log_file_path