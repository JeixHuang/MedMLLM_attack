import json
from analysis import analyze_csv_files_from_path

def load_config(config_path):
    """
    从给定路径加载配置文件。
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def main():
    config = load_config("config.json")
    input_path = config.get("input_path", "")
    column_name = config.get("column_name", "")
    output_path = config.get("output_path", "output.csv")

    if not input_path or not column_name:
        print("配置文件中未找到有效的输入路径或列名。")
        return

    analyze_csv_files_from_path(input_path, column_name, output_path)

if __name__ == "__main__":
    main()
