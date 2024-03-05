import os
from bs4 import BeautifulSoup

exclude_dirs = {'.git', '.github', 'node_modules'}

def update_script_js(nav_links_str):
    try:
        with open('script.js', 'r') as file:
            lines = file.readlines()
        lines[0] = f'const menu = `{nav_links_str}`;\n'
        with open('script.js', 'w') as file:
            file.writelines(lines)
    except IOError:
        print("Error updating script.js")

def read_html_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError:
        print(f"Error reading file: {file_path}")
        return None

def generate_nav_link(filename, title, is_root=False):
    # Correctly format the file path for URLs
    href = os.path.join(os.path.dirname(filename), os.path.basename(filename))
    # Replace backslashes with forward slashes and encode spaces
    href = href.replace('\\', '/')
    if not is_root:
        href = '/' + href  # Ensure the path is absolute
    return f'<a href="{href}">{title}</a>'



def sort_links(item):
    filename, title = item
    return '' if title == 'Home' else title

def update_menu_structure(root, dirs, files):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    links_dict = {}
    is_root = os.path.basename(root) == os.path.basename('.')

    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            title = get_title_from_file(filepath)
            rel_path = os.path.relpath(filepath, start=".")  # Get relative path from root
            label = os.path.basename(root) if not is_root else "Home"
            if label not in links_dict:
                links_dict[label] = []
            links_dict[label].append(generate_nav_link(rel_path, title, is_root))

    return links_dict

def get_title_from_file(file_path):
    contents = read_html_file(file_path)
    if contents:
        soup = BeautifulSoup(contents, 'html.parser')
        return soup.title.string if soup.title else "No title"
    return "No title"

menu_start = "<div class=\"menu\"><div class=\"accordion\">"
menu_end = "</div><button class=\"button\" id=\"Btn\"><i class='bx bx-menu bx-burst' style='color:#54d82d' ></i></button></div>"

all_links_dict = {}

for root, dirs, files in os.walk("."):
    links_dict = update_menu_structure(root, dirs, files)
    for label in links_dict:
        if label not in all_links_dict:
            all_links_dict[label] = []
        all_links_dict[label].extend(links_dict[label])

menu_html = menu_start
for label, links in all_links_dict.items():
    if label == "Home":
        menu_html += f'<div class="contentBox"><div class="label">{"".join(links)}</div><div class="content"></div></div>'
    else:
        links_html = ''.join(links)
        menu_html += f'<div class="contentBox"><div class="label">{label}</div><div class="content">{links_html}</div></div>'
menu_html += menu_end

print(f"Final menu HTML: {menu_html}")

update_script_js(menu_html)
