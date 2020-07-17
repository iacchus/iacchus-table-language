#!/usr/bin/env python

import re
import shlex

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

        cells = self.cells

        parsed = str()
        count = 1

        for index, item in enumerate(cells):

            if index % columnsno == 0:
                count = 1
                parsed += indent("<tr>\n", tr_root_indent)
                #tag = indent("<tr>\n{}", tr_root_indent)
                #tag = indent("<tr>\n{}",tr_root_indent)

            parsed += self._process_body_cell(item)

            if (index + 1) % columnsno == 0 or cells[index] is cells[-1]:
                #tag = indent("{}</tr>\n", tr_root_indent)
                parsed += indent("</tr>\n", tr_root_indent)
                #tag = indent("{}</tr>\n", tr_root_indent)
            #else:
            #    tag = '{}'

            #parsed += tag.format(self._process_body_cell(item))

        table_parsed = indent(table_root.format(tbody=parsed),
                              table_root_indent)
        html_parsed = html_root.format(body=table_parsed)

        self.output = html_parsed

        return self.output


    def _process_header_cell(self, cell):
        return indent(f"<th>{cell}</th>\n", td_root_indent)


    def _process_body_cell(self, cell):
        return indent(f"<td>{cell}</td>\n", td_root_indent)
