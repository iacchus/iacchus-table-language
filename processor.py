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


class ITMLProcessor:


    def __init__(self, preprocessor):

        self.preprocessor = preprocessor

        self.process()

        self.columnsno = self.preprocessor.columnsno
        self.columns = self.preprocessor.columns


    def process(self):

        self.item_list = list(self.preprocessor.groups.values())
        self.parsed_list = list()


        for index, item in enumerate(self.item_list):


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
        parsed = re.sub(r'(?<=.)\n(?=.)', r' ', parsed)

        return parsed

