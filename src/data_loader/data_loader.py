import torch
from torch.utils.data import Dataset, DataLoader

class TimelineDataset(Dataset):
    def __init__(self, data):
        self.data = data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        metadata = self.data[idx]["metadata"]
        timelines = self.data[idx]["timelines"]
        
        # Metadata 및 타임라인 데이터 추출
        file_name = metadata["file_name"]
        video_length = metadata["length"]
        
        # 타임라인 데이터를 시간대 별로 분류
        timeline_data = []
        for timeline in timelines:
            start_time = timeline["start"]
            end_time = timeline["end"]
            label = timeline["variation"]
            
            timeline_data.append((start_time, end_time, label))
        
        # 데이터를 정렬하여 시간대에 맞게 배치
        timeline_data.sort(key=lambda x: x[0])
        
        return {
            "file_name": file_name,
            "video_length": video_length,
            "timeline_data": timeline_data
        }
