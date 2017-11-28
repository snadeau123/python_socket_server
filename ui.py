import sys
import os

class screenwrite():
    '''
    [1] HEADER = '\033[95m'
    [2] OKBLUE = '\033[94m'
    [3] OKGREEN = '\033[92m'
    [4] WARNING = '\033[93m'
    [5] FAIL = '\033[91m'
    [6] FLASHING = '\033[5m'
    [0] ENDC = '\033[0m'
    '''
    def __init__(self, ymin=0, ymax=0):
        self.x = 0
        self.y = ymin
        self.C = ['\033[0m', '\033[95m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[5m']
        self.ymin = ymin
        self.ymax = ymax
        self.clrlenght = 40

    def printnl(self, s, color=0):
        sys.stdout.write("%s\x1b7\x1b[%d;%df%s\x1b8%s" % (self.C[0], self.y, self.x, " "*self.clrlenght, self.C[0]))
        sys.stdout.write("%s\x1b7\x1b[%d;%df%s\x1b8%s" % (self.C[0], self.y+1, self.x, " "*self.clrlenght, self.C[0]))
        sys.stdout.write("%s\x1b7\x1b[%d;%df%s\x1b8%s" % (self.C[color], self.y, self.x, s, self.C[0]))
        sys.stdout.flush()
        self.y = self.y + 1
        if self.y > self.ymax:
            self.y = self.ymin

    def printStatic(self, s, x, y, color=0):
        sys.stdout.write("%s\x1b7\x1b[%d;%df%s\x1b8%s" % (self.C[color], y, x, s, self.C[0]))
        sys.stdout.flush()

    def clearScreen(self):
        _ = os.system('cls')
        _ = os.system('clear')

