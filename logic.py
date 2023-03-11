import time, threading
class clock:

    def __init__(self,jobl,inputl,tkillpill,statwin):
        self.jobl = jobl
        self.inputl = inputl 
        self.tkillpill = tkillpill
        self.clockstate = "play"
        self.statwin = statwin
        self.pause = threading.Lock()


    def clockstater(self, val):
        self.clockstate=val
        self.handleclockstate()


    def handleclockstate(self):
        if self.clockstate == 'p':
            with self.pause:
                while True:
                    temp = self.inputl.get()
                    self.statline("hesdlkfjalkfdjl")
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
            self.jobl.put([self.statwin.y, self.statwin.x + j, "_"])
            time.sleep(0.04)
            self.jobl.put([self.statwin.y, self.statwin.x + j, x[j]])
            time.sleep(0.04)
            j=j+1



    def worktime(self):
        timeset=10
        while timeset >= 0 and not self.tkillpill.wait(1):
            pi = '{:02d}:{:02d}'.format(int(timeset / 60), int(timeset % 60))
            self.jobl.put([5, 1, str(pi)])
            with self.pause:
                timeset = timeset - 1
        if not self.tkillpill.wait(0):
            self.breaktime()


    def breaktime(self):
        timeset=5
        while timeset >= 0 and not self.tkillpill.wait(1):
            pi = '{:02d}:{:02d}'.format(int(timeset / 60), int(timeset % 60))
            self.jobl.put([5, 1, str(pi)])
            timeset = timeset - 1
        if not self.tkillpill.wait(0):
            self.worktime()
