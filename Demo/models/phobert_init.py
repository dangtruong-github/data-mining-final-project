from transformers import AutoTokenizer, AutoModelForSequenceClassification

import torch
import json

from torch import nn

class FineTuneModel(nn.Module):
    def __init__(self, main_model):
        super(FineTuneModel, self).__init__()
        self.main_model = main_model
        self.sigmoid = nn.Sigmoid()
    def forward(self, input_ids, attention_mask):
        x = self.main_model(input_ids, attention_mask).logits
        x = self.sigmoid(x)
        return x
    
def prepare_model_and_token(mode, text):
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
    phobert_model_pretrained = AutoModelForSequenceClassification.from_pretrained("vinai/phobert-base", num_labels = 8)

    model = FineTuneModel(main_model = phobert_model_pretrained)

    # đến đây để nguyên như này, tokenizer thì mình import ở trên rồi
    token = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=256,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_tensors="pt"
    )

    model.load_state_dict(torch.load("./models/pho_bert_models/{}.pth".format(mode), map_location=torch.device('cpu')))

    return model, token

def predict(mode, text):
    model, token = prepare_model_and_token(mode, text)

    input_ids = token.input_ids
    attention_mask = token.attention_mask

    threshold = None

    with open("./models/pho_bert_models/threshold.json", "r") as file:
        f = json.load(file)
        threshold = f[mode]

    output = None

    with torch.no_grad():
        model.eval()
        output = model(input_ids, attention_mask)

    output = output.tolist()

    return output[0], threshold