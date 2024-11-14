
import sys
from Parser import Parser
from Renamer import Renamer
from Allocator import Allocator
from AllocatorNS import AllocatorNS
import time
from datetime import datetime
start_tic = datetime.now()
start_time = time.time()


#operations = ["load", "store", "loadI", "add", "sub", "mult", "lshift", "rshift", "output", "nop"]
categories = ["CONSTANT", "REGISTER", "MEMOP", "LOADI", "ARITHOP", "OUTPUT", "NOP", "COMMA", "INTO", "MEMOP", "ENDFILE", "NEXTLINE"]

def main():
    #initialize vars
    argn = len(sys.argv)

    if argn < 2:
        sys.stderr.write("ERROR : Too few command line arguments. \n")
        printHelp()
        return
    
    flag = sys.argv[1]
    fileName = ""

    if flag == "-h": 
        printHelp()
        return
    
    #get flag and file name
    if argn < 3: #too few args, print help msg
        sys.stderr.write("ERROR : Too few command line arguments. \n")
        printHelp()
        return
    elif argn == 3: 
        fileName = sys.argv[2]

    if argn > 3:
        sys.stderr.write("ERROR : Too many command line arguments. \n")
        printHelp()
        return

    try:
        f = open(fileName)
    except:
        sys.stderr.write("ERROR : Could not open file: " + fileName + ". \n")
        sys.exit(1)
    
    # handle different flag cases
    if flag == "-x":
        rename(f)
    elif flag.isdigit():
        k = int(flag)
        if k < 3 or k > 64:
            sys.stderr.write("ERROR : k must be a digit between 3 and 64.  \n")
        else:
            allocate(f, k)
    else:
        sys.stderr.write("ERROR : booo. \n")
        printHelp()
        sys.exit(2)
        
    # self timer :(
    stop_tic  = datetime.now()
    elapsed = stop_tic - start_tic
    elapsed_time = (elapsed.days * 86400 + elapsed.seconds) * 1000 + elapsed.microseconds / 1000.0
    #print(round(elapsed_time/ 1000,4))

    
def rename(file):
    # no need to parse file
    parse = Parser(file)
    error, opCount = parse.parseFile() 
    if error != 0: # Sucess
        sys.stderr.write("ERROR : Error parsing ILOC file. \n")
        sys.stdout.write("ILOC file has parsing errors. \n")
    else: # Failure
        rename = Renamer(parse)
        rename.rename()
        rename.printILOC()
    file.close()

def allocate(file, k):
    parse = Parser(file)
    error, opCount = parse.parseFile() 
    if error != 0: 
        sys.stderr.write("ERROR : Error parsing ILOC file. \n")
        sys.stdout.write("ILOC file has parsing errors. \n")
    else: 
        
        rename = Renamer(parse)
        rename.rename()
        if k < rename.getmax():
            allocate = Allocator(rename, k)
            allocate.allocate()
            #allocate.printILOC()
        else:
            allocate = AllocatorNS(rename, k)
            allocate.allocate()
            allocate.printILOC()


def printHelp():
    sys.stdout.write("COMP 412: Local Register Allocation code check 1: \n Scans, parses, and renames file \n \n python3 412fe.py [-flag] [filename] \n \n" + 
        "Options: \n \t -h \t prints help message \n \t -x \t Renames file. \n" + 
        "Arguments: \n \t filename \t path to the ILOC input file. \n")

if __name__ == '__main__':
    main()
