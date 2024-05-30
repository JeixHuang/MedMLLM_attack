import os
import pandas as pd

def get_average_scores(base_dir):
    methods = ["gcg", "pgd", "mcm"]
    models = ["med-flamingo", "RadFM", "XrayGLM", "CheXagent"]
    score_types = ["text_score_both", "img_score_both", "asr_score_both"]
    
    # Initialize a dictionary to store the average scores
    avg_scores = {method: {model: {score: 0 for score in score_types} for model in models} for method in methods}
    
    for method in methods:
        for model in models:
            file_path = os.path.join(base_dir, f"ret_{method}", "processed_ret", f"{model}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                for score in score_types:
                    avg_scores[method][model][score] = df[score].mean()
            else:
                print(f"File {file_path} does not exist")
    
    return avg_scores

def generate_latex_table(avg_scores):
    latex_str = """
    \\begin{table}[hbp]
    \\centering
    \\caption{Performance Scores for Different Models and Inputs}
    \\resizebox{\\textwidth}{!}{
    \\begin{tabular}{cccccccccccccccc}
    \\toprule
    \\multirow{2}{*}{Score Type} & \\multicolumn{3}{c}{Med-Flamingo} & \\multicolumn{3}{c}{RadFM} & \\multicolumn{3}{c}{XrayGLM} & \\multicolumn{3}{c}{CheXagent} \\
    \\cmidrule(lr){2-4} \\cmidrule(lr){5-7} \\cmidrule(lr){8-10} \\cmidrule(lr){11-13}
     & Text & Image & ASR & Text & Image & ASR & Text & Image & ASR & Text & Image & ASR \\\\
    \\midrule
    """
    for method, models in avg_scores.items():
        scores = []
        for model in models:
            scores.extend([f"{models[model]['text_score_both']:.4f}", f"{models[model]['img_score_both']:.4f}", f"{models[model]['asr_score_both']:.4f}"])
        latex_str += f"{method} & {' & '.join(scores)} \\\\\n"
    
    latex_str += """
    \\bottomrule
    \\end{tabular}}
    \\end{table}
    """
    
    return latex_str

# Define the base directory
base_dir = "transfer_experiment"

# Get the average scores
avg_scores = get_average_scores(base_dir)

# Generate the LaTeX table
latex_table = generate_latex_table(avg_scores)
print(latex_table)
