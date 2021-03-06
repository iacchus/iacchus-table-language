#!/usr/bin/env python

import re
import shlex

# preprocessor deals with sanitizing the input
# preprocessor:
#   checks for header
#   preprocesses header
#   removes the header line
#   remove # comments
#   remove empty lines
#   checks for indentation
#   delivers to parser a organized block to be processed
#
# parser deals with processing the sanitized input
# parser:
#   parses given the header info by preprocessor
#   parses indentation
#   parses especial characters
#   mount the columns with the header data given to it

# https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python

FILENAME = "test.itl"
with open(FILENAME, "r") as fd:
#     data = fd.readlines()
    data = fd.readlines()
#LINES = [line.expandtabs().strip('\n') for line in data]
LINES = [line.expandtabs() for line in data]

#print(LINES)

parsed = str()

indent = 0
groups = dict()
groupno = 0

for lineno, line in enumerate(LINES):

    if lineno == 0:
        print(shlex.split(line))
        if re.match('^itbl ', line):
            continue
        else:
            print('Not a legitimate ITML table. Exiting.')
            exit(1)

    match = re.match(r'^([ ]*)([\w\W]*)', line)
    line_indent = len(match[1])
    line_contents = match[2]

    print(indent, line_indent, line_contents)
    if line_indent == 0 and line_contents:
        groupno += 1
        groups.update({groupno: list() })
        groups[groupno].append(line_contents)
        #indent = line_indent  # new indent
        indent = 0  # new indent
    elif line_indent > 0 and line_contents:
        if indent == 0 or line_indent == indent:

            #if line_indent == indent:
                # then alright!

            indent = line_indent  # new indent
            groups[groupno].append(line_contents)

        else:
            print(f"Invalid indentation at line {lineno+1}.")
            exit(2)
            pass  # invalid indent!

    print(format(len(match[1]), "02d"), format(len(match[2]),"02d"), line)

#print(groups)
import pprint
pprint.pprint(groups.values())

# for key, value in groups.items():
#     groups.update({key: " ".join(value)})
#     print(key, groups[key])

# print(groups)
