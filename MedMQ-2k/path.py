import os

def generate_markdown_dir_tree(startpath):
    """Generate a markdown tree structure for the directory."""
    markdown_lines = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        markdown_lines.append('{}- **{}/**'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            markdown_lines.append('{}- {}'.format(subindent, f))
    return '\n'.join(markdown_lines)

# Usage: Specify your project root directory here
project_root = 'path/to/MedicalPromptGeneration'
markdown_content = generate_markdown_dir_tree(project_root)
print(markdown_content)

# Optionally write to a Markdown file
with open('directory_structure.md', 'w') as f:
    f.write(markdown_content)
