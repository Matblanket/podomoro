import os, misc
def ttywidth():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns)

def getjob(y=0, x=0, t="%", ref=True):
    return {
        "x": x,
        "y": y,
        "t": t,
        "ref": ref
    }

def block(y, x, joblist, clear=False):
    if clear:
        joblist.put(misc.getjob(y + 0, x, " " * 3))
        joblist.put(misc.getjob(y + 1, x, " " * 3))
    else:
        joblist.put(misc.getjob(y + 0, x, chr(9608) * 3))
        joblist.put(misc.getjob(y + 1, x, chr(9608) * 3))
