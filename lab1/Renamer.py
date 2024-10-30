from Parser import Parser
from IR import IR
import sys

class Renamer:
    def __init__(self, parser:Parser) -> None:
        self.IR = parser.IR.queue
        self.SRVR = [-1] * (parser.max + 1)
        self.LU = [-1] * (parser.max + 1)
        self.currLive = 0
        self.maxLive = 0
        self.VR = 0
        self.opCount = parser.opCount
        self.idx = parser.opCount - 1 
        # self.opCodes = [0: load, 1: loadI, 2: store, 3: output, 4: rshift, 5: sub, 6: nop, 7: add, 8: lshift, 9: mult]
        self.opCodes = ["load", "loadI", "store", "output", "rshift", "sub", "nop", "add", "lshift", "mult"]
    
    def set(self, sr, pos):
        if self.SRVR[sr] == -1:
            self.SRVR[sr] = self.VR
            self.VR += 1
            self.currLive += 1
        self.IR[self.idx].set(pos+1, self.SRVR[sr])
        self.IR[self.idx].set(pos+3, self.LU[sr])

    def getmax(self):
        return(self.maxLive)

    def rename(self):
        while(self.idx >= 0):
            #self.maxLive = max(self.maxLive, len(self.SRVR) - self.SRVR.count(-1))

            self.maxLive = max(self.maxLive, self.currLive)
            # handle def
            sr3 = self.IR[self.idx].get(10) #def should be in operand 3
            if sr3 != -1:
                self.set(sr3, 10)
                # kill op
                if self.SRVR[sr3] != -1:
                    self.currLive -= 1
                self.SRVR[sr3] = -1
                self.LU[sr3] = -1
            
            
            #handle use
            sr2 = self.IR[self.idx].get(6)
            sr1 = self.IR[self.idx].get(2)
            op = self.IR[self.idx].get(1)
            if sr2 != -1: #sr2 is used
                self.set(sr1, 2)
                self.set(sr2, 6)
                self.LU[sr1] = self.idx
                self.LU[sr2] = self.idx
            elif op != 3 and op != 1: #only sr1 is used
                if sr1 != -1:
                    self.set(sr1, 2)
                    self.LU[sr1] = self.idx
            self.idx -= 1

    def printILOC(self):
        while self.IR:
            record = self.IR.popleft()
            opCode = record.get(1)
            match opCode:
                case 0:
                    #load: load r1 => r2
                    sys.stdout.write(self.opCodes[opCode] + " r" + str(record.get(3)) + " => r" + str(record.get(11)) + "\n")
                case 1:
                    #loadI: loadI x => r1
                    sys.stdout.write(self.opCodes[opCode] + " " + str(record.get(2)) + " => r" + str(record.get(11)) + "\n")
                case 2:
                    #store: store r1 => r2
                    sys.stdout.write(self.opCodes[opCode] + " r" + str(record.get(3)) + " => r" + str(record.get(7)) + "\n")
                case 3: 
                    #output: output x
                    sys.stdout.write(self.opCodes[opCode] + " " + str(record.get(2)) + "\n")
                case 6:
                    #nop 
                    sys.stdout.write(self.opCodes[opCode] + " \n")
                case _: 
                    #other: op r1, r2 => r3
                    sys.stdout.write(self.opCodes[opCode] + " r" + str(record.get(3)) + ", r" + str(record.get(7)) + " => r" + str(record.get(11)) + "\n")
            
            


                
                