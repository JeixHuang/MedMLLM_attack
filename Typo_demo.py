import random

from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas as pd
import os
import csv


def adjust_image_to_standard(source_image, standard_size=1024):
    """Resize or pad the image to fit the 1024x1024 standard size."""
    original_width, original_height = source_image.size

    # Calculate the new size maintaining the aspect ratio
    ratio = min(standard_size / original_width, standard_size / original_height)
    new_size = int(original_width * ratio), int(original_height * ratio)
    resized_image = source_image.resize(new_size, Image.Resampling.LANCZOS)

    # Create a new image with a white background
    new_image = Image.new("RGB", (standard_size, standard_size), "white")
    # Calculate top-left corner coordinates to paste the resized image
    paste_coords = ((standard_size - new_size[0]) // 2, (standard_size - new_size[1]) // 2)
    new_image.paste(resized_image, paste_coords)

    return new_image


def create_text_block(text, font_path="arial.ttf", font_size=90, image_width=1024):
    """Create an image block of text, trying to bypass the 'textsize' issue."""
    font = ImageFont.truetype(font_path, font_size)
    line_height = int(font_size * 1.2)
    lines = textwrap.wrap(text, width=40)  # This might need adjustment

    image_height = (len(lines) + 1) * line_height
    text_image = Image.new('RGB', (image_width, image_height), "white")
    draw = ImageDraw.Draw(text_image)

    y = line_height // 2  # Start half a line height down
    for line in lines:
        # An alternative approach to bypass direct 'textsize' call
        # We approximate the centering by using the string length, not perfect but should work for a demo
        text_width_approx = len(line) * font_size // 2  # Rough approximation
        x = (image_width - text_width_approx) // 2  # Center based on approximation
        draw.text((x, y), line, fill="black", font=font)
        y += line_height

    return text_image


def concatenate_images(source_image_path, text):
    """Concatenate the source image and the text block."""
    source_image = Image.open(source_image_path)
    adjusted_image = adjust_image_to_standard(source_image)
    text_image = create_text_block(text)

    final_image_height = 1024 + text_image.height
    final_image = Image.new('RGB', (1024, final_image_height), "white")
    final_image.paste(adjusted_image, (0, 0))
    final_image.paste(text_image, (0, 1024))

    final_image_path = source_image_path.rsplit('.', 1)[0] + "_final.png"
    final_image.save(final_image_path)


img_paths = []


def get_all_picture():
    file_paths = ["dataset/teeth"]
    num = 0
    for file_path in file_paths:
        imgs = os.listdir(file_path)
        for i in imgs:
            img_paths.append([num, '{}/{}'.format(file_path, i)])
            num += 1
    print(img_paths)
    csv_headers = ['序号', '路径']
    data = pd.DataFrame(columns=csv_headers, data=img_paths)  # 将数据放进表格
    # #data.to_csv("myfile.csv", header=csv_headers, index=False, mode='a+', encoding='utf-8')
    data.to_csv('all_image_path.csv')
    
def getRandom():
    data = pd.read_csv("all_image_path.csv")
    paths = []
    for index, row in data.iterrows():
        paths.append(row["路径"])
    return paths[random.randint(1, len(paths)-1)]

# Example usage

source_image_path = getRandom()  # Adjust with your actual image path
key_phrases = source_image_path.split("/")[1]
concatenate_images(source_image_path, key_phrases)
