import os
from pathlib import Path
from markdownnode import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    md_file_text = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    temp_file_text = template_file.read()
    template_file.close()

    md_html = markdown_to_html_node(md_file_text).to_html()
    page_title = extract_title(md_file_text)
    temp_file_html = temp_file_text.replace("{{Title}}", page_title).replace("{{Content}}", md_html)
    temp_file_html = temp_file_text.replace('href="/', f'href="{basepath}' ).replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(temp_file_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    os.makedirs(dest_dir_path, exist_ok=True)
    content_dir = os.listdir(dir_path_content)
    for item in content_dir:
        # make paths for copying
        content_path = os.path.join(dir_path_content, item)
        print(f"Content path: {content_path}")
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(content_path) and Path(content_path).suffix == ".md":       
            html_filename = Path(item).stem + ".html"
            html_dest_path = os.path.join(dest_dir_path, html_filename)
            generate_page(content_path, template_path, html_dest_path, basepath)
        elif os.path.isdir(content_path):
            generate_pages_recursive(content_path, template_path, dest_path, basepath)

    
    
    




