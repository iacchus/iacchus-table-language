#!/usr/bin/env python

import re
import shlex
import pprint

import preprocessor
import processor

FILENAME = "test.itl"

with open(FILENAME, "r") as fd:
    lines = fd.readlines()

preproc = preprocessor.ITMLPreprocessor(text=lines)
proc = processor.ITMLProcessor(preproc)

for item in proc.parsed_list:
    pprint.pprint(item, width=160)
