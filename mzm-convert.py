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

programName = "mzm-convert"

def usage():
    stderr.write(programName + " [-z|-b|-c] filename [filename...]\n")

def main():
    if len(argv) < 3:
        usage()
        exit(1)

    outputType = ""

    if ( argv[1] == "-b" ) or ( argv[1] == "--basic" ):
        outputType = "basic"
    elif ( argv[1] == "-z" ) or ( argv[1] == "--z80" ):
        outputType = "z80"
    elif ( argv[1] == "-c" ) or ( argv[1] == "--basicode" ):
        outputType = "basicode"
    else:
        usage()
        exit(1)
        
    # make sure that there are files to parse
    if len(argv) < 3:
        usage()
        exit(1)
    
    # create the MazezamList to hold the mazezams
    
    mazezamList = MazezamList()
    
    # for all the filenames provided on the command-line, open each file, parse
    # it into mazezamList and close it.
    
    for filename in argv[2:]:
        try:
            input = open(filename,'r')
        except:
            stderr.write(programName + ": cannot open input file "+filename+"\n")
            exit(2)
        try:
            mazezamList.readFromMZMLines(input.readlines())
        except MZMParseError, thatError:
            thatError.filename = filename
            stderr.write(programName + ": "+str(thatError)+"\n")
            exit(3)
        input.close()

    if outputType == "basic":
        mazezamList.write2zxbas(stdout)
    elif outputType == "z80":
        mazezamList.write2z80(stdout)
    else:
        mazezamList.write2basicode(stdout)

main()
