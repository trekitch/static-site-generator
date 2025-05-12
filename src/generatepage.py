import os
from markdownnode import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    md_file_text = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    temp_file_text = template_file.read()
    template_file.close()

    md_html = markdown_to_html_node(md_file_text).to_html()
    page_title = extract_title(md_file_text)
    temp_file_html = temp_file_text.replace("{{ Title }}", page_title).replace("{{ Content }}", md_html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(temp_file_html)

    
    
    




