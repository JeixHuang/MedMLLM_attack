import tkinter as tk
from tkinter import ttk, PhotoImage
import pandas as pd
from PIL import Image, ImageTk
import os
import shutil  

def load_data(filepath):
    return pd.read_csv(filepath)

def create_image_label(window, path, row, column, columnspan):
    try:
        image = Image.open(path)
        image = image.resize((100, 100), Image.ANTIALIAS)  # Resize image
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(window, image=photo)
        label.image = photo  # Keep a reference!
        label.grid(row=row, column=column, columnspan=columnspan, sticky='W', padx=5, pady=5)
        
        # Save the image in a specified directory
        output_path = '/home/huangxijie/MedMLLM_attack/communication'
        save_path = os.path.join(output_path, os.path.basename(path))
        image.save(save_path)  # Save the resized image
        # Alternatively, to save the original image:
        # shutil.copy(path, save_path)
    except Exception as e:
        print(f"Error loading or saving image: {e}")
        label = ttk.Label(window, text="Image not available")
        label.grid(row=row, column=column, columnspan=columnspan, sticky='W', padx=5, pady=5)

def create_text_label(window, text, row, column, columnspan):
    label = ttk.Label(window, text=text, wraplength=400)
    label.grid(row=row, column=column, columnspan=columnspan, sticky='W', padx=5, pady=5)
    return label

def main():
    filepath = '/home/huangxijie/MedMLLM_attack/metric/normal_ret/med-flamingo-3MAD-Tiny-1K-respones.csv'
    data = load_data(filepath)
    
    window = tk.Tk()
    window.title("Dialogue Simulation")

    row = 0
    for index, entry in data.iterrows():
        # Adjust file path if needed
        image_path = os.path.join('/home/huangxijie/MedMLLM_attack/metric/', entry['file_name'])

        # Dialogue 1
        question1 = f"{image_path} + this is an image for {entry['original_attribute']} {entry['harmful_prompt']}"
        create_image_label(window, image_path, row, 0, 1)
        create_text_label(window, question1, row + 1, 0, 1)
        create_text_label(window, entry['malicious_response'], row + 2, 0, 1)

        # Dialogue 2
        question2 = f"{image_path} + this is an image for {entry['unmatch_attribute']} {entry['normal_prompt']}"
        create_image_label(window, image_path, row + 3, 0, 1)
        create_text_label(window, question2, row + 4, 0, 1)
        create_text_label(window, entry['unmatch_response'], row + 5, 0, 1)
        
        row += 6  # Adjust based on content size

    window.mainloop()

if __name__ == "__main__":
    main()
