import argparse
from omegaconf import OmegaConf
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import torch
import torch.nn as nn
from transformers import BertPreTrainedModel, BertModel, BertTokenizer  # Import the tokenizer
from torch.utils.data import DataLoader, Dataset
from transformers import AdamW
import json
from data_loader.data_loader import CustomDataset
from model.model import TimelineDetectionModel

def main(config):
    # 🆘
    # Load your JSON data and create an instance of CustomDataset
    with open("your_json_file.json", "r") as json_file:
        data = json.load(json_file)

    dataset = CustomDataset(data)

    # Create a DataLoader for the dataset
    batch_size = 32  # Adjust this based on your needs
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Initialize the model
    model = TimelineDetectionModel.from_pretrained("bert-base-uncased", num_labels=8)  # Adjust num_labels as needed

    # Define the optimizer and loss function
    optimizer = AdamW(model.parameters(), lr=2e-5)
    loss_fn = nn.CrossEntropyLoss()

    # Tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    # Training loop
    num_epochs = 10  # Adjust as needed
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()

    for epoch in range(num_epochs):
        total_loss = 0
        for batch in dataloader:
            start_times = batch["start_time"]
            end_times = batch["end_time"]
            attributes = batch["attributes"]
            labels = batch["label"]

            # Tokenize your text data, prepare tensors, and send them to the device

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits

            # Modify the loss calculation based on your specific task
            loss = loss_fn(logits, labels)

            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {total_loss:.4f}")

    # Save the trained model
    model.save_pretrained("timeline_detection_model")

    # Inference
    model.eval()

    # TODO: Prepare dataset
    # Assuming you have new video data to predict on (X_test_videos)
    X_test_videos = [...]  # Your new video data

    # Tokenize and evaluate (similar to your previous code)
    for video_text in X_test_videos:
        tokens = tokenizer.encode_plus(
            video_text,
            add_special_tokens=True,
            max_length=128,  # Adjust as needed
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors="pt"
        )

        input_ids = tokens["input_ids"].to(device)
        attention_mask = tokens["attention_mask"].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()

        if predicted_class == 0:
            print("Timeline Detected")
        else:
            print("Explanation Detected")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, default="base_config")
    args, _ = parser.parse_known_args()
    main(args)
