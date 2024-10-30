class Record:
    def __init__(self) -> None:
        #self.record = [line number, opcode, SR1, VR1, PR1, NU1, SR2, VR2, PR2, NU2, SR3, VR3, PR3, NU3]
        self.record = [-1 for i in range(14)]
    
    def set(self, idx, content):
        self.record[idx] = content
    
    def get(self, idx):
        return self.record[idx]
    
    def printList(self):
        print(*self.record, sep = ', ')