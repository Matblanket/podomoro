import os, misc, curses, random 
def ttywidth():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns)

def getjob(y=0, x=0, t="%", ref=True,rand=False):
        return {
            "x": x,
            "y": y,
            "t": t,
            "ref": ref,
            "color": "rand" if rand else "norm"
        }

def block(y, x, joblist, rand=False, clear=False ):
    if clear:
        joblist.put(misc.getjob(y + 0, x, " " * 3))
        joblist.put(misc.getjob(y + 1, x, " " * 3))
    else:
        if rand:
            joblist.put(misc.getjob(y + 0, x, chr(9608) * 3,rand=True))
            joblist.put(misc.getjob(y + 1, x, chr(9608) * 3,rand=True))
        else:
            joblist.put(misc.getjob(y + 0, x, chr(9608) * 3))
            joblist.put(misc.getjob(y + 1, x, chr(9608) * 3))

