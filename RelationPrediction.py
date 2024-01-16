import torch
import pandas as pd

from transformers import AutoModel, AutoConfig, AutoTokenizer
import os


df_train = pd.read_csv('parssimpleqa-train.csv')

class RPModel(torch.nn.Module):
    def __init__(self, pretrained_model):
        super(RPModel, self).__init__()
        self.bert = pretrained_model
        self.fc = torch.nn.Linear(self.bert.config.hidden_size, len(df_train['RP'].unique()))
        self.dropout = torch.nn.Dropout(self.bert.config.hidden_dropout_prob)

    def forward(self, input_ids, attention_mask, token_type_ids=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        pooled_output = outputs['last_hidden_state'][:, 0, :]  # Use the CLS token for classification
        pooled_output = self.dropout(pooled_output)
        logits = self.fc(pooled_output)
        return logits


def RP(new_sentence):



    parsbert_model_name = "HooshvareLab/bert-fa-zwnj-base"
    config = AutoConfig.from_pretrained(parsbert_model_name)
    parsbert_model = AutoModel.from_pretrained(parsbert_model_name)
    tokenizer = AutoTokenizer.from_pretrained(parsbert_model_name)
    save_directory = "RPmodel"  # Replace with your desired directory
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)

    # Load the fine-tuned RPmodel
    fine_tuned_model = RPModel(parsbert_model)
    fine_tuned_model.load_state_dict(torch.load(os.path.join(save_directory, "rp_model.pth"), map_location=torch.device('cpu')))
    fine_tuned_model.to(device)

    # Load the fine-tuned tokenizer
    fine_tuned_tokenizer = AutoTokenizer.from_pretrained(save_directory)
    #
    #
    # new_sentence = "محل مرگ حافظ کجا است؟"
    # # new_sentence = "بشیر التابعی کجا به دنیا آمده است؟"
    # new_sentence = "محل تولد بشیر التابعی کجاست"
    # # new_sentence = input('سوال خود را بپرسید')
    #
    # Tokenize the sentence
    tokenized_input = fine_tuned_tokenizer(new_sentence, return_tensors='pt', padding=True, truncation=True, max_length=512)
    label_dict = {label: idx for idx, label in enumerate(df_train['RP'].unique())}
    input_ids = tokenized_input['input_ids'].to(device)
    attention_mask = tokenized_input['attention_mask'].to(device)
    token_type_ids = tokenized_input.get('token_type_ids', None)  # Optional, only if your RPmodel requires it


    with torch.no_grad():
        fine_tuned_model.eval()
        outputs = fine_tuned_model(input_ids, attention_mask, token_type_ids=token_type_ids)
        predicted_class = torch.argmax(outputs, dim=1).item()


    print(new_sentence)
    predicted_label = list(label_dict.keys())[list(label_dict.values()).index(predicted_class)]
    print(predicted_label)
    return predicted_label
    #
    # # parts = predicted_label.split('_')
    # # print(parts)
    # # # Extract the part after the underscore (if available)
    # # if len(parts) > 1:
    # #     result = parts[1]
    # #     print(result)
#
# RP("محل مرگ حافظ کجا است؟")
