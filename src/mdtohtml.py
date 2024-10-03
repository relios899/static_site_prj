from typing import Text
from textnode import * 
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            res.append(node)
        else: 
            split_lines = node.text.split(delimiter)
            if len(split_lines) % 2 == 0:
                raise ValueError("invalid markdown syntax")
            nodes = []
            for i, line in enumerate(split_lines):
                if line == "":
                    continue
                if i % 2 == 0:
                    nodes.append(TextNode(line, text_type_text, None))
                else:
                    nodes.append(TextNode(line, text_type, None))
            res.extend(nodes)
    return res


def extract_markdown_image(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_link(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        images = extract_markdown_image(node.text)
        if len(images) == 0:
            res.append(node)
            continue

        new_text = node.text
        nodes = []
        for img in images:
            alt, img_link = img
            split_lines = new_text.split(f"![{alt}]({img_link})", 1)
            if split_lines[0] != "":
                nodes.append(TextNode(split_lines[0], "text"))
            nodes.append(TextNode(alt, text_type_image, img_link))
            new_text = split_lines[-1]
        if new_text != "":
            nodes.append(TextNode(new_text, "text"))
        res.extend(nodes)
    return res

def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        links = extract_markdown_link(node.text)
        if len(links) == 0:
            res.append(node)
            continue

        new_text = node.text
        nodes = []
        for link in links:
            alt, img_link = link 
            split_lines = new_text.split(f"[{alt}]({img_link})", 1)
            if split_lines[0] != "":
                nodes.append(TextNode(split_lines[0], "text"))
            nodes.append(TextNode(alt, text_type_link, img_link))
            new_text = split_lines[-1]
        if new_text != "":
            nodes.append(TextNode(new_text, "text"))
        res.extend(nodes)
    return res


def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    nodes = split_nodes_image([node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    return nodes

