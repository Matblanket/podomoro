import curses, sys, select, queue, threading
from logic import clock 

joblist = queue.Queue()
inputlist = queue.Queue()
tkillpill = threading.Event()
pomodoro = clock(joblist,inputlist,tkillpill)

def inputer():
    while not tkillpill.wait(0):
        r, w, e = select.select([sys.stdin], [], [], 0.1)
        if sys.stdin in r:
            userin = sys.stdin.read(1)
            if userin=='q':
                tkillpill.set()
            inputlist.put(userin)


def logicer():
    pomodoro.worktime()


def starter():
    curses.wrapper(painter)


def painter(stdscr):
    stdscr.clear()
    stdscr.refresh()
    while not tkillpill.wait(0):
        try:
            a = joblist.get(block=True,timeout=0.1)
            stdscr.addstr(a[0],a[1],a[2])
            stdscr.refresh()
        except queue.Empty:
            pass 


def main():
    inproc = threading.Thread(target=inputer)
    cursesproc = threading.Thread(target=starter)
    cursesproc.start()
    inproc.start()
    logicproc = threading.Thread(target=logicer)
    logicproc.start()
    inproc.join()
    cursesproc.join()
    logicproc.join()


main()
