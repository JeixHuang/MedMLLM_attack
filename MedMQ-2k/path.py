import os

def generate_markdown_dir_tree(startpath):
    """Generate a markdown directory tree with annotations for each directory and file."""
    ignore = ['.git', '__pycache__']  # 忽略列表，避免遍历不必要的目录
    lines = ["# Project Directory Tree\n", "```\n"]  # 开始构建Markdown文本
    for root, dirs, files in os.walk(startpath, topdown=True):
        # 排除一些不必要的目录
        dirs[:] = [d for d in dirs if d not in ignore]
        files = [f for f in files if f not in ignore]

        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        if os.path.basename(root) == os.path.basename(startpath):
            lines.append(os.path.basename(startpath) + "/\n")
        else:
            lines.append(indent + os.path.basename(root) + '/\n')

        subindent = '│   ' * level + '├── '
        for fname in files:
            lines.append(subindent + fname + '\n')

    lines.append("```")
    return "".join(lines)

# Specify your project root directory here
project_root = 'MedMQ-2k/Ultrasound'
markdown_content = generate_markdown_dir_tree(project_root)

# Print the output to the console
print(markdown_content)

# Optionally, write the output to a Markdown file
with open('directory_structure.md', 'w') as file:
    file.write(markdown_content)
