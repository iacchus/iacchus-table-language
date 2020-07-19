#!/usr/bin/env python

import re
import shlex

TABLE_ROOT = """\
<table>
  <thead>
{thead}\
  </thead>
  <tbody>
{tbody}\
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


class HtmlITMLPostProcessor:
    """Example Postprocessor which translates a Table object to HTML.

    This is an example implementation of a postprocessor class which translates
    our Table object into an html table inside a full HTML5 file.
    """


    def __init__(self, table):

        self.table = table

        self.process(table)


    def process(self, table):

        header_row = self._process_header_row()
        body_rows = "".join([self._process_body_row(row=x)
                             for x in range(1, self.table.rowsno)])
        html_table = self._process_table(header=header_row, body=body_rows)
        html_full = self._process_html(body=html_table)

        self.output = html_full

        return self.output


    def _process_header_row(self):

        before =  indent("<tr>\n", tr_root_indent)
        after = indent("</tr>\n", tr_root_indent)

        header_row = self.table.get_row(row=0)
        row = "".join([self._process_header_cell(cell) for cell in header_row])

        processed_row = f"{before}{row}{after}"

        return processed_row


    def _process_body_row(self, row):

        before =  indent("<tr>\n", tr_root_indent)
        after = indent("</tr>\n", tr_root_indent)

        header_row = self.table.get_row(row=row)
        row = "".join([self._process_body_cell(cell) for cell in header_row])

        processed_row = f"{before}{row}{after}"

        return processed_row


    def _process_table(self, header, body):
        html_table = TABLE_ROOT.format(thead=header, tbody=body)
        return indent(html_table, table_root_indent)


    def _process_html(self, body):
        html_full = HTML_ROOT.format(body=body)
        return html_full


    def _process_header_cell(self, cell):
        cell_paragraphs = str().join([self._process_paragraphs(x)
                                      for x in cell.paragraphs])
        return indent(f"<th>{cell_paragraphs}</th>\n", td_root_indent)


    def _process_body_cell(self, cell):
        cell_paragraphs = str().join([self._process_paragraphs(x)
                                      for x in cell.paragraphs])
        return indent(f"<td>{cell_paragraphs}</td>\n", td_root_indent)


    def _process_paragraphs(self, paragraph):

        processed_paragraph = f"<p>{paragraph}</p>"

        return processed_paragraph

