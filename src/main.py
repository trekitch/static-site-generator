import os
import shutil

from copystaticfiles import copy_files
from generatepage import generate_page,generate_pages_recursive

static_path = "./static"
dest_path = "./public"
content_path = "./content"
template_path = "./template.html"

def main():
    
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    copy_files("./static", "./public")

    print("Generating page...")
    generate_pages_recursive(
        os.path.join(content_path),
        template_path,
        os.path.join(dest_path),
    )

if __name__ == "__main__":
    main()