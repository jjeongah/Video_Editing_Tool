import cv2
import os
import tempfile

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from io import StringIO

def generate_shorts(timeline_log, input_video_path):
    """
    Extracts video clips based on scene information from a timeline log file.

    Args:
        timeline_log (str): Path to the timeline log file.
        input_video_path (str): Path to the input video file.
        output_shorts_path (str): Path to the directory where video clips will be saved.

    Returns:
        List[str]: List of paths to the generated video clips.
    """
    # Create a StringIO object to simulate a file
    timeline_log_file = StringIO(timeline_log)

    # Load the scene information from the StringIO object
    lines = timeline_log_file.readlines()
    logger.info("lines information: %s", lines)

    scenes = []
    for line in lines:
        if line.startswith("Scene"):
            parts = line.split()
            print(parts)
            scene_start = parts[4]
            scene_end = parts[-1]
            scenes.append({"start": scene_start, "end": scene_end})
    logger.info("scenes information: %s", scenes)

    # Open the input video file
    cap = cv2.VideoCapture(input_video_path)

    # Create a temporary directory to store the output video and log file
    temp_dir = tempfile.mkdtemp()

    # Define the paths for the output video and log file within the temporary directory
    output_shorts_path = os.path.join(temp_dir, 'output/')
    
    # Ensure the output directory exists
    os.makedirs(output_shorts_path, exist_ok=True)

    # Convert scene start and end times to frames
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    scene_frames = []
    logger.info("🔥 Video clips extract starts.")
    clip_paths = []  # List to store paths of generated clips
    for i, scene in enumerate(scenes):
        start_time_parts = scene["start"].split(':')
        end_time_parts = scene["end"].split(':')

        start_frame = (
            int(start_time_parts[0]) * 3600 * frame_rate +
            int(start_time_parts[1]) * 60 * frame_rate +
            int(float(start_time_parts[2]) * frame_rate)
        )

        end_frame = (
            int(end_time_parts[0]) * 3600 * frame_rate +
            int(end_time_parts[1]) * 60 * frame_rate +
            int(float(end_time_parts[2]) * frame_rate)
        )

        scene_frames.append({"start": start_frame, "end": end_frame})

    # Extract video clips for each scene
    for i, scene in enumerate(scene_frames):
        start_frame = scene["start"]
        end_frame = scene["end"]
        clip_name = f'clip_{i + 1}.mp4'
        clip_path = os.path.join(output_shorts_path, clip_name)
        clip_paths.append(clip_path)  # Append the path to the list

        # Set the video writer for the output clip
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(clip_path, fourcc, frame_rate, (int(cap.get(3)), int(cap.get(4))))

        # Seek to the start frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        while cap.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()

    # Release the input video
    cap.release()

    logger.info("🔥 Video clips extracted successfully.")
    return clip_paths