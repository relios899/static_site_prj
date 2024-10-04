from os.path import dirname, exists
from re import split
from htmlnode import *
from leafnode import *
from parentnode import *
from blocktohtml import *
from mdtohtml import *
from textnode import *
import os

'''
    Conversions:
    md heading to appropriate headings (h1-h6)
    
'''
paragraph_tag = "p"
code_tag = "code"
quote_tag = "blockquote"
unordered_list_tag = "ul"
ordered_list_tag = "ol"
list_item_tag = "li"

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown) 
    parent_nodes = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        tag = None
        text = None
        node = None
        if block_type == block_type_heading:
            tag = determine_type_of_header_tag(block)
            text = strip_md_block_id_from_text(block, block_type)
            node = generate_nodes(tag, text)
        elif block_type == block_type_paragraph:
            tag = paragraph_tag
            lines = block.split("\n")
            text = " ".join(lines)
            node = generate_nodes(tag, text)
        elif block_type == block_type_code:
            tag = code_tag
            text = strip_md_block_id_from_text(block, block_type)
            node = generate_nodes(tag, text)
            node = ParentNode("pre", [node])
        elif block_type == block_type_quote:
            tag = quote_tag
            text = strip_md_block_id_from_text(block, block_type)
            node = generate_nodes(tag, text)
        elif block_type == block_type_unordered_list:
            tag = unordered_list_tag
            node = generate_nodes_for_lists(tag, block)
        elif block_type == block_type_ordered_list:
            tag = ordered_list_tag
            node = generate_nodes_for_lists(tag, block)
            
        if node is None:
            raise ValueError("Node cannot be None")
        parent_nodes.append(node)

    main_node = ParentNode("div", parent_nodes)
    return main_node

def generate_nodes_for_lists(tag, block):
    list_items = block.split("\n")
    items = []
    for item in list_items:
        split_item = item.split(" ", 1)
        text = split_item[1]
        items.append(generate_nodes(list_item_tag, text))
    node = ParentNode(tag, items)
    return node

def generate_nodes(tag, text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    node = ParentNode(tag, leaf_nodes)
    return node
    
def determine_type_of_header_tag(block):
    header_markers_and_text = block.split(' ')
    md_header_type = len(header_markers_and_text[0])
    match md_header_type:
        case 1:
            return "h1"
        case 2:
            return "h2"
        case 3:
            return "h3"
        case 4:
            return "h4"
        case 5:
            return "h5"
        case 6:
            return "h6"
            
def strip_md_block_id_from_text(block, block_type):
    if block_type == block_type_heading:
        split_block = block.split(' ', maxsplit = 1)
        return split_block[-1]
    if block_type == block_type_code:
        split_block = block.split("```")
        return split_block[1].strip()
    if block_type == block_type_quote:
        return block[1:].strip()
        
def extract_title(markdown):
    split_md = markdown.split("\n")        
    for split in split_md:
        check = re.findall(r"^# ", split)
        if len(check) > 0:
            return split[1:].strip()


def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path).read()
    template_file = open(template_path).read()
    html_node = markdown_to_html_node(md_file)
    html_str = html_node.to_html()
    html_title = extract_title(md_file)
    # might need to look into title with spaces
    
    template_file = template_file.replace("{{ Title }}", str(html_title))
    template_file = template_file.replace("{{ Content }}", html_str)
    create_file_at_dest(dest_path, template_file)


def create_file_at_dest(dest_path, file_to_write):
    dirs_to_create = os.path.dirname(dest_path)
    if not os.path.exists(dirs_to_create):
        print(f"creating directories {dirs_to_create}")
        os.makedirs(dirs_to_create)
    
    f = open(dest_path, "w")
    f.write(file_to_write)
    f.close()



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        dest_dir_path = dest_dir_path.replace(".md",".html")
        generate_page(dir_path_content, template_path, dest_dir_path)
        return
    for item in os.listdir(dir_path_content):
        generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item))


