import argparse
from omegaconf import OmegaConf
import torch
from torch.utils.data import Dataset, DataLoader
from data_loader.data_loader import TimelineDataset
from model.model import TimelineDetectionModel
import os
import json

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(config):
    # 🆘
    config = OmegaConf.load(f"../config/{args.config}.yaml")
    data_dir = config.train.input_path 
    all_data = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
            all_data.append(data)

    # 데이터를 하나의 리스트로 결합
    combined_data = []
    for data in all_data:
        combined_data.extend(data)

    # 데이터를 TimelineDataset으로 변환
    dataset = TimelineDataset(combined_data)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # 모델 및 손실 함수, 옵티마이저 정의
    input_size = 1  # 입력 특성 수 (예: 시간대)
    hidden_size = 64  # LSTM의 은닉 상태 크기
    num_classes = 1  # 이진 분류 문제이므로 클래스 수는 1

    model = TimelineDetectionModel(input_size, hidden_size, num_classes)
    criterion = torch.nn.BCEWithLogitsLoss()  # 이진 분류 손실
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 학습 루프
    num_epochs = 10

    for epoch in range(num_epochs):
        for batch in dataloader:
            # 데이터 및 레이블 추출
            timeline_data = batch["timeline_data"]
            video_length = batch["video_length"]

            # 모델 입력 데이터 생성
            inputs = torch.tensor([[(end_time - start_time) / video_length] for start_time, end_time, _ in timeline_data], dtype=torch.float32)

            # 모델 출력 계산
            outputs = model(inputs)

            # 라벨 데이터 생성 (이진 분류)
            labels = torch.tensor([1 if label == "category" else 0 for _, _, label in timeline_data], dtype=torch.float32)

            # 손실 계산 및 역전파
            loss = criterion(outputs, labels.view(-1, 1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}")

        # 학습된 모델 저장 (필요하면)
        torch.save(model.state_dict(), "timeline_detection_model.pth")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, default="base_config")
    args, _ = parser.parse_known_args()
    main(args)