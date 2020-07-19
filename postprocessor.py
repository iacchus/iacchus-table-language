#!/usr/bin/env python

import re
import shlex

TABLE_ROOT = """\
<table>
  <thead>
    <tr>
{thead}
    </tr>
  </thead>
  <tbody>
{tbody}
  </tbody>
</table>\
"""

HTML_ROOT = """
<!doctype html>
<html lang=en>
  <head>
    <meta charset=utf-8 />
    <title>Iacchus' Table Markup Language proof-of-concept</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
{body}
  </body>
</html>
"""

html_root_indent = 0
table_root_indent = 4
tr_root_indent = 4
td_root_indent = 6


def indent(text, size):

    indent = ' ' * size
    parsed = re.sub(r'^', f'{indent}', text, flags=re.MULTILINE)

    return parsed.rstrip(' ')
    #return parsed


class HtmlITMLPostProcessor:


    def __init__(self, table):

        self.table = table

        self.process(table)


    def process(self, table):

        columnsno = table.columnsno
        header_columns = table.columns

        cells = table.cells
        rowsno = table.rowsno


#         thead = str()
#
#         for index, item in enumerate(header_columns):
#
#             if index % columnsno == 0:
#                 thead += indent("<tr>\n", tr_root_indent)
#
#             #paragraphs = self._process_paragraphs(item)
#             thead += self._process_header_cell(item)
#
#             if (index + 1) % columnsno == 0 or cells[index] is cells[-1]:
#                 thead += indent("</tr>\n", tr_root_indent)
#
#         tbody = str()

#         for index, item in enumerate(cells):
#
#             if index % columnsno == 0:
#                 tbody += indent("<tr>\n", tr_root_indent)
#
#             paragraphs = self._process_paragraphs(item)
#             tbody += self._process_body_cell(paragraphs)
#
#             if (index + 1) % columnsno == 0 or cells[index] is cells[-1]:
#                 tbody += indent("</tr>\n", tr_root_indent)

        header_row = self._process_header_row()
        body_rows = [self._process_body_row(row=x)
                     for x in range(1, self.table.rowsno)]
        html_table = self._process_table(header=header_row, body=body_rows)
        html_full = self._process_html(body=html_table)

        self.output = html_full

        return self.output

    def _process_header_row(self):

        before =  indent("<tr>\n", tr_root_indent)
        after = indent("</tr>\n", tr_root_indent)

        header_row = self.table.get_row(row=0)
        row = [self._process_header_cell(cell) for cell in header_row]

        processed_row = f"{before}{row}{after}"

        return processed_row

    def _process_body_row(self, row):

        before =  indent("<tr>\n", tr_root_indent)
        after = indent("</tr>\n", tr_root_indent)

        header_row = self.table.get_row(row=row)
        row = [self._process_header_cell(cell) for cell in header_row]

        processed_row = f"{before}{row}{after}"

        return processed_row

    def _process_table(self, header, body):
        html_table = TABLE_ROOT.format(thead=header, tbody=body)
        return html_table

    def _process_html(self, body):
        html_full = TABLE_ROOT.format(body=body)
        return html_full

    def _process_header_cell(self, cell):
        return indent(f"<th>{cell}</th>\n", td_root_indent)


    def _process_body_cell(self, cell):
        return indent(f"<td>{cell}</td>\n", td_root_indent)

    def _process_paragraphs(self, cell):

        paragraphs = str()
        for paragraph in cell:
            paragraphs += f"<p>{paragraph}</p>"

        return paragraphs

