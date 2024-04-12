import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas as pd
import os
import csv

def adjust_image_to_standard(source_image, standard_size=1024):
    original_width, original_height = source_image.size
    ratio = min(standard_size / original_width, standard_size / original_height)
    new_size = int(original_width * ratio), int(original_height * ratio)
    resized_image = source_image.resize(new_size, Image.Resampling.LANCZOS)
    new_image = Image.new("RGB", (standard_size, standard_size), "white")
    paste_coords = ((standard_size - new_size[0]) // 2, (standard_size - new_size[1]) // 2)
    new_image.paste(resized_image, paste_coords)
    return new_image

def create_text_block(text, font_path="arial.ttf", font_size=90, image_width=1024):
    font = ImageFont.truetype(font_path, font_size)
    line_height = int(font_size * 1.2)
    lines = textwrap.wrap(text, width=40)
    image_height = (len(lines) + 1) * line_height
    text_image = Image.new('RGB', (image_width, image_height), "white")
    draw = ImageDraw.Draw(text_image)
    y = line_height // 2
    for line in lines:
        text_width_approx = len(line) * font_size // 2
        x = (image_width - text_width_approx) // 2
        draw.text((x, y), line, fill="black", font=font)
        y += line_height
    return text_image

def concatenate_images(source_image_path, text):
    source_image = Image.open(source_image_path)
    adjusted_image = adjust_image_to_standard(source_image)
    text_image = create_text_block(text)
    final_image_height = 1024 + text_image.height
    final_image = Image.new('RGB', (1024, final_image_height), "white")
    final_image.paste(adjusted_image, (0, 0))
    final_image.paste(text_image, (0, 1024))
    final_image_path = source_image_path.rsplit('.', 1)[0] + "_final.png"
    final_image.save(final_image_path)
    return final_image_path

def build_dataset():
    data = pd.read_csv("sample_ret.csv")
    data['img_path'] = [getRandom() for _ in range(len(data))]
    # Ensure that key_phrases are strings and handle potential NaN values
    data['key_phrases'] = data['key_phrases'].fillna('No Key Phrase').apply(str)
    # Now, generate images
    data['img_typo'] = [concatenate_images(row['img_path'], row['key_phrases']) for index, row in data.iterrows()]
    data.to_csv('updated_dataset.csv', index=False)


def get_all_picture():
    img_paths = []
    file_paths = ["images"]
    for file_path in file_paths:
        imgs = os.listdir(file_path)
        for i in imgs:
            img_paths.append(os.path.join(file_path, i))
    return img_paths

def getRandom():
    paths = get_all_picture()
    return paths[random.randint(0, len(paths) - 1)]

get_all_picture()
build_dataset()
