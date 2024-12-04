#!/usr/bin/env python
import sys
import re
import builtins

START_TOC_LN = 64
END_TOC_LN = 489

chapter_ln_p = re.compile("^[0-9][0-9]?\n$")
chapter_p = re.compile("^[A-Z][a-zA-Z ]*\n$")
section_p = re.compile(r"^[0-9]+\.[0-9]+ [A-Z]")
all_caps_p = re.compile("^[A-Z ]+\n$")
first_cap = re.compile("^[A-Z]")
first_lower = re.compile("^[a-z]")

def print(*args, **kwargs):
    return builtins.print(*args, end="", **kwargs)

def empty(l):
    return l == "\n"

def chapter_declaration(l):
    return (START_TOC_LN < ln and ln < END_TOC_LN and 
            empty(q[0]) and chapter_ln_p.match(q[1]) and 
            empty(q[2]) and chapter_p.match(l))

def form_feed(l):
    return ord(l[0]) == 12

def double_form_feed(l):
    return len(l) > 2 and ord(l[0]) == 12 and ord(l[1]) == 12

QL = 3
q = QL * [None]
def push(q, l):
    for i in range(QL-1):
        q[i] = q[i+1]
    q[QL-1] = l


skip = 0
chapters = []
ln = 1
for l in open(sys.argv[1]):
    ln += 1

    if skip != 0:
        skip -= 1
        continue

    if double_form_feed(l):
        continue
    elif form_feed(l): # ^L seem to be page headers
        skip = 3
        continue
    elif all_caps_p.match(l):
        skip = 1
        continue

    if chapter_declaration(l):
        chapters += [l]

    if first_cap.match(l):
        l += "\n"

    if l in chapters:
        l += "# "

    if section_p.match(l):
        l = "## " + ' '.join(l.split()[1:]) + "\n"

    push(q,l)
    if (ln > END_TOC_LN):
        if not (empty(q[2]) and first_lower.match(l)):
            print(q[2])

print(chapters)

