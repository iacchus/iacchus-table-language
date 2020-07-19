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
    """Processes a raw ITML input and returns data to be processed.

    The preprocessor sanitizes input and modules it to be processed by the
    ITML processor.

    Attributes:
        lines (list): The raw, not preprocessed, input data divided by lines.
        preprocessed_data (list): A list of sanitized data ready to be passed
            to the ITMLProcessor to be processed.
    """

    def __init__(self, text=None, filename=None):

        if filename:
            with open(filename, "r") as fd:
                text = fd.read()

        if text:
            self.load_text(text)


    def process(self, text):
        """Sanitizes the raw ITML input.

        Args:
            text (str): a raw input in ITML format.

        Returns:
            list: A `list` ready to be passed to the ITML processor.
            """

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
        groups = list()
        groupno = 0

        for lineno, line in enumerate(lines):

            match = re.match(r'^(?P<blanks>[ ]*)(?P<text>[\w\W]*)', line)
            matches = match.groupdict()

            line_indent = len(matches['blanks'])
            line_contents = matches['text']
            blank_line = re.match('^[\n]$', line_contents)

            # line is a comment; continue `for` loop ignoring current line:
            if re.match(r'^[\x20]*[#].*\n$', line_contents):
                continue

            # remove inline comments
            parsed_line = re.sub(r'[\x20]*[#].*\n', '\n', line_contents)

            if blank_line:

                # blank line. was the previous `indent` greater than indent 0?
                # so let's keep it, because a newline between two indented
                # blocks of text is used to separate paragraphs of the same
                # cell:
                if indent > 0:
                    groups[groupno] += parsed_line

                # it is only a blank line; skip it:
                else:
                    continue

            # line has text and it is not indented; start a new group
            elif line_indent == 0:
                groups.append(parsed_line)  # start a new group
                groupno = len(groups) - 1  # set current group index
                indent = 0  # new indent

            # line has text and is indented. was the previous line
            # `indent` == 0 and this is an indented continuation of it?
            # or this is a continuation of the previous already indented line
            # with the same indentation?
            elif indent == 0 or line_indent == indent:
                indent = line_indent  # new indent
                groups[groupno] += parsed_line

            # line is indented but it's indentation is not equal the previous
            # indented line(s)
            else:
                raise(f"Invalid indentation at line {lineno+1}.")

        return groups


    def _check_header(self, line):
        """Checks if the data stream header line is in a valid itml format."""

        header_match = re.match(f'^{HEADER_TAG}[ ]+', line)

        return header_match

    def loads(self, text):
        """Loas an ITML stream from a string.

        Args:
            text (str): the string in ITML format.
        """

        if isinstance(text, str):
            self.load_text(text)
        else:
            raise('loads() expect a str() as `text` parameter.')

        return True

    def load(self, filename):
        """Loads an ITML stream from a file.

        Args:
            text (str): the name of the file containing the text in ITML
                format.
        """

        with open(filename, "r") as fd:
            text = fd.read()

        self.load_text(text)

        return True

    def load_text(self, text):

        self.text = text
        self.preprocessed_data = self.process(text)


