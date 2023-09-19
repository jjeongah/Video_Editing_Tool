import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
from omegaconf import OmegaConf
import os

def main(config):
    # Load the video file
    config = OmegaConf.load(f"../config/{args.config}.yaml")
    video_path = config.path.data.eda_input
    cap = cv2.VideoCapture(video_path)

    # Initialize variables to store metadata
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    duration_seconds = frame_count / frame_rate

    print(f"Number of frames: {frame_count}")
    print(f"Frame width: {frame_width}, Frame height: {frame_height}")
    print(f"Frame rate: {frame_rate} fps")
    print(f"Duration: {duration_seconds} seconds")

    # Visualize a subset of video frames
    sampled_frames = []
    num_frames_to_sample = 10  # Change this to the number of frames you want to sample

    for _ in range(num_frames_to_sample):
        ret, frame = cap.read()
        if not ret:
            break
        sampled_frames.append(frame)

    # Close the video capture
    cap.release()

    # Display sampled frames
    fig, axs = plt.subplots(1, num_frames_to_sample, figsize=(15, 5))
    for i, frame in enumerate(sampled_frames):
        axs[i].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        axs[i].axis("off")

    # Add metadata as text below the first frame
    metadata_text = f"Number of frames: {frame_count}\nFrame width: {frame_width}, Frame height: {frame_height}\nFrame rate: {frame_rate} fps\nDuration: {duration_seconds} seconds"
    axs[0].text(0, -50, metadata_text, color='white', backgroundcolor='black')

    # Save the figure to a file (e.g., PNG)
    figure_path = config.path.data.eda_output  # Specify the file path and name
    plt.savefig(figure_path)

    # Show the figure
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, default="base_config")
    args, _ = parser.parse_known_args()
    main(args)
