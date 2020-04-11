import os
import time
import shutil
import random
import math

import keyboard
import termfmt as tfmt

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def clearLine():
    width, height=shutil.get_terminal_size()
    print("\r"+" "*(width)+"\r", end="")

class Question:
    def __init__(self, q="", a=""):
        self.question=q
        self.answer=a
        self.pos=0
        self.autoPos()

    def autoPos(self):
        while (self.pos < len(self.answer)) and not ('0' <= self.answer[self.pos] <= '9') :
            self.pos+=1

    def input(self, c):
        if '0' <= c <= '9':
            if self.pos < len(self.answer) :
                if self.answer[self.pos] == c:
                    self.pos+=1
                    self.autoPos()
                    return 0
                else:
                    return 1

    def getText(self):
        return self.question+self.answer[:self.pos]

    def full(self):
        return self.pos == len(self.answer)

def genAdd(a, b, shuf=False):
    if shuf: a,b=b,a
    return Question(str(a)+"+"+str(b)+"=", str(a+b))

def genProd(a, b, shuf=False):
    if shuf: a,b=b,a
    return Question(str(a)+"*"+str(b)+"=", str(a*b))

def genFrac(a,b):
    return Question(str(a)+"/"+str(b)+"=", str(a//math.gcd(a,b))+"/"+str(b//math.gcd(a,b)))

def genDecomp(n):
    def decomp(n):
        ret=[]
        d=2
        while n!=1:
            if n%d: d+=1
            else:
                n//=d
                ret.append(d)
        return ret

    return Question(str(n)+"=", "*".join(map(str, decomp(n))))


def genListMinMax(func, nMin, nMax, nb):
    return [func(random.randint(nMin, nMax), random.randint(nMin, nMax)) for k in range(nb)]

def genListFrac(nMin, nMax, nb):
    c=random.randint(nMin, nMax)
    return [genFrac(random.randint(nMin, nMax)*c, random.randint(nMin, nMax)*c) for k in range(nb)]

def genListDecomp(nMin, nMax, nb):
    return [genDecomp(random.randint(nMin, nMax)) for k in range(nb)]

def genTable(a):
    t=[genProd(a, k, shuf=True) for k in range(1,10)]
    random.shuffle(t)
    return t

class ModeTest:
    def __init__(self, l=[]):
        self.qList=l
        self.pos=0
        self.startTime=time.time()
        self.lastTime=time.time()
        self.total=0
        self.missed=0

    def input(self, c):
        if c=='h':
            print("Help!")
        elif '0' <= c <= '9':
            if self.pos < len(self.qList):
                self.lastTime=time.time()
                ret=self.qList[self.pos].input(c)
                self.missed+=ret
                if self.qList[self.pos].full():
                    self.total+=1
                    clearLine()
                    print(self.qList[self.pos].getText())
                    self.pos+=1
                self.display(failed=ret)
        elif c=='q':
            print("\nQuit.")
            exit(0)
        if  self.pos == len(self.qList):
            print("")
            print("Stats:")
            print(round((1-self.missed/self.total)*100,1), "%", sep="")
            print(self.getScore())
            exit(0)

    def getScore(self):
        perc=1-self.missed/self.total
        rank=tfmt.fmt("F", tfmt.fgClorRGB(255, 0, 0)+tfmt.bold)
        if perc==1:
            rank=tfmt.fmt("S", tfmt.fgClorRGB(0, 255, 255)+tfmt.bold)
        elif perc>0.95:
            rank=tfmt.fmt("A", tfmt.fgClorRGB(0, 255, 0)+tfmt.bold)
        elif perc>0.85:
            rank=tfmt.fmt("B", tfmt.fgClorRGB(128, 255, 0)+tfmt.bold)
        elif perc>0.75:
            rank=tfmt.fmt("C", tfmt.fgClorRGB(255, 255, 0)+tfmt.bold)
        elif perc>0.50:
            rank=tfmt.fmt("D", tfmt.fgClorRGB(255, 128, 0)+tfmt.bold)
        elif perc>0.00:
            rank=tfmt.fmt("E", tfmt.fgClorRGB(255, 64, 0)+tfmt.bold)

        time=self.lastTime-self.startTime
        timeTxt=str(int(time//60))+"'"+str(round(time%60, 1))+'"'

        return rank+" "+timeTxt

    def display(self, failed=False):
        if self.pos < len(self.qList):
            clearLine()
            print(self.qList[self.pos].getText()+("-" if failed else ""), end="", flush=True)

## UI loop

kb=keyboard.KBHit()

#mode=ModeTest(genListMinMax(genProd, 10, 99, 20))
#mode=ModeTest(genTable(3))
#mode=ModeTest(genListFrac(10, 20, 10))
mode=ModeTest(genListDecomp(10, 50, 10))
newMode=None

lastSize=os.terminal_size([0,0])


while True:
    if lastSize!=shutil.get_terminal_size():
        lastSize=shutil.get_terminal_size()
        mode.display()
    if kb.kbhit():
        n=0
        mode.input(kb.getch())
        if newMode is not None:
            mode=newMode()
            newMode=None

    time.sleep(0.01)
