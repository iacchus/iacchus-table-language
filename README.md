This project aims to develop a simple, concise and robust language for making
bi-dimensional data tables

# ITML Language Specification

(this is pre-alpha and is currently in development)

Contents:

- introduction: why and how?
- specification
  - the header
  - the body
  - comments
  - formatting
  - versioning

## Introduction: Why, and how?

We are trying to follow the steps of simple languages like markdown and toml,
which simply do their job well done and nothing else.

Is is simple and legible, and writing them goes in the natural process of
writing text in a text editor, and not in drawing tables having to adjust the
table columns when more text is added. In ITML you simple state the format
and state the cols in the first line, and the each subsequent line or lines, if
we use indentation in an entry, or paragraphs if we use space between indented
text of the same cell, will be the contents of a table cell.

## The Header

The first line of the stream contains the string `itbl` and the names of all
columns of the table, using shell like escape, like this:

```
itbl "Column 1" Column\ 2 Column3
```

There will be three columns in this description. "Column 1" "Column 2" and
"Column". The backslash in 'Column 2' is used to escape espaces, so they don't get splitted
but are partes of the same argument. As seen in 'Column 1', the quotation marks
also can be used to escape spaces inside a column name, very like in a command
line shell.

We are currently thinking on means of allowing extend the header in multiple
lines so that we dont need to limit the column names to be declared in only one
line.

## The Body

After the header, each new line with indentation 0 (not indented) will be
treated as table cell.

If the line needs to be broken in various lines, the line continuation will be
syntatically representing by adding indentation to the broken lines, this is,
by adding spaces before the caracters in the new broken lines. The amount of
spaces if not actually enforced, but it is enforced that multiple indented
lines have the same amount of spaces than the indented line before. Example:

```
itbl COLUMN1 COLUMN2 COLUMN3  # then we have 3 columns

This is the first column of the table, and we will break this line and indent,
    it, so that we dont break our formatting rule of not trespassing the number
    of 79 characters per line. See how the multiple lines indented have the
    same indentation: this is an enforced rule. If the number of spaces differ
    from one to another, it is a bug and the itml file should not pass the
    preprocessing phase.
This is a cell in the second column. Now we are going to show that we do not
  need to have the same indentation as before, but we SHOULD always use the
  same indentation. This is not enforced for the time being, but we should 
  attain to some standards for formatting our itml files. We are thinking if we
  should use 2 or 4 spaces. Very probably we will stick with 4 spaces, as
  any modern text editor is capable of shifting a tab for 4 spaces and then
  automatically keep the indentation on the following lines, and 4 spaces
  improve readability of the itbl source.
And this is a cell in the third column.
```

## Comments

Comments inside the `itbl` file are added with the character `#`. This can be
made in empty lines or after text.

Comment lines and inline comments are removed from the data at preprocessing
time, so they don't get to the itml processor.

## Formatting

One of the caracteristics which we have in mind as we develop the ITML-lang is
readability from the very `itbl` source.

SO, we will try to attain to best practices in writing the source so that we
respect some rules, even these rules not being enforced by the ITML
specification.

Some of these rules we are borrowing from the Python language, which uses
indentation syntatically as well and have being proven to be good through the
time and use.

### Max character width

The ITBL format lines should have the maximum of 79 characters per line.
Additional characters should be broken to the next line and indented.

The ITBL format indentation should not use TAB, and should be indented with
2 or 4 spaces, concisely. After pre-alpha we will see which case is better and
change this documentation with the urging to use 2 or 4 spaces, which be
better.

The lines representing the cells of one row in the ITML format should have an
empty line after the number of columns. Simple like this:

```
itbl COLUMN1 COLUMN2 COLUMN3  # then we have 3 columns

This text is the first column. 
This text is the second column. 
This text is the third column.

After the newline, this is the first column of the second row.
And this is the second column of the second row.
And this is the last(3rd) column of the second row.
```

As seen above, after the three columns of the first row we add a blank line to
improve readability of the source. The newline has no syntatic meaning, as we
are all consenting adults here, but it should be used to improve readability.

The inline comments in ITML format, this is, the comments made after a line of
text should have too espaces before the `#` character.

This project aims to develop a simple, concise and robust language for making
bi-dimensional data tables

[https://github.com.iacchus/iacchus-table-language](https://github.com.iacchus/iacchus-table-language)

## Our proof-of-concept implementation in python

We are currently in pre alpha.

**preprocessor** - parses input data and check for error in language

**procesor** - formats preprocessed data in turns of creating a sanitized
data base to be used by

**postprocessor** - which transform processed data in other media, like html,
markdown, unicode etc. Each of these formats should have it's own postprocess,
depending on with type of output we desire.

