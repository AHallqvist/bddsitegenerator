import os
import shutil
import sys

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def _copy_directory_contents(source_dir, destination_dir):
    for entry in os.listdir(source_dir):
        source_path = os.path.join(source_dir, entry)
        destination_path = os.path.join(destination_dir, entry)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {source_path} -> {destination_path}")
        else:
            os.mkdir(destination_path)
            _copy_directory_contents(source_path, destination_path)


def copy_directory_recursive(source_dir, destination_dir):
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory does not exist: {source_dir}")

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    os.mkdir(destination_dir)
    _copy_directory_contents(source_dir, destination_dir)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as source_file:
        markdown = source_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    page_html = page_html.replace('href="/', f'href="{basepath}')
    page_html = page_html.replace('src="/', f'src="{basepath}')

    destination_dir = os.path.dirname(dest_path)
    if destination_dir:
        os.makedirs(destination_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as destination_file:
        destination_file.write(page_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(content_path):
            if not content_path.endswith(".md"):
                continue

            relative_path = os.path.relpath(content_path, dir_path_content)
            destination_file_path = os.path.join(dest_dir_path, relative_path).replace(".md", ".html")
            generate_page(content_path, template_path, destination_file_path, basepath)
            continue

        destination_subdir = os.path.join(dest_dir_path, entry)
        generate_pages_recursive(content_path, template_path, destination_subdir, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(project_root, "static")
    destination_dir = os.path.join(project_root, "docs")
    copy_directory_recursive(source_dir, destination_dir)

    generate_pages_recursive(
        os.path.join(project_root, "content"),
        os.path.join(project_root, "template.html"),
        os.path.join(project_root, "docs"),
        basepath,
    )


if __name__ == "__main__":
    main()

