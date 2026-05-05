from block import markdown_to_html_node
from pathlib import Path
import sys
from textnode import TextNode, TextType
from inline import split_nodes_link
import os
import shutil


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found")


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    template = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace('href="/', f'href="{base_path}')
        .replace('src="/', f'src="{base_path}')
    )
    if not dest_path.parent.exists():
        dest_path.parent.mkdir()

    with open(dest_path, "w") as f:
        f.write(template)


def copy_dir_recursive(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copy_dir_recursive(s, d)
        else:
            shutil.copy2(s, d)


def generate_pages_recursive(dir_path, template_path, dest_path, base_path):
    if not dest_path.exists():
        dest_path.mkdir()

    for item in os.listdir(dir_path):
        new_dest_path = dest_path / item
        if item.endswith(".md"):
            from_path = dir_path / item
            generate_page(
                from_path, template_path, new_dest_path.with_suffix(".html"), base_path
            )
        elif os.path.isdir(dir_path / item):
            generate_pages_recursive(
                dir_path / item, template_path, new_dest_path, base_path
            )


def main():
    if len(sys.argv) == 2:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    root = Path(__file__).parent.parent
    dest_path = root / "docs"
    static_path = root / "static"

    if dest_path.exists():
        shutil.rmtree(dest_path)

    copy_dir_recursive(static_path, dest_path)

    content_path = root / "content"
    template_path = root / "template.html"

    generate_pages_recursive(content_path, template_path, dest_path, base_path)


if __name__ == "__main__":
    main()
