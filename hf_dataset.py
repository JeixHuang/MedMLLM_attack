import pandas as pd
from datasets import Dataset,Image
import time

df = pd.read_csv("CMIC-111k/3MAD-70K.csv")

# Get unique attribute values
attributes = df["original_attribute"].unique()

# Create a Hugging Face Dataset for each attribute value
for attribute in attributes:
    print(attribute)
    time.sleep(5)

    attribute_dataset = Dataset.from_pandas(df[df["original_attribute"] == attribute])
    attribute_dataset = attribute_dataset.map(lambda example: {"image": example["file_name"]}, batched=True)
    attribute_dataset = attribute_dataset.cast_column("image", Image())
    attribute_dataset.push_to_hub("MedMLLM-attack/3MAD-70K", split=attribute.split(" ")[-1], max_shard_size="1GB")
