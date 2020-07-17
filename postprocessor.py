#!/usr/bin/env python

import re
import shlex

# class HtmlITMLPostProcessor(ITMLProcessor):
# 
# 
#     def __init__():
#         pass
# 
#     def process()
# 
table_root = """
<table>
  <thead>
    <tr>
      <th colspan="2">The table header</th>
    </tr>
  </thead>
  <tbody>
{tbody}
  </tbody>
</table>
"""

html_root = """
<!doctype html>
<html lang=en>
  <head>
    <meta charset=utf-8>
    <title>blah</title>
  </head>
  <body>
{body}
  </body>
</html>
"""
class HtmlITMLPostProcessor:


    def __init__(self, processor):

        self.processor = processor

        self.columnsno = self.processor.columnsno
        self.columns = self.processor.columns

        self.cells = self.processor.parsed_list

        self.process()


    def process(self):

        columnsno = self.columnsno

        parsed = str()
        count = 1

        for index, item in enumerate(self.cells):

            if index % columnsno == 0:
                count = 1
                tag = "<tr>\n{}\n"

            elif (index + 1) % columnsno == 0:
                tag = "{}\n</tr>\n"
            else:
                tag = '{}\n'

            parsed += tag.format(self._process_body_cell(item))

        table_parsed = table_root.format(tbody=parsed)
        html_parsed = html_root.format(body=table_parsed)

        self.output = html_parsed

        return self.output


    def _process_header_cell(self):
        return f"<th>{cell}</th>"


    def _process_body_cell(self, cell):
        return f"<td>{cell}</td>"
