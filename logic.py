class clock:

    def __init__(self,jobl,inputl,tkillpill):
        self.jobl = jobl
        self.inputl = inputl 
        self.tkillpill = tkillpill


    def worktime(self):
        timeset=10
        while timeset > 0 and not self.tkillpill.wait(1):
            pi = str(int(timeset / 60))+':'+str(int(timeset % 60))
            if len(pi) != 5:
                if pi.find(':') < 2:
                    while pi.find(':') != 2:
                        pi = '0'+pi
                while len(pi) != 5:
                    pi = pi[:3]+'0'+pi[3:]
            self.jobl.put([5, 1, str(pi)])
            timeset = timeset - 1
        if not self.tkillpill.wait(0):
            self.breaktime()


    def breaktime(self):
        timeset=5
        while timeset > 0 and not self.tkillpill.wait(1):
            pi = str(int(timeset / 60))+':'+str(int(timeset % 60))
            if len(pi) != 5:
                if pi.find(':') < 2:
                    while pi.find(':') != 2:
                        pi = '0'+pi
                while len(pi) != 5:
                    pi = pi[:3]+'0'+pi[3:]
            self.jobl.put([5, 1, str(pi)])
            timeset = timeset - 1
        if not self.tkillpill.wait(0):
            self.worktime()
