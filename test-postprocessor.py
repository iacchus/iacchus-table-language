#!/usr/bin/env python

import re
import shlex
import pprint

import preprocessor
import processor
import postprocessor

FILENAME = "test.itl"
OUTPUT_FILENAME = 'test.html'

with open(FILENAME, "r") as fd:
    lines = fd.readlines()

preproc = preprocessor.ITMLPreprocessor(text=lines)
proc = processor.ITMLProcessor(preproc.preprocessed_data)
table = proc.table
postproc = postprocessor.HtmlITMLPostProcessor(table)

print(postproc.output)

with open(OUTPUT_FILENAME, 'w') as output_file:
    output_file.write(postproc.output)
