from textnode import TextNode
import os
from generate_html_from_md import generate_page, generate_pages_recursive
from shutil import rmtree, copy
import re



def main():
    src = "./static/"
    dest = "./public/"
    cp_from_src_to_dest(src, dest)
    generate_pages_recursive("./content/", "template.html", "./public/")
    

def cp_from_src_to_dest(src, dest):
    if os.path.exists(dest):
        print(f"deleted {dest}")
        rmtree(dest)
    if os.path.isfile(src):
        copy(src, dest)
        print(f"copied file {src} to {dest}")
        return
    os.mkdir(dest)
    print(f"created dir from {src} to {dest}")
    contents = os.listdir(src)
    for item in contents:
        cp_from_src_to_dest(os.path.join(src, item),os.path.join(dest, item))

    

        

main()
