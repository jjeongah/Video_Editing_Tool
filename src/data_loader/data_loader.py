from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, json_data):
        self.data = json_data["metadata"]
        self.timelines = json_data["timelines"]

    def __len__(self):
        return len(self.timelines)

    def __getitem__(self, idx):
        timeline = self.timelines[idx]
        start_time = timeline["start"]
        end_time = timeline["end"]
        attributes = timeline["attributes"]
        label = 0  # Set the label based on your criteria

        # Extract other relevant data from self.data if needed

        return {
            "start_time": start_time,
            "end_time": end_time,
            "attributes": attributes,
            "label": label
        }