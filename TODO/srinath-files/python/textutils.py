#!/usr/bin/env python
"""Contains a function to do word-wrapping on text paragraphs."""

import string
import re, random
import operator

def JustifyLine(line, width):
    """Stretch a line to width by filling in spaces at word gaps.

    The gaps are picked randomly one-after-another, before it starts
    over again.

    Author: Christopher Arndt <chris.arndt@web.de
    """
    i = []
    while 1:
        # line not long enough already?
        if len(' '.join(line)) < width:
            if not i:
                # index list is exhausted
                # get list if indices excluding last word
                i = range(max(1, len(line)-1))
                # and shuffle it
                random.shuffle(i)
            # append space to a random word and remove its index
            line[i.pop(0)] += ' '
        else:
            # line has reached specified width or wider
            return ' '.join(line)


def FillParagraphs(text, width=80, justify=0):
    """Split a text into paragraphs and wrap them to width linelength.

    Optionally justify the paragraphs (i.e. stretch lines to fill width).

    Inter-word space is reduced to one space character and paragraphs are
    always separated by two newlines. Indention is currently also lost.

    Author: Christopher Arndt <chris.arndt@web.de
    """
    # split taxt into paragraphs at occurences of two or more newlines
    paragraphs = re.split(r'\n\n+', text)
    for i in range(len(paragraphs)):
        # split paragraphs into a list of words
        words = paragraphs[i].strip().split()
        line = []; new_par = []
        while 1:
           if words:
               if len(' '.join(line + [words[0]])) > width and line:
                   # the line is already long enough -> add it to paragraph
                   if justify:
                       # stretch line to fill width
                       new_par.append(JustifyLine(line, width))
                   else:
                       new_par.append(' '.join(line))
                   line = []
               else:
                   # append next word
                   line.append(words.pop(0))
           else:
               # last line in paragraph
               new_par.append(' '.join(line))
               line = []
               break
        # replace paragraph with formatted version
        paragraphs[i] = '\n'.join(new_par)
    # return paragraphs separated by two newlines
    return '\n\n'.join(paragraphs)

def IndentParagraphs(text, width=80, indent=0, justify=0):
    """Indent a paragraph, i.e:
        . left (and optionally right) justify text to given width
        . add an extra indent if desired.

        This is nothing but a wrapper around FillParagraphs
    """
    retText =  re.sub(r"^|\n", "\g<0>" + " "*indent, \
                  FillParagraphs(text, width, justify))
    retText = re.sub(r"\s+$", '', retText)
    return retText


def OffsetText(text, indent):
    return re.sub("^|\n", "\g<0>" + " "*indent, text)


def FormatTable(tableText, ROW_SPACE=2, COL_SPACE = 3, \
                COL_WIDTH=30, TABLE_WIDTH=80, justify=0):
    """
    FormatTable(tableText [, ROW_SPACE=2, COL_SPACE = 3, COL_WIDTH=30])
        returns string

    Given a 2 dimensional array of text as input, produces a plain text
    formatted string which resembles the table output.

    The optional arguments specify the inter row/column spacing and the
    column width.
    """

    # first find out the max width of the columns
    # maxlengths is a dictionary, but can be accessed exactly like an
    # array because the keys are integers.
    maxlengths = {}      
    for row in tableText:
        lengths = map(len, row)
        for i in range(len(lengths)):
            # Using: dictionary.get(key, default)
            maxlengths[i] = max(lengths[i], maxlengths.get(i, -1))
    
    # Truncate each of the maximum lengths to the maximum allowed.
    for i in range(0, len(maxlengths)):
        maxlengths[i] = min(maxlengths[i], COL_WIDTH)

    if justify:
        formattedTable = []

        for row in tableText:
            formattedTable.append(map(FillParagraphs, row, \
                                          [COL_WIDTH]*len(row)))
    else:
        formattedTable = tableText
    
    retTableText = ""
    for row in formattedTable:
        rowtext = row[0]
        width = maxlengths[0]
        for i in range(1, len(row)):
            rowtext = VertCatString(rowtext, width, " "*COL_SPACE)
            rowtext = VertCatString(rowtext, width + COL_SPACE, row[i])

            width = width + COL_SPACE + maxlengths[i]

        retTableText += string.join(rowtext, "")
        retTableText += "\n"*ROW_SPACE

    return re.sub(r"\n+$", "", retTableText)


def VertCatString(string1, width1, string2):
    """
    VertCatString(string1, width1=None, string2)
        returns string

    Concatenates string1 and string2 vertically. The lines are assumed to
    be "\n" seperated.

    width1 is the width of the string1 column (It is calculated if left out).
    (Width refers to the maximum length of each line of a string)

    NOTE: if width1 is specified < actual width, then bad things happen.
    """
    lines1 = string1.split("\n")
    lines2 = string2.split("\n")

    if width1 is None:
        width1 = -1
        for line in lines1:
            width1 = max(width1, len(line))

    retlines = []
    for i in range(0, max(len(lines1),  len(lines2))):
        if i >= len(lines1):
            lines1.append(" "*width1)
        
        lines1[i] = lines1[i] + " "*(width1 - len(lines1[i]))

        if i >= len(lines2):
            lines2.append("")
        
        retlines.append(lines1[i] + lines2[i])

    return string.join(retlines, "\n")


















def _test(width=78, justify=1):
    """Module test case."""
        
    s ="""
This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. 
This is some text. This is some text. This is some text. 

This is some text. This is some text. This is some text. 
This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. This is some text. 
This is some text. This is some text. 
This is some text.

This is some text. 
This is some text. 
This is some text. This is some text. 
This is some text. This is some text. This is some text. 
"""
    print FillParagraphs(s, width, justify)

if __name__ == '__main__':
    _test(55,0)


# vim:et:sts=4
