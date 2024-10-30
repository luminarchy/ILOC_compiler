from IR import IR
from Record import Record
from Renamer import Renamer
import sys

class AllocatorNS:
    def __init__(self, renamer: Renamer, k):
        self.renamer = renamer
        self.VRnum = self.renamer.VR - 1
        self.PRnum = k
        self.VRPR = [-1]*(self.VRnum+1)
        self.PRVR = [-1]*(self.PRnum)
        self.PRNU = [-1]*(self.PRnum)
        self.PRs = []
        for i in range(0, self.PRnum):
            self.PRs.append(i)
        self.IR = renamer.IR
        # self.record = [line number, opcode, SR1, VR1, PR1, NU1, SR2, VR2, PR2, NU2, SR3, VR3, PR3, NU3]
        # self.opCodes = [0: load, 1: loadI, 2: store, 3: output, 4: rshift, 5: sub, 6: nop, 7: add, 8: lshift, 9: mult]
        
        self.opCodes = ["load", "loadI", "store", "output", "rshift", "sub", "nop", "add", "lshift", "mult"]
    
    def allocate(self):
        for i in range(0, self.renamer.opCount):
            op = self.IR[i]
            vr2 = op.get(7)
            vr1 = op.get(3)
            vr3 = op.get(11) 
            if vr1 != -1: 
                op.set(4, self.VRPR[vr1])
            
                if vr2 != -1:
                    op.set(8, self.VRPR[vr2])

                    if op.get(9) == -1:
                        self.PRVR[op.get(8)] = -1
                        self.VRPR[vr2] = -1
                        self.PRNU[op.get(8)] = -1
                        self.PRs.append(op.get(8))
                

                if op.get(5) == -1:
                    self.PRVR[op.get(4)] = -1
                    self.VRPR[vr1] = -1
                    self.PRNU[op.get(4)] = -1
                    self.PRs.append(op.get(4))
            
            if vr3 != -1:
                op.set(12, self.getPR(vr3, op.get(13), i, False))
                if op.get(13) == -1:
                    self.PRVR[op.get(12)] = -1
                    self.VRPR[vr3] = -1
                    self.PRNU[op.get(12)] = -1
                    self.PRs.append(op.get(12))
            
            

                
                

    def getPR(self, vr, nu, i, is2):
        pr = 0
        pr = self.PRs.pop()
        self.VRPR[vr] = pr
        self.PRVR[pr] = vr
        self.PRNU[pr] = nu
        return(pr)

    def printILOC(self):
        while self.IR:
            record = self.IR.popleft()
            opCode = record.get(1)
            match opCode:
                case 0:
                    #load: load r1 => r2
                    sys.stdout.write(self.opCodes[opCode] + " r" + str(record.get(4)) + " => r" + str(record.get(12)) + "\n")
                case 1:
                    #loadI: loadI x => r1
                    sys.stdout.write(self.opCodes[opCode] + " " + str(record.get(2)) + " => r" + str(record.get(12)) + "\n")
                case 2:
                    #store: store r1 => r2
                    sys.stdout.write(self.opCodes[opCode] + " r" + str(record.get(4)) + " => r" + str(record.get(8)) + "\n")
                case 3: 
                    #output: output x
                    sys.stdout.write(self.opCodes[opCode] + " " + str(record.get(2)) + "\n")
                case 6:
                    #nop 
                    sys.stdout.write(self.opCodes[opCode] + " \n")
                case 10:
                    continue
                case _: 
                    #other: op r1, r2 => r3
                    sys.stdout.write(self.opCodes[opCode] + " r" + str(record.get(4)) + ", r" + str(record.get(8)) + " => r" + str(record.get(12)) + "\n")
        

        