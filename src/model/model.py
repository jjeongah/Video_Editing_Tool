import torch.nn as nn
from transformers import BertPreTrainedModel, BertModel

class TimelineDetectionModel(BertPreTrainedModel):
    def __init__(self, config):
        super(TimelineDetectionModel, self).__init__(config)
        self.num_labels = config.num_labels

        # Load the pre-trained BERT model
        self.bert = BertModel(config)

        # Add a classification head for timeline detection
        self.timeline_classifier = nn.Linear(config.hidden_size, self.num_labels)

        # Initialize the weights
        self.init_weights()

    def forward(self, input_ids, attention_mask=None):
        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask
        )

        # Use the pooled output for classification
        pooled_output = outputs.pooler_output

        # Pass the pooled output through the timeline classification head
        timeline_logits = self.timeline_classifier(pooled_output)

        return timeline_logits
