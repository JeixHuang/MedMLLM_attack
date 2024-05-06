# import pandas as pd
# from datasets import Dataset,Image
# import time

# df = pd.read_csv("CMIC-111k/3MAD-70K.csv")

# # Get unique attribute values
# attributes = df["original_attribute"].unique()

# # Create a Hugging Face Dataset for each attribute value
# for attribute in attributes:
#     print(attribute)
#     time.sleep(5)

#     attribute_dataset = Dataset.from_pandas(df[df["original_attribute"] == attribute])
#     attribute_dataset = attribute_dataset.map(lambda example: {"image": example["file_name"]}, batched=True)
#     attribute_dataset = attribute_dataset.cast_column("image", Image())
#     split_name = attribute.replace(" and ", "_")
#     print(split_name)
#     attribute_dataset.push_to_hub(
#         "MedMLLM-attack/3MAD-70K", split=split_name, max_shard_size="1GB"
#     )


import datasets

dataset = datasets.load_dataset(
    "MedMLLM-attack/3MAD-70K", num_proc=10
)

df = dataset["Ultrasound_Breast"].to_pandas()
df = df[df["file_name"] != "CMIC-111k/Ultrasound/Breast/benign__156_.png"]
df = df[df["file_name"] != "CMIC-111k/Ultrasound/Breast/normal__17_.png"]
df = df[df["file_name"] != "CMIC-111k/Ultrasound/Breast/benign__290_.png"]

import pandas as pd
from datasets import Dataset, Image
import time


# Create a Hugging Face Dataset for each attribute value
attribute = "Ultrasound_Breast"
# df = df.drop(columns=["__index_level_0__"])
print(attribute)
print(df.head())


attribute_dataset = Dataset.from_pandas(
    df[df["original_attribute"] == "Ultrasound and Breast"]
)
attribute_dataset = attribute_dataset.map(
    lambda example: {"image": example["file_name"]}, batched=True
)
attribute_dataset = attribute_dataset.cast_column("image", Image())

print(attribute_dataset)
# print(attribute_dataset["image"])

for sample in df["image"]:
    print(type(sample))

print(attribute_dataset["__index_level_0__"])


# attribute_dataset.push_to_hub(
#     "MedMLLM-attack/3MAD-70K", split=attribute, max_shard_size="1GB"
# )
