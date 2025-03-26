import shutil
import os
from pathlib import Path
from block_functions import markdown_to_html_node


def copy_static(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for item in os.listdir(source_dir_path):
        source_item = os.path.join(source_dir_path, item)
        dest_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(source_item):
            print(f"Copying file: {source_item} to {dest_item}")
            shutil.copy(source_item, dest_item)
        else:
            print(f"Copying directory {source_item} to {dest_item}")
            copy_static(source_item, dest_item)

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        contents = f.read()
    with open(template_path) as f:
        template = f.read()
    html_node = markdown_to_html_node(contents)
    html = html_node.to_html()
    title = extract_title(contents)
    updated_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(updated_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)