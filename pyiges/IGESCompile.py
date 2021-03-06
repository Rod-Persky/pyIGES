#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: IGES.IGESCompile
   :platform: Agnostic, Windows
   :synopsis: Main GUI program

.. requires decimal

.. Created on Fri Mar 29 14:58:02 2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES
"""


import decimal

this_context = decimal.BasicContext
this_context.prec = 8
decimal.setcontext(this_context)


def format_line(data, section):
    """concatinate data chuncks and add section marker and line counter

    :param data: list of values
    :type data: list

    :param section: letter for the corresponding IGES section
    :type section: string

    """
    out = ""

    for i in range(0, len(data)):
        new_data = "{:<72}".format(data[i])
        new_section = "{:7}".format(i + 1)
        out += "\n" + new_data + section + new_section
        #old: out = "{}{}{:<72}{}{:7}".format(out, "\n", data[i], section, i + 1)

    return out


def IGESUnaligned(data, IGESGlobal, section, DirectoryPointer=0):
    """split data into chuncks of correct length for file output
    Step 1, Convert data
    Step 2, Check line length is less then IGESGlobal.linelength
    Step 2a, Add parameter to line
    Step 2b, Add line to LineStore
    Step 4, return LineStore sting
    """

    if section == "P":
        LineLength = IGESGlobal.LineLength - 2
    else:
        LineLength = IGESGlobal.LineLength

    lines = [""]

    if len(data) == 0:
        raise ValueError("Parameter data is 0 length")

    for item in data:
        nline = len(lines) - 1
        itemType = type(item)
        if itemType is str:
            Parameter = "{}H{}".format(len(item), item)
        elif itemType is int:
            Parameter = "{}".format(item)
        elif itemType is float:
            Parameter = "{}".format(decimal.Decimal(item).normalize())
            # Parameter = "{}".format(numpy.around(item, 5))
        elif 'numpy.float64' in str(itemType):
            Parameter = "{}".format(decimal.Decimal(item).normalize())
            # Parameter = "{}".format(numpy.around(item, 5))
        else:
            raise NotImplementedError("Unable to convert type ", str(itemType))

        current_line_length = len(lines[nline])
        # See if we can fit this parameter on the line
        if current_line_length == 0:
            # If we're on the first item for the line
            lines[nline] = Parameter

        elif current_line_length + len(Parameter) + 1 < LineLength:
            # We can fit the Parameter on this line with a trailing comma
            lines[nline] += IGESGlobal.ParameterDelimiterCharacter + Parameter

        elif len(Parameter) < LineLength - (len(Parameter) + 1):
            # We could not fit the Parameter on this line but we can fit the parameter on the next line
            lines[nline] += IGESGlobal.ParameterDelimiterCharacter
            lines.append(Parameter)

        else:
            # Parameter does not in one line so it has to be split into multible lines
            remaining_space = IGESGlobal.LineLength - current_line_length
            lines[nline] += IGESGlobal.ParameterDelimiterCharacter + Parameter[:remaining_space]
            Parameter = Parameter[remaining_space:]
            chunks = len(Parameter)
            lines.extend([Parameter[i:i+IGESGlobal.LineLength] for i in range(0, chunks, IGESGlobal.LineLength)])

    lines[-1] += IGESGlobal.RecordDelimiter

    if section == "P":
        # in the parameter section we need to add a pointer back to the directory on every line
        for i in range(0, len(lines)):
            lines[i] = "{:<{}}{:>7}".format(lines[i], IGESGlobal.LineLength, DirectoryPointer)

    return lines, len(lines)
