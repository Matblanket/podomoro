import time, threading, misc, subprocess
from window import timewindow, window
timeset = 16
timesetq = [timeset/4, timeset/2, 3*timeset/4, timeset]
jobtemplate = {
        "y": 0,
        "x": 0,
        "t": "%",
        "ref": True
        }


class clock:
    def __init__(self, jobl, inputl, tkillpill, statwin):
        self.jobl = jobl
        self.inputl = inputl
        self.tkillpill = tkillpill
        self.clockstate = "play"
        self.statwin = statwin
        self.pause = threading.Lock()
        self.displaytime = timewindow(9, 10, self.jobl, "nrml", 4)
        self.displaybintime = timewindow(40, 10, self.jobl, "nrml", 11)
        self.displaytimebr = timewindow(self.displaytime.niam.y-1,
                                        self.displaytime.niam.x+40,
                                        self.jobl, "chrg", 4)
        self.displaydectime = timewindow(40, 140, self.jobl, "nrml", 4)

    def clockstater(self, val):
        self.clockstate = val
        self.handleclockstate()

    def handleclockstate(self):
        if self.clockstate == 'p':
            with self.pause:
                self.statline("Podomoro paused. Come back whenever ^_^")
                while True:
                    temp = self.inputl.get()
                    if temp == 'c':
                        self.clockstate = "play"
                        break
                    if temp == 'q':
                        self.statline("Ending session. Good work today ^_^")
                        self.tkillpill.set()
                        break
        if self.clockstate == 'q':
            with self.pause:
                self.statline("Are you sure? (y/n)")
                while True:
                    temp = self.inputl.get()
                    if temp == 'y':
                        self.statline("Ending session. Good work today ^_^")
                        self.tkillpill.set()
                        break
                    if temp == 'n':
                        self.statline("Aight continuing with current session.")
                        break

    def statline(self, x=""):
        self.jobl.put(misc.getjob(self.statwin.y, self.statwin.x,
                                  "+" * self.statwin.width))
        time.sleep(0.2)
        self.jobl.put(misc.getjob(self.statwin.y, self.statwin.x,
                                  "-" * self.statwin.width))
        time.sleep(0.2)
        self.statwin.winclear()
        time.sleep(0.02)
        x = " > " + x
        j = 0
        while j < len(x):
            self.jobl.put(misc.getjob(self.statwin.y, self.statwin.x + j, "_"))
            time.sleep(0.04)
            self.jobl.put(misc.getjob(self.statwin.y, self.statwin.x + j, x[j]))
            time.sleep(0.04)
            j=j+1

    def worktime(self):
        self.displaytimebr.type = "chrg"
        timeset = 1500
        while timeset > 0 and not self.tkillpill.wait(1):
            pi = '{:02d}:{:02d}'.format(int(timeset / 60), int(timeset % 60))
            binv = misc.decimalToBinary(timeset)
            for i in range(misc.ttyheight()):
                self.jobl.put(misc.getjob(i, 0, str(pi)))
            self.displaybintime.displaytime(binv)
            self.displaytime.displaytime(pi.replace(':', ''))
            self.displaytimebr.displaytime(pi.replace(':', ''))
            self.displaydectime.displaytime(str(timeset))
            with self.pause:
                timeset = timeset - 1
        if not self.tkillpill.wait(0):
            self.breaktime()

    def breaktime(self):
        self.displaytimebr.type = "rand"
        timeset=300
        while timeset > 0 and not self.tkillpill.wait(1):
            pi = '{:02d}:{:02d}'.format(int(timeset / 60), int(timeset % 60))
            for i in range(misc.ttyheight()):
                self.jobl.put(misc.getjob(i, 1, str(pi)))
            timeset = timeset - 1
            self.displaytimebr.displaytime(pi.replace(':', ''))
        if not self.tkillpill.wait(0):
            self.worktime()
