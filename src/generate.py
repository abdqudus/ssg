import re
import os
import shutil
from markdown_helper_functions import markdown_to_html_node

def extract_title(markdown):
    pattern = r'^# ([^\n]+)'
    titles =re.findall(pattern,markdown,re.MULTILINE)
    if len(titles) == 0:
        raise ValueError('No Heading found')
    return [title.strip() for title in titles]


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r', encoding='utf-8') as file:
        from_content = file.read()

    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    
    html_string = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    template_content=template_content.replace('{{ Title }}',title[0])
    template_content = template_content.replace('{{ Content }}',html_string)

    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content = os.listdir(dir_path_content)
    for path_segment in content:
        new_src = os.path.join(dir_path_content,path_segment)
        dest_path = os.path.join(dest_dir_path,path_segment)
        is_md = os.path.isfile(new_src) and os.path.basename(new_src).endswith('.md')
        if is_md:
            dest_path= dest_path.replace('.md','.html')
            generate_page(new_src,template_path,dest_path)
        else:
            os.mkdir(dest_path,0o777)
            generate_pages_recursive(new_src,template_path,dest_path)

current_path = os.getcwd()
content = os.path.join(current_path,"content")
public = os.path.join(current_path,'public')
template_path = os.path.join(current_path,'template.html')