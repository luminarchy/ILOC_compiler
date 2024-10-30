from IR import IR
from Record import Record
from Renamer import Renamer
from collections import deque
import sys

class Allocator:
    def __init__(self, renamer: Renamer, k):
        self.renamer = renamer
        self.VRnum = self.renamer.VR - 1
        self.PRnum = k - 1
        self.VRPR = [-1]*(self.VRnum+1)
        self.PRVR = [-1]*(self.PRnum)
        self.PRNU = [-1]*(self.PRnum)
        self.PRs = deque()
        for i in range(0, self.PRnum):
            self.PRs.append(i)
        self.spilloc = [-1]*(self.VRnum+1)
        self.clean = [-1]*(self.VRnum+1)
        self.spillines = 0
        self.loadIs = [-1]*(self.VRnum+1)
        self.loadI = deque()
        self.IR = renamer.IR
        self.record = Record()
        # self.record = [ine number, opcode, SR1, VR1, PR1, NU1, SR2, VR2, PR2, NU2, SR3, VR3, PR3, NU3]
        # self.opCodes = [0: load, 1: loadI, 2: store, 3: output, 4: rshift, 5: sub, 6: nop, 7: add, 8: lshift, 9: mult]
        
    
    def allocate(self):
        while self.IR:
            
            # op = self.IR[i + self.spillines]
            self.record = self.IR.popleft()
            vr2 = self.record.get(7)
            vr1 = self.record.get(3)
            vr3 = self.record.get(11) 
            if vr1 != -1: 
                if self.VRPR[vr1] == -1:
                    self.record.set(4, self.getPR(vr1, self.record.get(5), False))
                    self.restore(vr1, self.record.get(4))
                else: 
                    self.record.set(4, self.VRPR[vr1])
            
                if vr2 != -1:
                    if self.VRPR[vr2] == -1:
                        self.record.set(8, self.getPR(vr2, self.record.get(9), True))
                        self.restore(vr2, self.record.get(8))
                    else: 
                        self.record.set(8, self.VRPR[vr2])

                    if self.record.get(9) == -1:
                        self.PRVR[self.record.get(8)] = -1
                        self.VRPR[vr2] = -1
                        self.PRNU[self.record.get(8)] = -1
                        self.PRs.append(self.record.get(8))
                

                if self.record.get(5) == -1 and vr1 != vr2:
                    self.PRVR[self.record.get(4)] = -1
                    self.VRPR[vr1] = -1
                    self.PRNU[self.record.get(4)] = -1
                    self.PRs.append(self.record.get(4))
            
            if vr3 != -1:
                if self.record.get(1) == 1:
                    self.loadIs[vr3] = self.record.get(2)
                    self.loadI.append(vr3)
                    self.record.set(1, 10)
                else: 
                    self.record.set(12, self.getPR(vr3, self.record.get(13), False))
                    self.loadIs[vr3] = -1
            self.printILOC()
            
            

                
                

    def getPR(self, vr, nu, is2):
        pr = 0
        r4 = self.record.get(4)
        if self.PRs:
            pr = self.PRs.pop()
        else: # spill
            # op = self.IR[i + self.spillines]
            op1 = int(self.PRNU[r4])
            if not is2:
                self.PRNU[r4] = -1
            maxL = [i for i in [self.VRPR[j] for j in range(len(self.loadIs)) if self.loadIs[j] != -1] if self.PRNU[i] != -1]
            #maxL = max(self.PRNU[i] for i in [self.VRPR[j] for j in self.loadI])
            if maxL:
                pr = self.PRNU.index(maxL)
            else:
                pr = self.PRNU.index(max(self.PRNU))
            
            # if is2:
            #     pr = -1
            #     maxnu = 0 
            #     for idx in range(len(self.PRNU)):
            #         if idx != op.get(4):
            #             maxn = max(self.PRNU[idx], maxnu)
            #             pr = idx
            # else:
            #     pr = self.PRNU.index(max(self.PRNU))         
            self.PRNU[self.record.get(4)] = op1
            self.spill(pr)

            
        self.VRPR[vr] = pr
        self.PRVR[pr] = vr
        self.PRNU[pr] = nu
        return pr
    
    def spill(self, pr):

        #curr = i + self.spillines
        vr = self.PRVR[pr]
        if self.loadIs[vr] == -1 and self.clean[vr] == -1: # not loadI

            self.spilloc[vr] = 32768 + 4 * self.spillines
            sys.stdout.write("loadI " + str(self.spilloc[vr]) + " => r" + str(self.PRnum) + "\n")
            # loadI = Record()
            # loadI.set(1, 1)
            # loadI.set(2, 32768 + 4 * self.spillines)
            # loadI.set(12, self.PRnum)

            sys.stdout.write("store r" + str(pr) + " => r" + str(self.PRnum) + "\n")
            # store = Record()
            # store.set(1, 2)
            # store.set(4, pr)
            # store.set(8, self.PRnum)

            # self.IR.insert(curr, loadI)
            # self.IR.insert(curr + 1, store)
            self.spillines += 2
        else:
            self.spilloc[vr] = self.loadIs[vr]

        self.VRPR[vr] = -1
        return pr
        
    def restore(self, vr, pr):
        #curr = i + self.spillines
        if self.loadIs[vr] != -1:

            sys.stdout.write("loadI " + str(self.loadIs[vr]) + " => r" + str(pr) + "\n")
            # loadI = Record()
            # loadI.set(1, 1)
            # loadI.set(2, self.loadIs[vr])
            # loadI.set(12, pr)

            # self.IR.insert(curr, loadI)
            #self.spillines += 1
        elif self.clean[vr] != -1:

            sys.stdout.write("loadI " + str(self.clean[vr]) + " => r" + str(self.PRnum) + "\n")
            # loadI = Record()
            # loadI.set(1, 1)
            # loadI.set(2, self.spilloc[vr])
            # loadI.set(12, self.PRnum)

            sys.stdout.write("load r" + str(self.PRnum) + " => r" + str(pr) + "\n")
            # load = Record()
            # load.set(1, 0)
            # load.set(4, self.PRnum)
            # load.set(12, pr)
            
            # self.IR.insert(curr, loadI)
            # self.IR.insert(curr + 1, load)
            #self.spillines += 2
        elif self.spilloc[vr] != -1:

            sys.stdout.write("loadI " + str(self.spilloc[vr]) + " => r" + str(self.PRnum) + "\n")
            # loadI = Record()
            # loadI.set(1, 1)
            # loadI.set(2, self.spilloc[vr])
            # loadI.set(12, self.PRnum)

            sys.stdout.write("load r" + str(self.PRnum) + " => r" + str(pr) + "\n")
            # load = Record()
            # load.set(1, 0)
            # load.set(4, self.PRnum)
            # load.set(12, pr)
            
            # self.IR.insert(curr, loadI)
            # self.IR.insert(curr + 1, load)
            self.clean[vr] = self.spilloc[vr]
           # self.spillines += 2
         

    def printILOC(self):
        self.record = self.record
        opCodes = ["load", "loadI", "store", "output", "rshift", "sub", "nop", "add", "lshift", "mult"]
        #while self.IR:
        opCode = self.record.get(1)
        match opCode:
            case 0:
                #load: load r1 => r2
                sys.stdout.write(opCodes[opCode] + " r" + str(self.record.get(4)) + " => r" + str(self.record.get(12)) + "\n")
            case 1:
                #loadI: loadI x => r1
                sys.stdout.write(opCodes[opCode] + " " + str(self.record.get(2)) + " => r" + str(self.record.get(12)) + "\n")
            case 2:
                #store: store r1 => r2
                sys.stdout.write(opCodes[opCode] + " r" + str(self.record.get(4)) + " => r" + str(self.record.get(8)) + "\n")
            case 3: 
                #output: output x
                sys.stdout.write(opCodes[opCode] + " " + str(self.record.get(2)) + "\n")
            case 6:
                #nop 
                sys.stdout.write(opCodes[opCode] + " \n")
            case 10:
                pass
            case _: 
                #other: op r1, r2 => r3
                sys.stdout.write(opCodes[opCode] + " r" + str(self.record.get(4)) + ", r" + str(self.record.get(8)) + " => r" + str(self.record.get(12)) + "\n")
    

        