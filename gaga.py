import curses, time, sys, select, queue, threading
from logic import clock 
from window import window
import misc 

joblist = queue.Queue()
inputlist = queue.Queue()
tkillpill = threading.Event()

statwin = window(5,10,True,joblist,misc.ttywidth(),3)

pomodoro = clock(joblist,inputlist,tkillpill,statwin)

def inputer():
    while not tkillpill.wait(0):
        r, w, e = select.select([sys.stdin], [], [], 0.1)
        if sys.stdin in r:
            userin = sys.stdin.read(1)
            inputlist.put(userin)


def logicer():
    pomodoro.worktime()


def starter():
    curses.wrapper(painter)


def painter(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    while not tkillpill.wait(0):
        try:
            a = joblist.get(block=True,timeout=0.1)
            paintervar(stdscr,a)
        except queue.Empty:
            pass 

def paintervar(stdscr,a):
    stdscr.addstr(a["y"],a["x"],a["t"])
    if a["ref"]:
        stdscr.refresh()

def inhandler():
    while not tkillpill.wait(0):
        try:
            i = inputlist.get(block=True, timeout=0.1)
            if i == 'p':
                pomodoro.clockstater('p')
            if i == 'q':
                tkillpill.set()
        except queue .Empty:
            pass


def main():
    inproc = threading.Thread(target=inputer)
    inputproc= threading.Thread(target=inhandler)
    cursesproc = threading.Thread(target=starter)
    cursesproc.start()
    inproc.start()
    inputproc.start()
    logicproc = threading.Thread(target=logicer)
    logicproc.start()
    inproc.join()
    cursesproc.join()
    logicproc.join()
    inproc.join()


main()
