import misc
class window:
    
    def __init__(self,y,x,border,jobl,width=10,height=10):
        self.y = y
        self.x = x
        self.width = width
        if misc.ttywidth()<self.x+self.width:
            self.width = misc.ttywidth()-self.x
        self.height = height
        self.jobl = jobl
        if border:
            self.bordersetup()
            self.y = y+1
            self.x = x+1
            self.width = width-2
            self.height = height-2

    def bordersetup(self):
        self.botborder()
        self.topborder()
        self.lborder()
        self.rborder()


    def topborder(self):
        self.jobl.put(misc.getjob(self.y,self.x,"-"*(self.width)))


    def botborder(self):
        self.jobl.put(misc.getjob(self.y+self.height-1,self.x,"-"*(self.width)))


    def lborder(self):
        for i in range(self.height):
            self.jobl.put(misc.getjob(self.y+i,self.x,"|"))


    def rborder(self):
        for i in range(self.height):
            self.jobl.put(misc.getjob(self.y+i,self.x+self.width-1,"|"))
