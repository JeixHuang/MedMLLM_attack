import json


def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def main():
    config = load_config("config.json")
    imgselect_path = config.get("imgselect_path", "")
    randommatch_path = config.get("randommatch_path", "")
    count_path = config.get("count_path", "")
    output_path= config.get("count_path","3MAD-ret.csv")
    


if __name__ == "__main__":
    main()