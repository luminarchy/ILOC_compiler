
import sys
from Scanner_New import Scanner
from Parser import Parser
import time
from datetime import datetime, date
start_tic = datetime.now()
start_time = time.time()


#operations = ["load", "store", "loadI", "add", "sub", "mult", "lshift", "rshift", "output", "nop"]
categories = ["CONSTANT", "REGISTER", "MEMOP", "LOADI", "ARITHOP", "OUTPUT", "NOP", "COMMA", "INTO", "MEMOP", "ENDFILE", "NEXTLINE"]

def main():
    #initialize vars
    argn = len(sys.argv)
    flag = flag = sys.argv[1]
    fileName = ""

    if flag == "-h": 
        printHelp()
        return
    
    #get flag and file name
    if argn == 2: #no flag given, assume flag is -p
        flag = "-p"
        fileName = sys.argv[1]
    elif argn == 3: 
        fileName = sys.argv[2]

    if argn > 3:
        sys.stderr.write("ERROR : Too many command line arguments. \n")
        printHelp()

    try:
        f = open(fileName)
    except:
        sys.stderr.write("ERROR : Could not open file: " + fileName + ". \n")
        sys.exit(1)
    
    # handle different flag cases
    if flag == "-s":
        sHandler(f, fileName)
    elif flag == "-p":
        pHandler(f)
    elif flag == "-r":
        rHandler(f)
    else:
        sys.stderr.write("ERROR : wrong command line arguments. \n")
        printHelp()
        sys.exit(2)
        
    # self timer :(
    stop_tic  = datetime.now()
    elapsed = stop_tic - start_tic
    elapsed_time = (elapsed.days * 86400 + elapsed.seconds) * 1000 + elapsed.microseconds / 1000.0
    print(round(elapsed_time/ 1000,4))

    
def sHandler(file, fileName):
    # no need to parse file
    scan = Scanner(file)
    cat, lexeme, line = 0, "", 0
    while cat != 10: # while not EOF
        cat, lexeme, line = scan.scanNext() 
        if cat == -1:
            # lexical error
            sys.stderr.write("ERROR " + str(line) + " : lexical error " + lexeme + " in file: " + fileName + "\n")
        else:
            # print tokens
            sys.stdout.write("Line " + str(line) + " : < " + categories[cat] + " , \"" + lexeme + "\" > \n")
    file.close()

def pHandler(file):
    parse = Parser(file)
    error, opCount = parse.parseFile() 
    if error == 0: # Sucess
        sys.stdout.write("Parse suceeded. Processed " + str(opCount) + " operations. \n")
    else: # Failure
        sys.stdout.write("Parse found errors. \n")
    file.close()

def rHandler(file):
    parse = Parser(file) 
    error, opCount = parse.parseFile()
    if error == 0:
        sys.stdout.write("Parse suceeded. Processed " + str(opCount) + " operations. \n")
    else:
        sys.stdout.write("Parse found " + str(error) + " errors, processed " + str(opCount) + " operations. \n")
    parse.printIR() # Print IR
    file.close()

def printHelp():
    sys.stdout.write("COMP 412: ILOC front end lab 1: \n Scans and parses files \n \n python3 412fe.py [-flag] [filename] \n \n" + 
        "Options: \n \t -h prints help message \n \t -s \t scans and prints the line number and <token, lexeme> for each word. \n" + 
        "\t -p (default) \t scans and parses, then either reports sucess or the number of errors found. \n" + 
        "\t -r \t scans and parses, then prints an readable intermediate representation of the input file \n \n" + 
        "Arguments: \n \t filename \t path to the ILOC input file. \n")

if __name__ == '__main__':
    main()
