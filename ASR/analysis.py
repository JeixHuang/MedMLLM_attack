import os
import csv
import heapq
from moderation import violates_moderation_details

def top_3_negatives(category_scores):
    """
    从类别分数中识别出得分最高的 3 个负面类别。
    """
    top_3 = heapq.nlargest(3, category_scores.items(), key=lambda x: x[1])
    return top_3

def analyze_csv_files_from_path(path, column_name, output_path):
    """
    分析指定路径下的 CSV 文件，并从指定列中获取文本进行分析，将结果保存到新的 CSV 文件。
    """
    results = []

    if os.path.isfile(path) and path.endswith(".csv"):
        results.extend(analyze_csv(path, column_name))
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".csv"):
                results.extend(analyze_csv(os.path.join(path, filename), column_name))
    else:
        print(f"无效的路径或文件类型：{path}")

    write_results_to_csv(output_path, results)

def analyze_csv(file_path, column_name):
    """
    从给定的 CSV 文件中读取指定列的文本，分析每一行，返回结果。
    """
    results = []

    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if column_name not in reader.fieldnames:
                print(f"列 {column_name} 未在文件 {file_path} 中找到。")
                return results

            for row in reader:
                text = row[column_name]
                category_scores = violates_moderation_details(text)
                top_negatives = top_3_negatives(category_scores)
                results.append({"filename": os.path.basename(file_path), "text": text, "top_negatives": top_negatives})

    except Exception as e:
        print(f"读取文件 {file_path} 时出错：{e}")

    return results

def write_results_to_csv(output_path, results):
    """
    将分析结果写入到新的 CSV 文件中。
    """
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["filename", "text", "category", "score"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                for category, score in result["top_negatives"]:
                    writer.writerow({"filename": result["filename"], "text": result["text"], "category": category, "score": score})

    except Exception as e:
        print(f"写入文件 {output_path} 时出错：{e}")
