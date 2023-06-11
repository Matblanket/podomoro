import random, curses, sys, select, queue, threading
from logic import clock
from window import window
import misc

joblist = queue.Queue()
inputlist = queue.Queue()
tkillpill = threading.Event()

state1 = window(0, 10, True, joblist, 270, 5)
statwin = window(5, 10, True, joblist, misc.ttywidth(), 3)
pomodoro = clock(joblist, inputlist, tkillpill, statwin)


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
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
    stdscr.clear()
    stdscr.addstr(3, 60, "  Paused: Q-quit C-Continue    Ongoing: P-Pause Q-quit(withConfirmation)", curses.color_pair(1))
    stdscr.addstr(1, 13, " __   __   __   __         __   __   __  ", curses.color_pair(1))
    stdscr.addstr(2, 13, "|__) /  \ |  \ /  \  |\/| /  \ |__) /  \ ", curses.color_pair(1))
    stdscr.addstr(3, 13, "|    \__/ |__/ \__/  |  | \__/ |  \ \__/ ", curses.color_pair(1))
    stdscr.refresh()
    while not tkillpill.wait(0):
        try:
            a = joblist.get(block=True, timeout=0.1)
            paintervar(stdscr, a)
        except queue.Empty:
            pass


def getrandcolor():
    return curses.color_pair(random.randint(1, 7))


def paintervar(stdscr, a):
    if a["color"] == "rand":
        stdscr.addstr(a["y"], a["x"], a["t"], getrandcolor())
    elif a["color"] == "norm":
        stdscr.addstr(a["y"],  a["x"],  a["t"])
    if a["ref"]:
        stdscr.refresh()


def inhandler():
    while not tkillpill.wait(0):
        try:
            i = inputlist.get(block=True,  timeout=0.1)
            if i == 'p':
                pomodoro.clockstater('p')
            if i == 'q':
                pomodoro.clockstater('q')
        except queue.Empty:
            pass


def logoer():
    while not tkillpill.wait(5):
        rand1 = random.randint(0, 15)
        rand2 = random.randint(0, 100)
        lines = misc.logo[-1].split('\n')
        #for i, j in enumerate(lines):
        #    joblist.put({
        #        'x': 10+rand2,
        #        'y': 20+i+rand1,
        #        't': j,
        #        'ref': False,
        #        'color': "norm"
        #        })
        t = misc.logo[random.randint(0, len(misc.logo)-2)]
        lines = t.split('\n')
        for i, j in enumerate(lines):
            joblist.put({
                'x': 10+rand2,
                'y': 17+i+rand1,
                't': j,
                'ref': True,
                'color': "rand"
            })


def main():
    inproc = threading.Thread(target=inputer)
    inputproc = threading.Thread(target=inhandler)
    cursesproc = threading.Thread(target=starter)
    cursesproc.start()
    inproc.start()
    inputproc.start()
    logicproc = threading.Thread(target=logicer)
    logo = threading.Thread(target=logoer)
    logo.start()
    logicproc.start()
    inproc.join()
    cursesproc.join()
    logicproc.join()
    inproc.join()
    logo.join()


main()
