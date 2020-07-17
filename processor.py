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


    def process(self):

        self.item_list = list(self.preprocessor.groups.values())
        self.parsed_list = list()


        for item in self.item_list:


            new_item = re.sub('\n\n+$', '', item)
            #print("ITEM:", item)
            parsed_paragraphs = re.split(r'\n\n', new_item)  # split paragraphs
            print("PARSED_PARAGRAPHS:", parsed_paragraphs)

            parsed = tuple(self._process_text(x) for x in parsed_paragraphs)

            if parsed:
                self.parsed_list.append(parsed)


    def _process_text(self, text):
        parsed = text
        #parsed = re.sub(r'^[ ]*[#]+[.]*\n', '', parsed)
        parsed = re.sub(r'^[\x20]*[#].*\n$', '', parsed)  # comments on empty
                                                          # lines

        parsed = re.sub(r'[ ]*[#].*\n', '\n', parsed)  # comments after
                                                       # lines with text

        parsed = re.sub(r'\n$', '', parsed)  # removing trailing newlines, as
                                             # paragraph strings are already
                                             # encapsulated in tuples

        parsed = re.sub(r'\\[ ]*\n', '', parsed)  # no ending whitespace
                                                  # after \ and newline

        parsed = re.sub(r'\n', ' ', parsed)  # no ending whitespace
                                             # after \ and newline

        return parsed

