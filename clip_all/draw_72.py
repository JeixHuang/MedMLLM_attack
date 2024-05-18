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
colors = ["red", "blue", "green", "orange"]

# Create subplots
fig, axs = plt.subplots(3, 3, figsize=(20, 20), constrained_layout=True)

# Plot scores and ASR
for method_idx, method in enumerate(methods):
    for input_idx, input_type in enumerate(inputs):
        ax = axs[method_idx, input_idx]
        
        for model_idx, model in enumerate(models):
            text_scores = reduced_matrix[model_idx, method_idx, input_idx, 0].flatten()
            img_scores = reduced_matrix[model_idx, method_idx, input_idx, 1].flatten()
            asr = reduced_matrix[model_idx, method_idx, input_idx, 2].flatten()
            color = colors[model_idx]
            
            # Scatter plot for text_score
            ax.scatter(asr, text_scores, color=color, s=50, label=f"{model} - Text Score", alpha=0.6)
            
            # Scatter plot for img_score with a secondary y-axis
            ax2 = ax.twinx()
            ax2.scatter(asr, img_scores, color=color, s=50, marker='x', label=f"{model} - Image Score", alpha=0.6)
            
        ax.set_title(f"Method: {method}, Input: {input_type}")
        ax.set_xlabel('ASR')
        ax.set_ylabel('Text Score (0-1)')
        ax2.set_ylabel('Image Score (0-25)', rotation=270, labelpad=15)
        
        # Combine legends from both y-axes
        handles1, labels1 = ax.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(handles1 + handles2, labels1 + labels2, loc='upper right')

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('model_method_input_scores_9_plots.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
