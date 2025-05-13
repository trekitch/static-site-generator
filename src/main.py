import os
import shutil
import sys

from copystaticfiles import copy_files
from generatepage import generate_page,generate_pages_recursive

# Check if there's at least one argument after the script name
if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

static_path = "./static"
dest_path = "./docs"
content_path = "./content"
template_path = "./template.html"

def main():
    
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    copy_files("./static", "./docs")

    print("Generating page...")
    generate_pages_recursive(
        os.path.join(content_path),
        template_path,
        os.path.join(dest_path),
        basepath
    )

if __name__ == "__main__":
    main()