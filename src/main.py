import os
import shutil
from pathlib import Path

from markdown_blocks import extarct_title, markdown_to_html_node


def main():
    public_path = '/home/jose/bootdev/static_site_generator/public/'
    static_path = '/home/jose/bootdev/static_site_generator/static/'
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    copy_files(static_path, public_path)
    generate_pages_recursive('./content/', './template.html', './public/')


def copy_files(current_path, destination):
    for f in os.listdir(current_path):
        joined_path = os.path.join(current_path, f)
        if os.path.isfile(joined_path):
            shutil.copy(joined_path, destination)
        else:
            new_destination = os.path.join(destination, f)
            os.mkdir(new_destination)
            copy_files(joined_path, new_destination)


def generate_page(from_path, template_path, dest_path):
    print(f'Generation page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, encoding='utf-8') as f:
        markdown = f.read()

    with open(template_path, encoding='utf-8') as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extarct_title(markdown)

    formatted_template = template.replace('{{ Title }}', title).replace('{{ Content }}', html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != '':
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(formatted_template)


def generate_pages_recursive(from_dir_path, template_path, dest_dir_path):
    for f in os.listdir(from_dir_path):
        origin_path = os.path.join(from_dir_path, f)
        new_dest_path = os.path.join(dest_dir_path, f)

        if os.path.isfile(origin_path):
            destination_path = Path(new_dest_path).with_suffix('.html')
            generate_page(origin_path, template_path, destination_path)
        else:
            generate_pages_recursive(origin_path, template_path, new_dest_path)


main()
