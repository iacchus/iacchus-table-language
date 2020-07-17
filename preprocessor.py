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
            with open(filename, "r") as fd:
                text = fd.readlines()

        if text:
            self.text = text
            self.process(text)


    def process(self, text):

        if isinstance(text, str):
            data = text.splitlines()
        elif isinstance(text, (list, tuple)):
            data = text


        lines = [line.expandtabs() for line in data]
        self.lines = lines


        if not self._process_header():
            raise('Not a legitimate ITML table (Header.) Exiting.')

        indent = 0
        groups = dict()
        groupno = 0

        for lineno, line in enumerate(lines):

            match = re.match(r'^(?P<blanks>[ ]*)(?P<text>[\w\W]*)', line)
            matches = match.groupdict()

            line_indent = len(matches['blanks'])
            line_contents = matches['text']
            blank_line = re.match('^[\n]$', line_contents)

            # line is a comment; continue for loop
            if re.match(r'^[\x20]*[#].*\n$', line_contents):
                continue

            # remove inline comments
            parsed_line = re.sub(r'[\x20]*[#].*\n', '\n', line_contents)

            if blank_line:

                if indent > 0:  # two subsequent newlines separate paragraphs
                                # when the text is indented
                    groups[groupno] += parsed_line

            # line has text
            elif line_indent == 0:
                groupno += 1
                groups.update({groupno: parsed_line})
                indent = 0  # new indent

            elif indent == 0 or line_indent == indent:
                indent = line_indent  # new indent
                #groups[groupno].append(parsed_line)
                groups[groupno] += parsed_line

            else:
                #print(f"Invalid indentation at line {lineno+1}.")
                raise(f"Invalid indentation at line {lineno+1}.")
                exit(2)

        self.groups = groups
        self.groupsno = len(groups)


    def _process_header(self):

        if len(self.lines) > 0:
            match = re.match(r'^itbl (.*)', self.lines[0])

        if len(match.groups()) == 1:
            self.columns = shlex.split(match[1])
            self.columnsno = len(self.columns)

        elif not match:
            return False

        return True

