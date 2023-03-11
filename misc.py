import os
def ttywidth():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns)
