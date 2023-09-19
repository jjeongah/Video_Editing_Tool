import torch
from torch.utils.data import Dataset, DataLoader

class TimelineDetectionModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(TimelineDetectionModel, self).__init__()
        self.lstm = torch.nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Use the final LSTM output for prediction
        return out