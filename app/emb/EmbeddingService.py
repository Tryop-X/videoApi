from transformers import BertTokenizer, BertModel


class EmbeddingService:
    def __init__(self):
        self.TOKENIZER = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.MODEL = BertModel.from_pretrained('bert-base-multilingual-cased')

    def get_embedding(self, text):
        inputs = self.TOKENIZER(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = self.MODEL(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()
