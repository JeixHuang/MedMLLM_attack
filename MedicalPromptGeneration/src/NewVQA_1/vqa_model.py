from transformers import AutoModelForQuestionAnswering, AutoTokenizer

class NewVQAModel:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_path)
        self.model.eval()

    def predict(self, image, question):
        # 对图像进行处理（如果模型需要图像特征）
        # 对问题进行处理
        inputs = self.tokenizer(question, return_tensors='pt')
        outputs = self.model(**inputs)
        answer = outputs[0]  # 根据模型的具体输出结构调整
        return answer
