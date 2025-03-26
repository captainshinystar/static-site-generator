import os
import shutil
import sys
from website_functions import copy_static, generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "template.html"
basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]

def main():
    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_static(dir_path_static, dir_path_docs)
    
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)


if __name__ == "__main__":
    main()