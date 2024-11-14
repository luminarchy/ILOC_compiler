import sys

class Scanner:
    def __init__(self, file):
        self.file = file
        self.lineCount = 0 # counts de lines
        self.char = '' # next char
        self.lineBuffer = "\n" # line buffer??!! stores line currently being read
        self.charCount = 0 # current char pos in line
        self.isEOF = False # is EOF????

        # the valid character alphabet, indices map each character to its corresponding column in the delta table
        self.charSet = [',', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'd', 'e', 'f', 'h', 'i', 'l', 'm', 'n', 'o', 
                        'p', 'r', 's', 't', 'u', 'I', '=', '>']
        
        # Set of operation categories, indices correspond to indices in delta table - 1
        # self.catSet = [0: "CONSTANT", 1: "REGISTER", 2: "MEMOP", 3: "LOADI", 4: "ARITHOP", 5: "OUTPUT", 6: "NOP", 7: "COMMA", 8: "INTO", 9: "MEMOP", 10: "EOF", 11: "EOL"]
        
        # initialize delta table, slight one-time overhead when Scanner object gets created. should've used numpy im lazy loooolololol
        # delta[j] is the possible finite states. 
        self.delta = [[-1 for i in range(30)] for j in range(37)] 
        # delta[0] = the stating state
        self.delta[0] = [8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, -1, -1, -1, -1, -1, -1, 13, 16, 19, 21, -1, 26, 31, -1, -1, -1, 33, -1] 
        # delta[1-10] are the accepting states, each a different token category
        self.delta[1][1:11] = [1] * 10 # numbers <3 
        self.delta[2][1:11] = [2] * 10 # registers <3
        # self.delta[3] = "MEMOP"
        # self.delta[4] = "LOADI"
        # self.delta[5] = "ARITHOP"
        # self.delta[6] = "OUTPUT"
        # self.delta[7] = "NOP"
        # self.delta[8] = "COMMA" 
        # self.delta[9] = "INTO" 
        self.delta[10][27] = 4 # "loadI", also "MEMOP"
        self.delta[11][13] = 12 # "ad"
        self.delta[12][13] = 5 # "add"
        self.delta[13][21] = 14 # "lo"
        self.delta[13][24] = 27 # "ls"
        self.delta[14][11] = 15 # "loa"
        self.delta[15][13] = 10 # "load"
        self.delta[16][26] = 17 # "mu"
        self.delta[17][18] = 18 # "mul"
        self.delta[18][25] = 5 # "mult"
        self.delta[19][21] = 20 # "no"
        self.delta[20][22] = 7 # "nop"
        self.delta[21][26] = 22 # "ou"
        self.delta[22][25] = 23 # "out"
        self.delta[23][22] = 24 # "outp"
        self.delta[24][26] = 25 # "outpu"
        self.delta[25][25] = 6 # "output"
        self.delta[26][1:11] = [2]*10 # "r[0-9]" go to registers
        self.delta[26][24] = 27 # "rs"
        self.delta[27][16] = 28 # "_sh"
        self.delta[28][17] = 29 # "_shi"
        self.delta[29][15] = 30 # "_shif"
        self.delta[30][25] = 5 # "_shift"
        self.delta[31][26] = 32 # "su"
        self.delta[31][25] = 34 # "st"
        self.delta[32][12] = 5 # "sub"
        self.delta[33][29] = 9 # "=>"
        self.delta[34][21] = 35 # "sto"
        self.delta[35][23] = 36 # "stor"
        self.delta[36][14] = 3 # "store"
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
    

    def scanNext(self):
        if self.isEOF: # check EOF first
            return 10, "", self.lineCount 
        
        # this part is from the textbook dab dab dab dab dab
        state = 0
        lexeme = ""
        stack = 0
        count = 0
        self.nextChar()

        # remove whitespace
        while self.char.isspace() and self.char != '\n':
            self.nextChar()

        self.charCount -= 1

        # check EOL
        if self.char == '\n':
            self.nextLine()
            return 11, "\\n", self.lineCount - 1 
        
        # check comment
        if self.char == '/' and self.lineBuffer[self.charCount+1] == '/':
            self.nextLine()
            return 11, "\\n", self.lineCount - 1

        # se = -1
        while state != -1: 
            self.nextChar() 
            lexeme += self.char
            if state < 11 and state > 0: # range of acceptable states
                stack = state # add most recept acceptable state to stack
                count = 0 # reset count 
            count += 1 # count steps from last acceptable state

            try:
                state = self.delta[state][self.charSet.index(self.char)] 
            except:
                state = -1 # if char is not in charSet, then it will throw an error, so state is se
        if stack == 0: 
            # if "bad" is still in stack, then acceptable end state is not reached, no need to continue
            self.nextLine()
            return -1, lexeme, self.lineCount-1

        # rollback
        state = stack
        lexeme = lexeme[:-(count)]
        self.charCount -= count
        
        return (state-1), lexeme, self.lineCount
        
            
            
        


            
            
            
            
