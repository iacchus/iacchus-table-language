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

HEADER_TAG = "itbl"

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

        if len(data) == 0:
            raise('Input is empty.')

        if not self._check_header(lines[0]):
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

            # we should think on a better way of handling TABS then enforcing
            # the user no not use it.
            if re.match(r'\t', line_contents):
                raise('TAB character at line {lineno+1}. Please use 4 spaces'
                      ' instead of tab.')

            # line is a comment; continue `for` loop
            if re.match(r'^[\x20]*[#].*\n$', line_contents):
                continue

            # remove inline comments
            parsed_line = re.sub(r'[\x20]*[#].*\n', '\n', line_contents)

            if blank_line:

                if indent > 0:  # two subsequent newlines separate paragraphs
                                # when the text is indented
                    groups[groupno] += parsed_line

            # line has text and is not indented
            elif line_indent == 0:
                groupno += 1
                groups.update({groupno: parsed_line})
                indent = 0  # new indent

            # line is indented. was the previous line `indent` == 0 and this
            # is an indented continuation of it?
            # or this is a continuation of the previous already intended line
            # with the same indentation?
            elif indent == 0 or line_indent == indent:
                indent = line_indent  # new indent
                groups[groupno] += parsed_line

            # line is indented but it's indentation is not equal the previous
            # indented line(s)
            else:
                raise(f"Invalid indentation at line {lineno+1}.")

        self.groups_dict = groups
        self.groups_list = list(groups.values())
        self.groupsno = len(groups)

        self._process_header(self.groups_list[0])

    def _check_header(self, line):

        header_match = re.match('^{header_tag} '.format(header_tag=HEADER_TAG),
                                line)

        return header_match

    def _process_header(self, header):

        parsed_header = re.sub(r'^{header_tag}[ ]+'.format(header_tag=
                                                           HEADER_TAG),
                               '', header)

        parsed_header = re.sub(r'\n\n$', '', parsed_header)
        parsed_header = re.sub(r'\\[ ]*\n', '', parsed_header)
        parsed_header = re.sub(r'\n', ' ', parsed_header)

        self.columns = shlex.split(parsed_header)
        self.columnsno = len(self.columns)

        return True

