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

    def __init__(self, columns, data=None):

        self.columns = columns
        self.columnsno = len(columns)

        self.raw_data = data

    @property
    def cellno(self):
        return len(self.cells)

    def new_cell(self):
        pass

    def does_cells_fill_table(self):
        pass

class Cell:

    def __init__(self, pos, contents):

#         if isinstance(contents, tuple):
#             self.paragraphs = str
#
#         elif isinstance(contents, str):
#             self.paragraphs = tuple(str)
#
#         elif isinstance(contents, list):
#             self.paragraphs = tuple(str)

        self.paragraphs = contents
        self.x, self.y = pos

    def __hash__(self):
        # PLEASE CODE ME!!!
        # return (y+1) * (x+1)
        pass

    def __str__(self):
        # PLEASE CODE ME!!
        # Each paragraph + postprocessor-specific formatting
        pass

class ITMLProcessor:


    def __init__(self, preprocessed_data):

        self.data = preprocessed_data

        #columns = self._process_header(preprocessed_data)

        #self.columnsno = len(self.columns)

        columns, data = self.process(preprocessed_data)

        self.table = Table(columns=columns, data=data)


    def process(self, preprocessed_data):

        parsed_data = list()

        header_already = False
        for item in preprocessed_data:

            if not header_already:
                columns = self._process_header(item)
                header_already = True
                continue

            parsed_data = self._process_text(item)

            split_paragraphs = re.split(r'\n\n', parsed_data)  # split paragraphs

            parsed_data.append(tuple(split_paragraphs))

        return (columns, parsed_data)


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

