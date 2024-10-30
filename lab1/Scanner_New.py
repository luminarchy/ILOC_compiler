import sys

class Scanner:
    def __init__(self, file):
        self.file = file
        self.lineCount = 0 # counts de lines
        self.char = '' # next char
        self.lineBuffer = "\n" # line buffer??!! stores line currently being read
        self.charCount = 0 # current char pos in line
        self.isEOF = False # is EOF????
        self.lexeme = ""
        self.state = -1 

        # self.catSet = [0: "CONSTANT", 1: "REGISTER", 2: "MEMOP", 3: "LOADI", 4: "ARITHOP", 5: "OUTPUT", 6: "NOP", 7: "COMMA", 8: "INTO", 9: "MEMOP", 10: "EOF", 11: "EOL"]
        # self.sa = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # set of possible end states 

    # get a new line to buffer from the file, 
    def nextLine(self): 
        self.lineCount += 1
        try: 
            self.lineBuffer = (self.file).readline()
        except:
            sys.stderr.write("ERROR: file could not be read. Please try again :(.")
            self.lineBuffer = "\n"
            self.isEOF = True
        else: 
            if self.lineBuffer == "":
                self.isEOF = True # readline() outputs empty string for EOF
            self.lineBuffer += "\n" # ensure each line ends with \n
            self.charCount = 0 
    
    # read the next character in the line buffer
    def nextChar(self):
        try: 
            self.char = self.lineBuffer[self.charCount]
        except IndexError:
            self.char = '\n' # make sure line ends with \n
        else:
            self.charCount += 1 
    
    # direct-coded scanner, reduce the amount of rollback and state checks. 
    def scanNext(self):
        if self.isEOF: # check EOF first
            return 10, "", self.lineCount # EOF
        
        # reset state and lexeme 
        self.state = -1 # default is se = -1
        self.lexeme = ""
        self.nextChar()

        while self.char.isspace() and self.char != '\n':
            self.nextChar() # skip spaces

        # check line
        if self.char == '\n':
            self.nextLine()
            return 11, "\\n", self.lineCount - 1
        
        if self.char == '/' and self.lineBuffer[self.charCount+1] == '/':
            self.nextLine()
            return 11, "\\n", self.lineCount - 1
        
        try:
            ch = ord(self.char) # in case, char is not an ASCII char?
        except:
            self.nextLine() 
            return -1, self.lexeme, self.lineCount - 1

        self.lexeme += self.char 
        match ch: # convert char to ASCII int, for easier processing of constants and registers
            case 10: #'\n'
                self.nextLine() 
                return 11, "\\n", self.lineCount - 1 # EOL
            
            case 44: # ',' COMMA
                return 7, ",", self.lineCount  #COMMA

            case 47: # '/' 
                self.nextChar()
                if self.char == '/': # comment
                    self.nextLine()
                    return 11, "\\n", self.lineCount - 1
            
            case x if 47 < x < 58: # '0' - '9' CONSTANT
                self.constantHandler()
                self.state = 0 # CONSTANT

            case 61: # '='
                self.nextChar() 
                self.lexeme += self.char
                if self.char == '>': # '=>'
                    self.state = 8 # INTO
            
            case 97: # 'a'
                self.nextChar() 
                self.lexeme += self.char
                if self.char == 'd': # 'ad'
                    self.nextChar() 
                    self.lexeme += self.char
                    if self.char == 'd': # "add"
                        self.state = 4 # ARITHOP
            
            case 108: # 'l'
                self.lHander() # either load, loadI, or lshift

            case 109: # 'm'
                self.nextChar() 
                self.lexeme += self.char
                if self.char == 'u': # 'mu'
                    self.nextChar() 
                    self.lexeme += self.char
                    if self.char == 'l': # "mul"
                        self.nextChar() 
                        self.lexeme += self.char
                        if self.char == 't': # "mult"
                            self.state = 4 # ARITHOP
                        
            case 110: # 'n'
                self.nextChar() 
                self.lexeme += self.char
                if self.char == 'o': # 'no'
                    self.nextChar() 
                    self.lexeme += self.char
                    if self.char == 'p': # "nop"
                        self.state = 6 # NOP

            case 111: # 'o'
                self.nextChar() 
                self.lexeme += self.char
                if self.char == 'u': # 'ou'
                    self.nextChar() 
                    self.lexeme += self.char
                    if self.char == 't': # "out"
                        self.nextChar() 
                        self.lexeme += self.char
                        if self.char == 'p': # "outp"
                            self.nextChar() 
                            self.lexeme += self.char
                            if self.char == 'u': # 'outpu'
                                self.nextChar() 
                                self.lexeme += self.char
                                if self.char == 't': # "output"
                                    self.state = 5 # OUTPUT
            case 114: # 'r'
                self.rHandler() # either register or rshift

            case 115: # 's'
                self.sHandler() # either sub or store
            case _: # char is not a proper starting char. 
                self.state = -1 # error state

        if self.state == -1: # check if state is error
            self.nextLine() # skip to next line, and return error state
            return -1, self.lexeme, self.lineCount - 1
        
        return self.state , self.lexeme, self.lineCount # return state
    
    def constantHandler(self): 
        # handles the number portion of both registers and constants
        self.nextChar() # peek at the next char, but dont add onto lexeme yet. 
        if(47 < ord(self.char) < 58):
            self.lexeme += self.char
            self.constantHandler() 
        else: # rollback
            self.charCount -= 1 
    
    def lHander(self):
        # handler for strings starting with l: load, loadI, lshift
        self.nextChar()
        self.lexeme += self.char
        match self.char:
            case 'o': # 'lo'
                #either load or loadI
                self.nextChar()
                self.lexeme += self.char
                if self.char == 'a': # 'loa'
                    self.nextChar()
                    self.lexeme += self.char
                    if self.char == 'd': # 'load'
                        self.nextChar() # peek at next char
                        if self.char == 'I': # 'loadI'
                            self.lexeme += self.char
                            self.state = 3 # LOADI
                        else: # rollback
                            self.charCount -= 1
                            self.state = 9 # MEMOP (load)
            case 's': # "ls"
                # must be lshift
                self.shiftHandler() 
            case _: 
                self.state = -1 # error
            
    def rHandler(self):
        self.nextChar()
        self.lexeme += self.char
        match ord(self.char):
            case x if 47 < x < 58:
                self.state = 1 # REGISTER
                self.constantHandler()
            case 115: # "rs_" 
                self.shiftHandler() # rshift
            case _:
                self.state = -1 # error

    def shiftHandler(self):
        self.nextChar()
        self.lexeme += self.char
        if self.char == "h": # "_sh"
            self.nextChar()
            self.lexeme += self.char
            if self.char == "i": # "_shi"
                self.nextChar()
                self.lexeme += self.char
                if self.char == "f": # "_shif"
                    self.nextChar()
                    self.lexeme += self.char
                    if self.char == "t": # " _shift"
                        self.state = 4 # ARITHOP 
    
    def sHandler(self):
        self.nextChar()
        self.lexeme += self.char
        match self.char:
            case 't': # 'st'
                self.nextChar()
                self.lexeme += self.char
                if self.char == "o": # 'sto'
                    self.nextChar()
                    self.lexeme += self.char
                    if self.char == "r": # 'stor'
                        self.nextChar()
                        self.lexeme += self.char
                        if self.char == "e": # 'store'
                            self.state = 2 # MEMOP (store)
            case 'u': # 'su'
                self.nextChar()
                self.lexeme += self.char
                if self.char == "b": # 'sub'
                    self.state = 4 # ARITHOP

            case _:
                self.state = -1 # error

                

        
            
            
        


            
            
            
            
