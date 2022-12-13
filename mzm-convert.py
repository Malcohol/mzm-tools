#!/usr/bin/python
#
# mzm-convert - parses MazezaM .mzm files and writes the mazezams in ZXBasic,
#              Z80 asm or BASICODE.
#
# Copyright (C) 2002,2009,2020 Malcolm Tyrrell
# malcolm.r.tyrrell@gmail.com
#
# This code may be used and distributed under the terms of the GNU General
# Public Licence v3.0 or later.

from MazezaM import MazezamList, MZMParseError
from sys import argv, stderr, stdout, exit
from argparse import ArgumentParser, FileType

programName = "mzm-convert"

def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-z", "--z80", action="store_true")
    group.add_argument("-b", "--basic", action="store_true")
    group.add_argument("-c", "--basicode", action="store_true")
    parser.add_argument("files", nargs="+", type=FileType("r"))
    parser.add_argument("-o", "--output", action="store")
    parsedArgs = parser.parse_args()
    
    # create the MazezamList to hold the mazezams
    
    mazezamList = MazezamList()

    # for all the filenames provided on the command-line, parse
    # it into mazezamList and close it.
    
    for input in parsedArgs.files:
        try:
            mazezamList.readFromMZMLines(input.readlines())
        except MZMParseError as thatError:
            thatError.filename = input.name
            stderr.write(programName + ": "+str(thatError)+"\n")
            exit(3)
        input.close()

    output = stdout
    if parsedArgs.output:
        output = open(parsedArgs.output, "w")

    if parsedArgs.basic:
        mazezamList.write2zxbas(output)
    elif parsedArgs.z80:
        mazezamList.write2z80(output)
    else:
        mazezamList.write2basicode(output)

main()
