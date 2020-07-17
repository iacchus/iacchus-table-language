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

#pprint.pprint(preproc.groups)
#pprint.pprint(preproc.parsed)
#print(preproc.parsed)
#print(*[item for item in preproc.parsed_list], sep='\n')
#pprint.pprint(preproc.parsed_list)
# print(preproc.groups)
#print(preproc.parsed_list)
#print(preproc.item_list)
# pprint.pprint("\join"*[item for item in preproc.item_list])
#for item in preproc.item_list:
for item in preproc.groups.values():
#for item in proc.parsed_list:
    #pprint.pprint(item, width=170)
    #print(repr(item))
    #print(*[el for el in item], sep="\n‧‧‧‧")
    #print(*[el for el in item], sep="\n‧‧‧‧")
    print(item)
