#!/bin/python

# These little functions can rewrite several bytes in a str (usually read from a binary file)
# In wrapper rewrite32*, content can be: int/str/string of hex

def rewrite(s, offset, size, content):
    if not isinstance(s,str) or len(content) != size:
        raise Exception
    return s[:offset]+content+s[offset+size:]

def rewrite32(s, offset, content):
    if isinstance(content, int):
        content=("%08X" % content).strip().decode("hex")
    elif isinstance(content,str) and len(content)>4:
        if content.startswith("0x"):
            content=content[2:]
        content=content.strip().decode("hex")
    return rewrite(s, offset, 4, content)

def rewrite32_little_endian(s, offset, content):
    if isinstance(content, int):
        content=("%08x" % content).strip().decode("hex")
    elif isinstance(content,str) and len(content)>4:
        if content.startswith("0x"):
            content=content[2:]
        content=content.strip().decode("hex")
    content = content[::-1]
    return rewrite(s, offset, 4, content)
