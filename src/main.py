import os
import shutil

from copystaticfiles import copy_files
from generatepage import generate_page

static_path = "./static"
dest_path = "./public"
content_path = "./content"
template_path = "./template.html"

def main():
    
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    copy_files("./static", "./public")

    print("Generating page...")
    generate_page(
        os.path.join(content_path, "index.md"),
        template_path,
        os.path.join(dest_path, "index.html"),
    )

if __name__ == "__main__":
    main()