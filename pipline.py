import argparse
import subprocess
import os

def medical_prompt_generation():
    # 获取当前脚本的路径
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # 构建 medical prompt generation 脚本的路径
    medical_script_path = os.path.join(current_dir, 'MedicalPromptGeneration/src', 'main.py')
    # 调用 MedicalPromptGeneration 脚本
    result = subprocess.run(['python', medical_script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("MedicalPromptGeneration Output:")
        print(result.stdout)
    else:
        print("Error in MedicalPromptGeneration:", result.stderr)

def metric_text2text():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    text2text_script_path = os.path.join(current_dir, 'metric/text2text.py')
    # 调用文本相似性评估脚本
    result = subprocess.run(['python', text2text_script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("Text-to-Text Similarity Output:")
        print(result.stdout)
    else:
        print("Error in Text-to-Text Metric:", result.stderr)

def metric_text2image():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    text2image_script_path = os.path.join(current_dir, 'metric/text2image.py')
    # 调用图像文本相似性评估脚本
    result = subprocess.run(['python', text2image_script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("Text-to-Image Similarity Output:")
        print(result.stdout)
    else:
        print("Error in Text-to-Image Metric:", result.stderr)

def main():
    parser = argparse.ArgumentParser(description="Run medical prompt generation or similarity metrics.")
    parser.add_argument('command', choices=['medical', 'text2text', 'text2image'], 
                        help='Choose a command to execute: "medical" for medical prompt generation, "text2text" for text similarity, "text2image" for text to image similarity.')
    
    args = parser.parse_args()

    if args.command == 'medical':
        medical_prompt_generation()
    elif args.command == 'text2text':
        metric_text2text()
    elif args.command == 'text2image':
        metric_text2image()

if __name__ == "__main__":
    main()
