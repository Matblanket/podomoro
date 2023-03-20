import random, curses, time, sys, select, queue, threading
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
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(5,curses.COLOR_WHITE,curses.COLOR_BLACK)
    curses.init_pair(6,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(7,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(8,curses.COLOR_BLACK,curses.COLOR_BLACK)
    stdscr.clear()
    stdscr.refresh()
    while not tkillpill.wait(0):
        try:
            a = joblist.get(block=True,timeout=0.1)
            paintervar(stdscr,a)
        except queue.Empty:
            pass 


def getrandcolor():
    return curses.color_pair(random.randint(1,7))


def paintervar(stdscr,a):
    if a["color"]=="rand":
        stdscr.addstr(a["y"],a["x"],a["t"],getrandcolor())
    elif a["color"]=="norm":
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
