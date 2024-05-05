import pandas as pd
from metric.image2text_similarity import ImageTextSimilarity
from metric.BiomedCLIP import ImageTextSimilarity_bio
from PIL import Image
import os

# Setup similarity calculators
similarity_calculator_i2t = ImageTextSimilarity()  
similarity_calculator_i2t_bio = ImageTextSimilarity_bio()

def process_image_text_similarity(row):
    # Load the image from the file path
    image_path = row['file_name']  # 确保这是一个路径
    image = Image.open(image_path)

    # 使用路径而不是图像对象
    score_clip_original = similarity_calculator_i2t.calculate_similarity_path(image_path, row['original_attribute'])
    score_clipbio_original = similarity_calculator_i2t_bio.calculate_similarity_path(image_path, row['original_attribute'])
    score_clip_unmatch = similarity_calculator_i2t.calculate_similarity_path(image_path, row['unmatch_attribute'])
    score_clipbio_unmatch = similarity_calculator_i2t_bio.calculate_similarity_path(image_path, row['unmatch_attribute'])

    return pd.Series({
        'Score_CLIP_original': score_clip_original,
        'Score_CLIPbio_original': score_clipbio_original,
        'Score_CLIP_unmatch': score_clip_unmatch,
        'Score_CLIPbio_unmatch': score_clipbio_unmatch
    })

def main():
    # Load the dataset
    df = pd.read_csv('CMIC-111k/3MAD-70K.csv')

    # Process each image and text, and store results
    results = df.apply(process_image_text_similarity, axis=1)
    final_df = pd.concat([df[['id', 'file_name', 'original_attribute', 'unmatch_attribute']], results], axis=1)

    # Save results to CSV
    final_df.to_csv('ret_dataset.csv', index=False)
    print("Results saved to ret_dataset.csv")

if __name__ == "__main__":
    main()
