import curses
import time

prevpi3 = 0
prevpi1 = 0
prevpi0 = 0
sec1 = 0
sec2 = 0
min1 = 0
min2 = 0


def waitforme(stdscr):
    while True:
        if stdscr.getch() == ord('c'):
            break


def startit(stdscr):
    j = 1500
    global prevpi3
    global prevpi1
    global prevpi0
    while j > 0:
        stdscr.nodelay(True)
        pi = str(int(j / 60))+':'+str(int(j % 60))
        if len(pi) != 5:
            if pi.find(':') < 2:
                while pi.find(':') != 2:
                    pi = '0'+pi
            while len(pi) != 5:
                pi = pi[:3]+'0'+pi[3:]
        stdscr.addstr(5, 0, str(pi))
        stdscr.refresh()
        highlight(stdscr, 4+1, int(pi[4]))
        if prevpi3 != pi[3]:
            highlight(stdscr, 3+1, int(pi[3]))
        prevpi3 = pi[3]
        if prevpi1 != pi[1]:
            highlight(stdscr, 1+1, int(pi[1]))
        prevpi1 = pi[1]
        if prevpi0 != pi[0]:
            highlight(stdscr, 0+1, int(pi[0]))
        prevpi0 = pi[0]
        x = stdscr.getch()
        if x == ord('p'):
            waitforme(stdscr)
        elif x == ord('q'):
            break
        j = j - 1
        time.sleep(1)


def highlight(stdscr, unit, val):
    stdscr.addstr(6+val, unit, chr(9608), curses.color_pair(1))
    stdscr.refresh()
    if unit == 5:
        global sec1
        clearprev(stdscr, unit, sec1)
        sec1 = val
    elif unit == 4:
        global sec2
        clearprev(stdscr, unit, sec2)
        sec2 = val
    elif unit == 2:
        global min1
        clearprev(stdscr, unit, min1)
        min1 = val
    elif unit == 1:
        global min2
        clearprev(stdscr, unit, min2)
        min2 = val


def clearprev(stdscr, unit, num):
    stdscr.addstr(6+num, unit, "?")
    stdscr.refresh()


def hellpup(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "="*(curses.COLS))
    stdscr.addstr(1, 0,
                  beaut(["hellpup from podomoro",
                         "inital write v2"], curses.COLS)
                  )
    stdscr.addstr(2, 0,
                  beaut(["s : START POMODORO",
                         "q : QUIT"], curses.COLS)
                  )
    stdscr.addstr(3, 0, "="*(curses.COLS))
    stdscr.addstr(5, 0, "00:00")
    stdscr.addstr(6, 0, "0??:??")
    stdscr.addstr(7, 0, "1??:??")
    stdscr.addstr(8, 0, "2??:??")
    stdscr.addstr(9, 0, "3??:??")
    stdscr.addstr(10, 0, "4??:??")
    stdscr.addstr(11, 0, "5??:??")
    stdscr.addstr(12, 0, "6??:??")
    stdscr.addstr(13, 0, "7??:??")
    stdscr.addstr(14, 0, "8??:??")
    stdscr.addstr(15, 0, "9??:??")
    stdscr.refresh()


def beaut(strlist, wide):
    fin = ""
    temp = 0
    for i in strlist:
        temp = temp + len(i)
    wide = wide - temp
    wide = wide / (len(strlist) - 1)
    for i in strlist:
        if i == strlist[-1]:
            fin = fin + strlist[-1]
            continue
        fin = fin + i + " "*int(wide)
    return fin


def main(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.curs_set(0)
    hellpup(stdscr)
    x = stdscr.getch()
    if x == ord('s'):
        startit(stdscr)
    stdscr.addstr(curses.LINES - 1, 0, "Aight, until next time",
                  curses.color_pair(1))


curses.wrapper(main)
