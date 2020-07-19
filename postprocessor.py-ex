#!/usr/bin/env python

import re
import shlex

table_root = """\
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

html_root = """
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


    def __init__(self, processor):

        self.processor = processor

        self.columnsno = self.processor.columnsno
        self.columns = self.processor.columns

        self.cells = self.processor.parsed_list

        self.process()


    def process(self):

        columnsno = self.columnsno
        header_columns = self.columns

        cells = self.cells


        thead = str()

        for index, item in enumerate(header_columns):

            if index % columnsno == 0:
                thead += indent("<tr>\n", tr_root_indent)

            #paragraphs = self._process_paragraphs(item)
            thead += self._process_header_cell(item)

            if (index + 1) % columnsno == 0 or cells[index] is cells[-1]:
                thead += indent("</tr>\n", tr_root_indent)

        tbody = str()

        for index, item in enumerate(cells):

            if index % columnsno == 0:
                tbody += indent("<tr>\n", tr_root_indent)

            paragraphs = self._process_paragraphs(item)
            tbody += self._process_body_cell(paragraphs)

            if (index + 1) % columnsno == 0 or cells[index] is cells[-1]:
                tbody += indent("</tr>\n", tr_root_indent)

        table_parsed = indent(table_root.format(thead=thead.strip('\n'),
                                                tbody=tbody.strip('\n')),
                              table_root_indent)
        html_parsed = html_root.format(body=table_parsed)

        self.output = html_parsed

        return self.output


    def _process_header_cell(self, cell):
        return indent(f"<th>{cell}</th>\n", td_root_indent)


    def _process_body_cell(self, cell):
        return indent(f"<td>{cell}</td>\n", td_root_indent)

    def _process_paragraphs(self, cell):

        paragraphs = str()
        for paragraph in cell:
            paragraphs += f"<p>{paragraph}</p>"

        return paragraphs

