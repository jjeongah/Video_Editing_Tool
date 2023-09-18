import cv2
import argparse
from omegaconf import OmegaConf

def main(args):
    config = OmegaConf.load(f"./config/{args.config}.yaml")
    input_video_path = config.path.data.input
    output_video_path = config.path.data.output

    # Load the video file
    cap = cv2.VideoCapture(input_video_path)

    # Create an output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(5))  # Get the frames per second of the input video
    frame_size = (int(cap.get(3)), int(cap.get(4)))  # Get the frame size
    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    # Threshold for frame quality (adjust as needed)
    quality_threshold = 50

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break

        # Calculate the frame quality (you can use different metrics)
        frame_quality = cv2.mean(frame)[0]

        # Check if the frame quality is above the threshold
        if frame_quality >= quality_threshold:
            out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, default="base_config")
    args, _ = parser.parse_known_args()
    main(args)
    
