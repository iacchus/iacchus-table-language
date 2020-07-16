#!/usr/bin/env python

import re
import shlex
import pprint

import preprocessor

FILENAME = "test.itl"

with open(FILENAME, "r") as fd:
    lines = fd.readlines()

preproc = preprocessor.ITMLPreprocessor(text=lines)

pprint.pprint(preproc.groups)

