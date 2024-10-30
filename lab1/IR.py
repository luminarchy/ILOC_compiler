from collections import deque
from Record import Record
class IR:
    def __init__(self):
        self.opCodes = ["load", "loadI", "store", "output", "rshift", "sub", "nop", "add", "lshift", "mult"]
        self.queue = deque()
    
    def push(self, newRecord):
        self.queue.append(newRecord)
    
    def printRecords(self):
        print("IR format: [line number, opcode, SR1, VR1, PR1, NU1, SR2, VR2, PR2, NU2, SR3, VR3, PR3, NU3]")
        print("opcode numbers: [0: store, 1: loadI, 2: store, 3: output, 4: rshift, 5: sub, 6: nop, 7: add, 8: lshift, 9: mult]")
        while self.queue:
            record = self.queue.popleft()
            record.printList()

            