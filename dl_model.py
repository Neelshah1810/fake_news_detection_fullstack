import torch
import numpy as np
import pandas as pd
from transformers import AutoModel, BertTokenizerFast
from sklearn.metrics import classification_report

# Define the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class BERT_Arch(torch.nn.Module):
    def __init__(self, bert):
        super(BERT_Arch, self).__init__()
        self.bert = bert
        self.dropout = torch.nn.Dropout(0.1)
        self.relu = torch.nn.ReLU()
        self.fc1 = torch.nn.Linear(768, 512)
        self.fc2 = torch.nn.Linear(512, 2)
        self.softmax = torch.nn.LogSoftmax(dim=1)

    def forward(self, sent_id, mask):
        cls_hs = self.bert(sent_id, attention_mask=mask, return_dict=True).pooler_output
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

# Load the model's state dict with strict=False to ignore unexpected keys
model = BERT_Arch(AutoModel.from_pretrained('bert-base-uncased'))
model.load_state_dict(torch.load('c1_fakenews_weights.pt', map_location=device), strict=False)
model.to(device)
model.eval()

tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

def predict_news(news_text):
    MAX_LENGTH = 15
    tokens_unseen = tokenizer(news_text, 
                              max_length=MAX_LENGTH, 
                              padding='max_length', 
                              truncation=True, 
                              return_tensors='pt')
    unseen_seq = tokens_unseen['input_ids'].to(device)
    unseen_mask = tokens_unseen['attention_mask'].to(device)

    with torch.no_grad():
        preds = model(unseen_seq, unseen_mask)
        preds = preds.detach().cpu().numpy()

    preds = np.argmax(preds, axis=1)
    return "Real News" if preds[0] == 1 else "Fake News"