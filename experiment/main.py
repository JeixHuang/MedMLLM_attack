from datasets import load_dataset
from PIL import Image
dataset = load_dataset("MedMLLM-attack/3MAD-70K")


# 假设你有 specific_model 和 specific_method 已经定义并实现了接口
model = specific_model('path/to/model')
method = specific_method(config={...})

for example in dataset['train']:
    image = Image.open(BytesIO(example['image']))
    text = example['text']

    # 应用优化方法
    optimized_image, optimized_text = method.apply(image, text)

    # 使用模型进行预测
    output = model.predict(optimized_image, optimized_text)
