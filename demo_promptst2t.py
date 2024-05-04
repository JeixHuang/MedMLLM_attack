import pandas as pd
from metric.text2text_similarity import TextSimilarityCalculator
from metric.image2text_similarity import ImageTextSimilarity  
from metric.BiomedCLIP import ImageTextSimilarity_bio
import os


df = pd.read_csv('general_prompts.csv')

similarity_calculator_t2t = TextSimilarityCalculator()

result_df = pd.DataFrame(columns=['Policy', 'colbert', 'sparse', 'dense', 'sparse+dense', 'colbert+sparse+dense'])

for index, row in df.iterrows():
    column1_text = row['question']  
    column2_text = row['malicious_question']  
    

    similarity_score_dict = similarity_calculator_t2t.compute_similarity_text(column1_text, column2_text)
    
    policy = row['policy']  
    

    result_df = pd.concat([result_df, pd.DataFrame({'Policy': policy, **similarity_score_dict}, index=[0])], ignore_index=True)


result_df.to_csv('similarity_results.csv', index=False)

print(result_df)