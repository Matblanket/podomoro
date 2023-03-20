import time, threading, misc
from window import window
timeset=16
timesetq=[timeset/4,timeset/2,3*timeset/4,timeset]
krys = {
    1: [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
    2: [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    0: [(0, 0), (0, 2), (1, 0), (0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    3: [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2), (2, 0), (2, 1)],
    4: [(0, 0), (1, 0), (0, 2), (1, 1), (1, 2), (2, 2)],
    5: [(0, 2), (0, 1), (1, 1), (2, 0), (2, 1)],
    6: [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2), (2, 1), (2, 2)],
    7: [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    8: [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
    9: [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (2, 2)],
    10: [(0, 0), (1, 0), (2, 0),
         (0, 1), (1, 1), (2, 1),
         (0, 2), (1, 2), (2, 2),]
}

jobtemplate = {
        "y":0,
        "x":0,
        "t":"%",
        "ref":True
        }

class clock:

    def __init__(self,jobl,inputl,tkillpill,statwin):
        self.jobl = jobl
        self.inputl = inputl 
        self.tkillpill = tkillpill
        self.clockstate = "play"
        self.statwin = statwin
        self.pause = threading.Lock()
        self.displaytime = window(9,10,True,self.jobl,39,8)
        self.minute= window(self.displaytime.y,self.displaytime.x,False,self.jobl)
        self.minute2= window(self.displaytime.y,self.displaytime.x+10,False,self.jobl)
        self.second= window(self.displaytime.y,self.displaytime.x+20,False,self.jobl)
        self.second2= window(self.displaytime.y,self.displaytime.x+30,False,self.jobl)
        self.displaytimebr = window(self.displaytime.y-1,self.displaytime.x+40,True,self.jobl,39,8)
        self.minutebr= window(self.displaytimebr.y,self.displaytimebr.x,False,self.jobl)
        self.minute2br= window(self.displaytimebr.y,self.displaytimebr.x+10,False,self.jobl)
        self.secondbr= window(self.displaytimebr.y,self.displaytimebr.x+20,False,self.jobl)
        self.second2br= window(self.displaytimebr.y,self.displaytimebr.x+30,False,self.jobl)



    def clockstater(self, val):
        self.clockstate=val
        self.handleclockstate()


    def letter(self,i,win,rand=False):
        temp = krys[int(i)]
        for u in krys[int(10)]:
            misc.block(u[0] * 2 + win.y, u[1] * 2 + win.x, self.jobl,clear=True)
        for u in temp:
            misc.block(u[0] * 2 + win.y, u[1] * 2 + win.x, self.jobl,rand)


    def displayletters(self,time):
        self.letter(time[0],self.minute)
        self.letter(time[1],self.minute2)
        self.letter(time[3],self.second)
        self.letter(time[4],self.second2)

    def displaylettersbr(self,time):
        self.letter(time[0],self.minutebr,True)
        self.letter(time[1],self.minute2br,True)
        self.letter(time[3],self.secondbr,True)
        self.letter(time[4],self.second2br,True)

    def chargingletter(self,win):
        for u in krys[int(10)]:
            misc.block(u[0] * 2 + win.y, u[1] * 2 + win.x, self.jobl,True)


    def handleclockstate(self):
        if self.clockstate == 'p':
            with self.pause:
                self.statline("hesdlkfjalkfdjl")
                while True:
                    temp = self.inputl.get()
                    if temp == 'c':
                        self.clockstate = "play"
                        break
                    if temp == 'q':
                        self.tkillpill.set()
                        break
            

    def statline(self, x = ""):
        x = " > " + x
        j = 0
        while j<len(x):
            self.jobl.put(misc.getjob(self.statwin.y, self.statwin.x + j, "_"))
            time.sleep(0.04)
            self.jobl.put(misc.getjob(self.statwin.y, self.statwin.x + j, x[j]))
            time.sleep(0.04)
            j=j+1


    def updatecharge(self,time):
        try:
            if time==0:
                self.chargingletter(self.second2br)
                self.chargingletter(self.secondbr)
                self.chargingletter(self.minute2br)
                self.chargingletter(self.minutebr)
            else:
                t=timesetq.index(time)
                if t==3:
                    self.chargingletter(self.minutebr)
                elif t==2:
                    self.chargingletter(self.minute2br)
                    self.chargingletter(self.minutebr)
                elif t==1:
                    self.chargingletter(self.secondbr)
                    self.chargingletter(self.minute2br)
                    self.chargingletter(self.minutebr)
                elif t==0:
                    self.chargingletter(self.second2br)
                    self.chargingletter(self.secondbr)
                    self.chargingletter(self.minute2br)
                    self.chargingletter(self.minutebr)
        except ValueError:
            pass


    def worktime(self):
        timeset=16
        while timeset > 0 and not self.tkillpill.wait(1):
            pi = '{:02d}:{:02d}'.format(int(timeset / 60), int(timeset % 60))
            self.jobl.put(misc.getjob(5, 1, str(pi)))
            self.displayletters(pi)
            self.updatecharge(timeset)
            with self.pause:
                timeset = timeset - 1
        self.displaytimebr.winclear()
        time.sleep(0.2)
        self.updatecharge(timeset)
        time.sleep(0.3)
        self.displaytimebr.winclear()
        time.sleep(0.2)
        self.updatecharge(timeset)
        time.sleep(0.3)
        self.displaytimebr.winclear()
        if not self.tkillpill.wait(0):
            self.breaktime()


    def breaktime(self):
        timeset=5
        while timeset > 0 and not self.tkillpill.wait(1):
            pi = '{:02d}:{:02d}'.format(int(timeset / 60), int(timeset % 60))
            self.jobl.put(misc.getjob(5, 1, str(pi)))
            timeset = timeset - 1
            self.displaylettersbr(pi)
        self.displaytimebr.winclear()
        time.sleep(0.2)
        self.updatecharge(timeset)
        time.sleep(0.3)
        self.displaytimebr.winclear()
        time.sleep(0.2)
        self.updatecharge(timeset)
        time.sleep(0.3)
        self.displaytimebr.winclear()
        if not self.tkillpill.wait(0):
            self.worktime()
