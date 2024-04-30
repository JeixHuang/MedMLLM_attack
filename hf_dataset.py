import base64
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
from datasets import Dataset
import datasets


def count_calls(func):
    # 这是一个闭包，用来存储函数调用次数
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print(f"{func.__name__} has been called {wrapper.calls} times")
        return func(*args, **kwargs)

    wrapper.calls = 0  # 初始化调用次数
    return wrapper


@count_calls
def image_to_base64(image_path):
    try:
        # 使用原始字符串来避免路径中的转义字符问题
        with Image.open(r"{}".format(image_path)) as image:
            if image.mode != "RGB":
                image = image.convert("RGB")
            np_img = np.asarray(image)
            pil_img = Image.fromarray(np.uint8(np_img))
            feature = datasets.Image()
            pil_img = feature.encode_example(pil_img)
            print(pil_img.keys())
            return pil_img
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return None
    except IOError:
        print(f"Cannot open image: {image_path}")
        return None
    except Exception as e:
        print(f"Error converting image {image_path} to base64: {e}")
        return None


# 读取CSV文件
df = pd.read_csv("3MAD-24K.csv")

# 替换图像路径为base64编码的字符串
df["img"] = df["img"].apply(image_to_base64)


# 将DataFrame转换为Hugging Face Dataset
dataset = Dataset.from_pandas(df)

# 上传到Hugging Face Hub（确保已经设置好认证）
dataset.push_to_hub("MedMLLM-attack/3MAD-24K")
