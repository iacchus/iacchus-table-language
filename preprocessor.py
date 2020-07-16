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


class ITMLPreprocessor:


    def __init__(self, text=None, filename=None):

        if filename:
            with open(FILENAME, "r") as fd:
                text = fd.readlines()

        if text:
            self.text = text
            self.process(text)


    def process(self, text):

        if isinstance(text, str):
            data = text.splitlines()
        elif isinstance(text, (list, tuple)):
            data = text

        LINES = [line.expandtabs() for line in data]

        if len(LINES) > 0:
            header = LINES.pop(0)
            match = re.match(r'^itbl ([\w\W]*)', header)

        if len(match==2):
            self.columns = shlex.split(match[2])
            self.columnsno = len(self.columns)

        elif not match:
            #print('Not a legitimate ITML table. Exiting.')
            raise('Not a legitimate ITML table (Header.) Exiting.')

        indent = 0
        groups = dict()
        groupno = 0

        for lineno, line in enumerate(LINES):

            match = re.match(r'^([ ]*)([\w\W]*)', line)
            line_indent = len(match[1])
            line_contents = match[2]

            if line_contents:

                if line_indent == 0:
                    groupno += 1
                    groups.update({groupno: list() })
                    groups[groupno].append(line_contents)
                    #indent = line_indent  # new indent
                    indent = 0  # new indent

                elif indent == 0 or line_indent == indent:
                    indent = line_indent  # new indent
                    groups[groupno].append(line_contents)

                else:
                    print(f"Invalid indentation at line {lineno+1}.")
                    exit(2)

        self.groups = groups
        self.groupsno = len(groups)


