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

            parsed = self._process_text(item)

            #print("ITEM:", item)
            #print("PARSED_PARAGRAPHS:", parsed_paragraphs)

            # parsed = tuple(self._process_text(x) for x in parsed_paragraphs)

            split_paragraphs = re.split(r'\n\n', parsed)  # split paragraphs

            self.parsed_list.append(tuple(split_paragraphs))


    def _process_text(self, text):

        parsed = text

        parsed = re.sub(r'[\n]*\n$', '', parsed)



        #parsed = re.sub(r'\n', '', parsed)  # removing trailing newlines, as
                                             # paragraph strings are already
                                             # encapsulated in tuples

        parsed = re.sub(r'\\[\x20]*\n', '', parsed)  # no ending whitespace
                                                     # after \ and newline

        #parsed = re.sub(r'(?!\n[\n]+|\n$)\n', '_', parsed,flags=re.MULTILINE)
        #parsed = re.sub(r'^$', '_')
        #parsed = re.sub(r'(.)\n(.)', r'\1 \2', parsed)  # join continuing
        parsed = re.sub(r'(?<=.)\n(?=.)', r' ', parsed)  # join continuing
                                                         # (indented) lines
                                                         # with a space


        #parsed = re.sub(r'\n', ' ', parsed)  # no ending whitespace
                                             # after \ and newline

        return parsed #if parsed else None  # empty string. Maybe we should let
                                           # preprocessor do it's job in 
                                           # processing comments

