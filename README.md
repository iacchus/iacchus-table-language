# iacchus-table-language

This project aims to develop a simple, concise and robust language for making
bi-dimensional data tables

[https://github.com.iacchus/iacchus-table-language](https://github.com.iacchus/iacchus-table-language)

## Pre alpha design

We are currently in pre alpha.

**preprocessor** - parses input data and check for error in language

**procesor** - formats preprocessed data in turns of creating a sanitized
data base to be used by

**postprocessor** - which transform processed data in other media, like html,
markdown, unicode etc. Each of these formats should have it's own postprocess,
depending on with type of output we desire.

## Language specification

For now we are still giving it touches, but the main specification is in
[brazilian portuguese] test.itb file at the root of this repository.
