import os
import shutil
from htmlnode import markdown_to_html_node

def copy_from_static_to_public(targetdir):
    shutil.rmtree(targetdir)
    os.mkdir(targetdir)
    rec_copy_file_to_route('static',targetdir)
    pass

def rec_copy_file_to_route(origin_route, target_route):
    files = os.listdir(origin_route)
    for file in files:
        filepath = os.path.join(origin_route, file)
        targetpath = os.path.join(target_route, file)
        if os.path.isfile(filepath):
            shutil.copy(filepath, targetpath)
        else:
            if not os.path.exists(targetpath):
                os.mkdir(targetpath)
            rec_copy_file_to_route(filepath, targetpath)
    pass

def extract_title(markdown):
    lines = markdown.split("\n")
    header = None
    for line in lines:
        if line.startswith("# ") and header == None:
            header = line.replace("# ", "")
    if header == None:
        raise Exception("No header found")
    else:
        return header

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_contents = ""
    from_file = open(from_path, "r")
    lastline = "0"
    while(lastline != ""):
        lastline = from_file.readline()
        from_contents += lastline
    from_file.close()
    template_contents = ""
    template_file = open(template_path, "r")
    lastline = "0"
    while(lastline != ""):
        lastline = template_file.readline()
        template_contents += lastline
    template_file.close()
    htmlnode= markdown_to_html_node(from_contents)
    headertext = extract_title(from_contents)
    final_contents = template_contents
    final_contents = final_contents.replace("{{ Title }}", headertext)
    final_contents = final_contents.replace("{{ Content }}", htmlnode.to_html())
    final_contents = final_contents.replace("href=\"/", f"href=\"{basepath}")
    final_contents = final_contents.replace("src=\"/", f"src=\"{basepath}")
    dirname = os.path.dirname(dest_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    dest_file = open(dest_path, "w")
    dest_file.write(final_contents)
    dest_file.close()
    pass

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_files = os.listdir(dir_path_content)
    dest_files = os.listdir(dir_path_content)
    for content_file in content_files:
        new_content_path = os.path.join(dir_path_content, content_file)
        new_dest_path = os.path.join(dest_dir_path, content_file)
        if os.path.isfile(new_content_path):
            if new_content_path.endswith(".md"):
                new_dest_path = new_dest_path[:-len(".md")] + ".html"
                generate_page(new_content_path, template_path, new_dest_path, basepath)
        else:
            generate_pages_recursive(new_content_path, template_path, new_dest_path, basepath)