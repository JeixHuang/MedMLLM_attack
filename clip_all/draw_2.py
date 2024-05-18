import numpy as np
import matplotlib.pyplot as plt

# Load the six-dimensional matrix
six_dimensional_matrix = np.load("clip_all_six_dimensional_matrix_avg.npy")

# Reduce dimensions to Input, Method, Model, and Score
reduced_matrix = np.mean(six_dimensional_matrix, axis=(0, 1))

# Define Input, Method, and Model combinations
inputs = ["unmatch", "both", "malicious"]
methods = ["gcg", "pgd", "mcm"]
models = ["med-flamingo", "RadFM", "XrayGLM", "CheXagent"]

# Function to generate colors based on model, method, and input
def generate_color(model_idx, method_idx, input_idx):
    red = int((model_idx) * (255 / (len(models) - 1)))
    green = int((method_idx) * (255 / (len(methods) - 1)))
    blue = int((input_idx) * (255 / (len(inputs) - 1)))
    return (red / 255, green / 255, blue / 255)

# Create subplots
fig, axs = plt.subplots(1, 4, figsize=(20, 10), gridspec_kw={'width_ratios': [4, 4, 0.3, 2]})

# Plot (text_score, asr) on the left subplot
for input_idx, input_type in enumerate(inputs):
    for method_idx, method in enumerate(methods):
        for model_idx, model in enumerate(models):
            text_scores = reduced_matrix[model_idx, method_idx, input_idx, 0]
            asr = reduced_matrix[model_idx, method_idx, input_idx, 2]
            color = generate_color(model_idx, method_idx, input_idx)
            axs[0].scatter(text_scores, asr, color=color)

axs[0].set_xlabel('Text Score')
axs[0].set_ylabel('ASR')
axs[0].set_title('Text Score vs ASR')

# Plot (img_score, asr) on the middle subplot
for input_idx, input_type in enumerate(inputs):
    for method_idx, method in enumerate(methods):
        for model_idx, model in enumerate(models):
            img_scores = reduced_matrix[model_idx, method_idx, input_idx, 1]
            asr = reduced_matrix[model_idx, method_idx, input_idx, 2]
            color = generate_color(model_idx, method_idx, input_idx)
            axs[1].scatter(img_scores, asr, color=color)

axs[1].set_xlabel('Image Score')
axs[1].set_ylabel('ASR')
axs[1].set_title('Image Score vs ASR')

# Create color gradients for reference
gradients = np.linspace(0, 1, 256).reshape(1, -1)
gradients = np.vstack((gradients, gradients))

# R Channel Gradient
axs[2].imshow(gradients, aspect='auto', cmap=plt.get_cmap('Reds'))
axs[2].set_title('R Channel')
axs[2].set_yticks([])
axs[2].set_xticks([])

# G Channel Gradient
axs[2].imshow(gradients, aspect='auto', cmap=plt.get_cmap('Greens'))
axs[2].set_title('G Channel')
axs[2].set_yticks([])
axs[2].set_xticks([])

# B Channel Gradient
axs[2].imshow(gradients, aspect='auto', cmap=plt.get_cmap('Blues'))
axs[2].set_title('B Channel')
axs[2].set_yticks([])
axs[2].set_xticks([])

# Combined color legend table
axs[2].axis('off')
table_data = []
for model_idx, model in enumerate(models):
    for method_idx, method in enumerate(methods):
        for input_idx, input_type in enumerate(inputs):
            color = generate_color(model_idx, method_idx, input_idx)
            table_data.append([model, method, input_type, color])

# Create table
columns = ["Model", "Method", "Input", "Color"]
cell_text = [[model, method, input_type, ''] for model, method, input_type, color in table_data]
cell_colors = [['white', 'white', 'white', color] for model, method, input_type, color in table_data]

table = axs[3].table(cellText=cell_text, colLabels=columns, cellColours=cell_colors, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.2, 1.2)

# Adjust layout
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1, wspace=0.3)

# Save the plot
plt.savefig('text_img_scores_with_color_reference.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
