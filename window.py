import misc

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


class timewindow:
    def __init__(self, y, x, jobl, type="nrml", width=4):
        self.niam = window(y, x, True, jobl, width*10-1, 8)
        self.type = type
        self.units = []
        self.curunits = [10]*width
        self.jobl = jobl
        for i in range(width):
            self.units.append(window(self.niam.y, self.niam.x+(i*10), False, jobl))

    def displaytime(self, time):
        if self.type == "chrg":
            if int(time)/1500 > 0.75:
                self.chargingletter(self.units[0])
            elif int(time)/1500 > 0.5:
                self.chargingletter(self.units[1])
            elif int(time)/1500 > 0.25:
                self.chargingletter(self.units[2])
            else:
                self.chargingletter(self.units[3])
        else:
            for i, j in enumerate(time):
                if j != str(self.curunits[i]):
                    self.letter(j, self.units[i], True if self.type == "rand" else False)

    def letter(self, i, win, rand=False):
        temp = krys[int(i)]
        for u in krys[int(10)]:
            misc.block(u[0] * 2 + win.y, u[1] * 2 + win.x, self.jobl, clear=True)
        for u in temp:
            misc.block(u[0] * 2 + win.y, u[1] * 2 + win.x, self.jobl, rand)

    def chargingletter(self, win):
        for u in krys[int(10)]:
            misc.block(u[0] * 2 + win.y, u[1] * 2 + win.x, self.jobl, True)


class window:
    def __init__(self, y, x, border, jobl, width=10, height=10):
        self.y = y
        self.x = x
        self.width = width
        if misc.ttywidth() < self.x + self.width:
            self.width = misc.ttywidth()-self.x
        self.height = height
        self.jobl = jobl
        if border:
            self.bordersetup()
            self.y = y+1
            self.x = x+1
            self.width = self.width-2
            self.height = self.height-2

    def winclear(self):
        for i in range(self.height):
            self.jobl.put(misc.getjob(self.y+i, self.x, " "*(self.width)))

    def bordersetup(self):
        self.lborder()
        self.rborder()
        self.botborder()
        self.topborder()

    def topborder(self):
        self.jobl.put(misc.getjob(self.y, self.x, "-"*(self.width)))

    def botborder(self):
        self.jobl.put(misc.getjob(self.y+self.height-1, self.x, "-"*(self.width)))

    def lborder(self):
        for i in range(self.height):
            self.jobl.put(misc.getjob(self.y+i, self.x, "|"))

    def rborder(self):
        for i in range(self.height):
            self.jobl.put(misc.getjob(self.y+i, self.x+self.width-1, "|"))

    def highborder(self):
        for i in range(self.height+2):
            self.jobl.put(misc.getjob(self.y-1+i, self.x-1, "|", rand=True))
            self.jobl.put(misc.getjob(self.y-1+i, self.x+self.width, "|", rand=True))
        self.jobl.put(misc.getjob(self.y-1, self.x-1, "-"*(self.width+2), rand=True))
        self.jobl.put(misc.getjob(self.y+self.height, self.x-1, "-"*(self.width+2), rand=True))
