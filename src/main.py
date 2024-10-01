from textnode import TextNode

def main():
    tn = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(tn)
    tn2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(tn==tn2)
    tn3 = TextNode("This is a node", "bold", "https://www.boot.dev")
    print(tn==tn3)
main()

