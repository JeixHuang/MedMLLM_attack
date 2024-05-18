import numpy as np
import matplotlib.pyplot as plt

# Load the six-dimensional matrix
six_dimensional_matrix = np.load("clip_all_six_dimensional_matrix_avg.npy")

# Define Model combinations
models = ["med-flamingo", "RadFM", "XrayGLM", "CheXagent"]
colors = ["red", "blue", "green", "orange"]

# Reduce dimensions to Model and Score, averaging over Policy, Attribute, Method, and Input
# Original shape: (Policy, Attribute, Model, Method, Input, Score)
# Target shape: (Model, Score)
reduced_matrix = np.mean(six_dimensional_matrix, axis=(0, 1, 3, 4))

# Validate shape
print(f"Reduced matrix shape: {reduced_matrix.shape}")  # Should be (4, 3)

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(20, 10), constrained_layout=True)

# Plot (text_score, asr) on the left subplot
for model_idx, model in enumerate(models):
    text_scores = reduced_matrix[model_idx, 0].flatten()
    asr = reduced_matrix[model_idx, 2].flatten()
    color = colors[model_idx]
    
    axs[0].scatter(text_scores, asr, color=color, s=100, label=model, alpha=0.6)

axs[0].set_xlabel('Text Score')
axs[0].set_ylabel('ASR')
axs[0].set_title('Text Score vs ASR')
axs[0].legend()

# Plot (img_score, asr) on the right subplot
for model_idx, model in enumerate(models):
    img_scores = reduced_matrix[model_idx, 1].flatten()
    asr = reduced_matrix[model_idx, 2].flatten()
    color = colors[model_idx]
    
    axs[1].scatter(img_scores, asr, color=color, s=100, label=model, alpha=0.6)

axs[1].set_xlabel('Image Score')
axs[1].set_ylabel('ASR')
axs[1].set_title('Image Score vs ASR')
axs[1].legend()

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('model_asr_scores.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
