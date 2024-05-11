import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate the perpendicular distance of a point from the line y=x
def perpendicular_distance(x, y):
    return abs(y - x) / np.sqrt(2)

# Specify the folder containing the CSV files
folder_path = '../metric/img2text_results'  # Update with your actual folder path

# Get all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# Prepare a dictionary to collect all data points
all_data = {}

# Create a color gradient from red to violet
color_count = len(csv_files)
colors = plt.cm.rainbow(np.linspace(0, 1, color_count))[::-1]  # Reverse to start from red

# Read each CSV file and collect data with colors
for i, csv_file in enumerate(csv_files):
    df = pd.read_csv(csv_file)
    if 'origin_score' in df.columns and 'unmatch_score' in df.columns:
        file_name = os.path.basename(csv_file).replace('.csv', '')
        all_data[file_name] = {
            'origin_scores': df['origin_score'].values,
            'unmatch_scores': df['unmatch_score'].values,
            'color': colors[i]
        }

# Check if any valid data was collected
if not all_data:
    raise ValueError("No valid data found in any CSV files.")

# Initialize the plot
plt.figure(figsize=(10, 10))

# Collect all data points across files for global calculations
global_origin_scores = []
global_unmatch_scores = []

# Plot all points from each file with unique colors
for file_name, data in all_data.items():
    global_origin_scores.extend(data['origin_scores'])
    global_unmatch_scores.extend(data['unmatch_scores'])
    plt.scatter(data['origin_scores'], data['unmatch_scores'], color=data['color'], alpha=0.6, label=file_name)

# Convert lists to numpy arrays for computation
global_origin_scores = np.array(global_origin_scores)
global_unmatch_scores = np.array(global_unmatch_scores)

# Calculate the perpendicular distances to the y=x line
distances = perpendicular_distance(global_origin_scores, global_unmatch_scores)
average_distance = np.mean(distances)

# Define x values for line plotting
x_values = np.linspace(min(global_origin_scores.min(), global_unmatch_scores.min()), max(global_origin_scores.max(), global_unmatch_scores.max()), 100)

# Plot the line y=x as a red dashed line
plt.plot(x_values, x_values, 'r--', label='y=x Line')

# Plot the bias line parallel to y=x but offset by the average distance, as a green dashed line
offset = average_distance * np.sqrt(2)
plt.plot(x_values, x_values + offset, 'g--', label=f'Bias Line (Offset by {offset:.2f})')

# Annotate the offset value within the plot, avoiding overlaps
plt.text(x_values[-1], x_values[-1] + offset, f'Offset: {offset:.2f}', fontsize=12, color='green', ha='left', va='bottom')

# Shade the region between the y=x line and the bias line
plt.fill_between(x_values, x_values, x_values + offset, color='grey', alpha=0.2, label='Impact Region')

plt.xlabel('Origin Score')
plt.ylabel('Unmatch Score')
plt.title('Scatter Plot with Highlighted Bias Line')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)

# Save the plot
output_path = 'med2med_scatter_plot_with_rainbow_bias_line.png'
plt.savefig(output_path, bbox_inches='tight')
plt.show()
print(f'Offset: {offset:.2f}')
