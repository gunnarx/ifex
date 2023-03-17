#!/usr/bin/python

import sys, os, re

def h_to_link(h, n):
    hashes = '#' * n
    m = re.search('^' + hashes + ' (.*)', h)
    if m:
        text = m[1]
        indent = ' ' * 4 * (n-1)
        # lower case, remove non-alphabetic and replace space with -
        link = "".join(c for c in text if c.isalpha() or c == ' ').lower().replace(' ','-')
        return f"{indent}- [{text}](#{link})"
    return None

# Read given file, or from STDIN
if len(sys.argv) == 1:
    lines = sys.stdin.readlines()
else:
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()

headings = [h for h in lines if re.search('^#', h)]

for tocline in [h_to_link(h, n) for h in headings for n in range(1,5) if h_to_link(h, n)]:
	print(tocline)
