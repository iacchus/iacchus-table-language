#!/usr/bin/env python

import re
import shlex


HEADER_TAG = "itbl"


class Table:
    """Implements a Table object, which contains the table's metadata.

    This class implements a Table object, which contains the table metadata
        which will further be usedd by the postprocessor to render the table
        for the preprocessor's specific formatting language (html, markdown,
        unicode etc.)
    The Table object will be created after the processing process and have it's
        `cells` attribute populated with the user input cells so to construct
        the table.

    Args:
        columns (list of str): The list with the names of the columns.
        raw_data (list of tuple of str): List of cells (tuple) containing
            paragraphs (str) returned by the ITMLProcessor `process` method.
            This is used to mount the table's metadata, and is not to be
            misunderstood as the initial input raw data, but rather already
            preprocessed and processed data.

    Attributes:
        columns (list of str): The list with the names of the columns.
        columnsno (int): The number of columns in the table.
        rowsno (int): The number of rows in the table.
        cellsno (int): The number of `Cell`s in the table
        cells (list of Cell): The list of `Cell`s in the table.
        cell_index (int): The index of the new cell which will be added.
        does_cells_fill_table (bool): If the cells fill table.

    """

    def __init__(self, columns, raw_data=None):

        self.columns = columns
        self.columnsno = len(columns)

        self.cells = list()

        for header in self.columns:
            self.new_cell(contents=(header,), header=True)

        if raw_data:
            self.raw_data = raw_data

            for item in raw_data:
                self.new_cell(contents=item)

    def new_cell(self, contents, header=False):

        cell_index = self.cell_index
        columnsno = self.columnsno

        cell_row, cell_column = divmod(cell_index, columnsno)
        pos = tuple([cell_column, cell_row])

        cell = Cell(pos=pos, contents=contents, header=header)

        self.cells.append(cell)

    def get_row(self, row):
        columnsno = self.columnsno
        requested_row = row * columnsno

        row = [self.cells[cell+requested_row] for cell in range(columnsno)]
        return row

    @property
    def rowsno(self):
        return len(self.cells) // self.columnsno

    @property
    def cellsno(self):
        return len(self.cells)

    @property
    def cell_index(self):
        return len(self.cells)

    @property
    def does_cells_fill_table(self):
        does_it_fill = (len(self.cells) % self.columnsno == 0)
        return does_it_fill

    def __repr__(self):

        cols = self.columnsno
        rows = self.rowsno
        cellsno = self.cellsno

        return f"<Table cols: {cols} rows: {rows} cellsno: {cellsno}>"


class Cell:

    def __init__(self, pos, contents, header=False):

        self.x, self.y = pos
        self.paragraphs = contents
        self.role = "body" if not header else "header"

    def __hash__(self):
        return (self.y + 1) * (self.x + 1)

    #def __str__(self):
        #cell_str = str().join(self.paragraphs)
        #
        #return cell_str

    def __iter__(self):
        return iter(self.paragraphs)

    def __repr__(self):
        col = self.x
        row = self.y
        paragraphs = len(self.paragraphs)
        role = self.role
        return (f"<Cell col: {col} row: {row}"
                f" paragraphs: {paragraphs} role {role}>")

class ITMLProcessor:


    def __init__(self, preprocessed_data):

        columns, processed_data = self.process(preprocessed_data)

        self.processed_data = processed_data
        self.table = Table(columns=columns, raw_data=processed_data)


    def process(self, preprocessed_data):

        processed_data = list()

        header_already = False
        for item in preprocessed_data:

            if not header_already:
                columns = self._process_header(item)
                header_already = True
                continue

            parsed_item = self._process_text(item)

            split_paragraphs = re.split(r'\n\n', parsed_item)  # split paragraphs

            processed_data.append(tuple(split_paragraphs))

        return (columns, processed_data)


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

        parsed_header = re.sub(f'^{HEADER_TAG}[ ]+', '', preprocessed_data)
        parsed_header = re.sub(r'\n\n$', '', parsed_header)
        parsed_header = re.sub(r'\\[ ]*\n', '', parsed_header)
        parsed_header = re.sub(r'\n', ' ', parsed_header)

        columns = shlex.split(parsed_header)

        return columns

