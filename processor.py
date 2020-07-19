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


class Table:
    columns = list()
    columnsno = int()

    def __init__(self):
        pass

class Cell:

    pos = tuple()

    def __init__(self):
        pass

class ITMLProcessor:


    def __init__(self, preprocessed_data):

        self.data = preprocessed_data

        self.columns = self._process_header(preprocessed_data)
        self.columnsno = len(self.columns)

        self.process(preprocessed_data)


    def process(self, data):

        self.parsed_list = list()

        for index, item in enumerate(data):

            if index == 0:  # raw header line
                self._process_header(item)

            parsed = self._process_text(item)

            split_paragraphs = re.split(r'\n\n', parsed)  # split paragraphs

            self.parsed_list.append(tuple(split_paragraphs))


    def _process_text(self, text):

        parsed = text

        # newlines at the end of string. They're already encapsulated
        parsed = re.sub(r'[\n]*\n$', '', parsed)

        # no ending whitespace after \ and newline
        parsed = re.sub(r'\\[\x20]*\n', '', parsed)

        # join continuing (indented) lines with a space
        parsed = re.sub(r'(?<=.)\n(?=.)', ' ', parsed)

        return parsed


    def _process_header(self, preprocessed_data):
        """Processes the itml table header line(s)

        Processes the ITML table header and returns the columns.
        """

        parsed_header = re.sub(f'^{HEADER_TAG}[ ]+', '', preprocessed_data[0])
        parsed_header = re.sub(r'\n\n$', '', parsed_header)
        parsed_header = re.sub(r'\\[ ]*\n', '', parsed_header)
        parsed_header = re.sub(r'\n', ' ', parsed_header)

        columns = shlex.split(parsed_header)

        return columns

