import re
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    split_lines = markdown.split("\n\n")
    split_lines = list(map(lambda x: x.strip(" "), split_lines))
    split_lines = list(filter(lambda x: x != "", split_lines))
    return split_lines

def block_to_block_type(block):
    '''
        paragraph - just a block of text
        heading - starts with 1-6 #, a space, then text
        code - starts and ends with ```
        quote - starts with >
        unordered_list - starts with * or - followed by space
        ordered_list - number followed by . and a space. Number must start
        at 1 and increment for each line
    '''
    if len(block) == 0:
        raise Exception("Bad block text was passed in")
    
    # quote block
    quote_check = block[0:1]
    if quote_check == ">":
        return block_type_quote

    # code block
    code_block_check = block.split("```")
    if len(code_block_check) == 3:
        return block_type_code

    # unordered list check
    if ( len(block) >= 2
        and block[0:1] in ["*", "-"]
            and block[1:2] == " "):
        return block_type_unordered_list

    # check for heading
    heading_block_check = re.findall(r"^#{1,6} ", block)
    if len(heading_block_check) > 0:
        return block_type_heading


    # check for ordered list
    split_lines = block.split("\n")
    count = 1
    for line in split_lines:
        pattern_check = re.findall(r"^(\d+). ", line)
        if len(pattern_check) == 0 or int(pattern_check[0]) != count:
            return block_type_paragraph
        count += 1


    # if nothing matches return paragraph
    return block_type_ordered_list


