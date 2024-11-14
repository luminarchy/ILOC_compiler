from Scanner_New import Scanner
from IR import IR
from Record import Record
import sys

class Parser:
    def __init__(self, file) -> None:
        self.scanner = Scanner(file)
        self.IR = IR() # Initialize IR
        self.errorCount = 0
        self.opCount = 0
        self.max = 0
        # self.record = [line number, opcode, SR1, VR1, PR1, NU1, SR2, VR2, PR2, NU2, SR3, VR3, PR3, NU3]
        # self.catSet = ["CONSTANT", "REGISTER", "MEMOP", "LOADI", "ARITHOP", "OUTPUT", "NOP", "COMMA", "INTO", "MEMOP"]
        # opCode indices
        # self.opCodes = [0: load, 1: loadI, 2: store, 3: output, 4: rshift, 5: sub, 6: nop, 7: add, 8: lshift, 9: mult]
        self.record = Record() # Initialize record

    
    def nextWord(self):
        word = self.scanner.scanNext()
        return(word)

    def parseFile(self):
        # begin parsing line
        word = self.nextWord()
        while(word[0] == 11):
                # remove unncessary \n 
                word = self.nextWord()
        while(word[0] != 10): # while not EOF
            self.record.set(0, int(word[2])) # set line number in record
            match word[0]:
                case 2: # store
                    self.record.set(1, 2)
                    self.finishStore()
                case 3:
                    self.record.set(1, 1)
                    self.finishLoadI()
                case 4:
                    # inelegant way of parsing arithops w/o having an index call or making a overly large delta table
                    # ill fix this one day, but it works so lulz
                    self.record.set(1, ord(word[1][0]) % 10)
                    self.finishArithop()
                case 5:
                    self.record.set(1, 3) 
                    self.finishOutput() 
                case 6:
                    self.record.set(1, 6)
                    self.finishNop()
                case 9: # load
                    self.record.set(1, 0)
                    self.finishMemop()
                case _: # Error
                    sys.stderr.write("ERROR " + str(word[2]) + " : invalid operation syntax. \n")
                    self.error(word)
                    self.errorCount += 1 
            word = self.nextWord()
            while(word[0] == 11):
                # remove unnecessary \n
                word = self.nextWord()
        return self.errorCount, self.opCount

    def printIR(self): # Print IR
        self.IR.printRecords() 

    def finishMemop(self): 
        word = self.nextWord()
        if word[0] != 1: 
            sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in MEMOP operation, expected a register. \n")
            self.error(word)
            self.errorCount += 1
        else:
            self.record.set(2, int(word[1][1:]))
            self.max = max(self.max, self.record.get(2))
            self.finishInto()  
    
    def finishStore(self):
        word = self.nextWord()
        if word[0] != 1: 
            sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in MEMOP operation, expected a register. \n")
            self.error(word)
            self.errorCount += 1
        else:
            self.record.set(2, int(word[1][1:]))
            self.max = max(self.max, self.record.get(2))
            word = self.nextWord()
            if word[0] != 8:
                sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in operation, expected an INTO. \n")
                self.error(word)
                self.errorCount += 1
            else:
                word = self.nextWord()
                if word[0] != 1:
                    sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in operation, expected a register. \n")
                    self.error(word)
                    self.errorCount += 1
                else:
                    self.record.set(6, int(word[1][1:]))
                    self.max = max(self.max, self.record.get(6))
                    word = self.nextWord()
                    if word[0] != 11:
                        sys.stderr.write("ERROR " + str(word[2]) + " : too many arguments \n")
                        self.error(word)
                        self.errorCount += 1
                    else:
                        self.IR.push(self.record)
                        self.record = Record()
                        self.opCount += 1

    
    def finishLoadI(self): 
        word = self.nextWord()
        if word[0] != 0:
            sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in LOADI operation, expected a constant \n")
            self.error(word)
            self.errorCount += 1
        else:
            self.record.set(2, int(word[1]))
            self.finishInto()

    def finishArithop(self): 
        word = self.nextWord()
        if word[0] != 1:
            sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in ARITHOP operation, expected a register. \n")
            self.error(word)
            self.errorCount += 1
        else:
            self.record.set(2, int(word[1][1:]))
            self.max = max(self.max, self.record.get(2))
            word = self.nextWord()
            if word[0] != 7:
                sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in ARITHOP operation, expected a COMMA. \n")
                self.error(word)
                self.errorCount += 1
            else:
                word = self.nextWord()
                if word[0] != 1:
                    sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in ARITHOP operation, expected a register. \n")
                    self.error(word)
                    self.errorCount += 1
                else:
                    self.record.set(6, int(word[1][1:]))
                    self.max = max(self.max, self.record.get(6))
                    self.finishInto()

    def finishInto(self): # finish INTO REGISTER format
        word = self.nextWord()
        if word[0] != 8:
            sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in operation, expected an INTO. \n")
            self.error(word)
            self.errorCount += 1
        else:
            word = self.nextWord()
            if word[0] != 1:
                sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in operation, expected a register. \n")
                self.error(word)
                self.errorCount += 1
            else:
                self.record.set(10, int(word[1][1:]))
                self.max = max(self.max, self.record.get(10))
                word = self.nextWord()
                if word[0] != 11:
                    sys.stderr.write("ERROR " + str(word[2]) + " : too many arguments \n")
                    self.error(word)
                    self.errorCount += 1
                else:
                    self.IR.push(self.record)
                    self.record = Record()
                    self.opCount += 1
                
    def finishOutput(self):
        word = self.nextWord()
        if word[0] != 0:
            sys.stderr.write("ERROR " + str(word[2]) + " : invalid syntax in output operation, expected a constant. \n")
            self.error(word)
            self.errorCount += 1
        else:
            self.record.set(2, int(word[1]))
            word = self.nextWord()
            if word[0] != 11:
                sys.stderr.write("ERROR " + str(word[2]) + " : output operation has too many arguments. \n")
                self.error(word)
                self.errorCount += 1
            else:
                self.IR.push(self.record)
                self.record = Record()
                self.opCount += 1

                
    
    def finishNop(self):
        word = self.nextWord()
        if word[0] != 11:
            sys.stderr.write("ERROR " + str(word[2]) + " : nop operation has too many arguments. \n")
            self.error(word)
            self.errorCount += 1
        else:
            self.IR.push(self.record) # push record into IR
            self.record = Record()  # new record
            self.opCount += 1
    
    def error(self, word): # skip to next line if there is an error. EOL can either be -1 (lexical error) or 11 (\n)
        next_word = word[0] 
        if next_word != 11 and next_word != -1: # make sure current error word isn't already an EOL
            while next_word != 11 and next_word != -1: # loop until EOL is found
                next_word = self.nextWord()[0] 
        self.record = Record() # new blank record
    
    


