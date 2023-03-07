import curses
import time
import os
import subprocess

prevpi3 = 0
prevpi1 = 0
prevpi0 = 0
sec1 = 0
sec2 = 0
min1 = 0
min2 = 0
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


def grid(i):
    return krys[i]


def letter(stdscr, i, offsetx=0, offsety=0):
    i = int(i)
    temp = grid(i)
    for u in temp:
        block(stdscr, u[0] * 2 + offsety, u[1] * 2 + offsetx, i)
    stdscr.refresh()


def block(stdscr, y, x, char=61):
    if char == 10:
        char = 32
    else:
        char = 9608
    stdscr.addstr(y + 0, x, chr(char) * 3)
    stdscr.addstr(y + 1, x, chr(char) * 3)


def waitforme(stdscr):
    hellpup(stdscr, ["c : CONTINUE POMODORO", "q : QUIT"])
    while True:
        statfill(stdscr, "Podomoro session paused :/")
        t = stdscr.getch()
        if t == ord('c'):
            return 1
        if t == ord('q'):
            return 0


def startit(stdscr):
    j = 2500
    global prevpi3
    global prevpi1
    global prevpi0
    hellpup(stdscr, ["p : PAUSE POMODORO", "r : RESET POMODORO", "q : QUIT"])
    statfill(stdscr, "Time to get productive (' ' )_/*")
    while j > 0:
        stdscr.nodelay(True)
        pi = str(int(j / 60))+':'+str(int(j % 60))
        if len(pi) != 5:
            if pi.find(':') < 2:
                while pi.find(':') != 2:
                    pi = '0'+pi
            while len(pi) != 5:
                pi = pi[:3]+'0'+pi[3:]
        stdscr.addstr(5, 1, str(pi))
        letter(stdscr, 10, 9, 9)
        letter(stdscr, pi[0], 9, 9)
        letter(stdscr, 10, 19, 9)
        letter(stdscr, pi[1], 19, 9)
        letter(stdscr, 10, 29, 9)
        letter(stdscr, pi[3], 29, 9)
        letter(stdscr, 10, 39, 9)
        letter(stdscr, pi[4], 39, 9)
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
            if waitforme(stdscr) == 0:
                break
            else:
                hellpup(stdscr, ["p : PAUSE POMODORO", "r : RESET POMODORO",
                                 "q : QUIT"])
                statfill(stdscr, "Continuing podomoro session..")
        elif x == ord('q'):
            break
        elif x == ord('r'):
            stdscr.nodelay(False)
            statfill(stdscr, "Reset podomoro session?(y/n)", color=1, stay=1)
            x = stdscr.getch()
            if x == ord('y'):
                j = 2500
            statfill(stdscr, "")
            time.sleep(0.1)
            stdscr.nodelay(True)
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
    stdscr.addstr(6+num, unit, "█")
    stdscr.refresh()


def hellpup(stdscr, str):
    stdscr.addstr(0, 0, "="*(curses.COLS))
    stdscr.addstr(1, 0,
                  beaut(["hellpup from podomoro",
                         "inital write v2"], curses.COLS)
                  )
    stdscr.addstr(2, 0,
                  beaut(str, curses.COLS)
                  )
    stdscr.addstr(3, 0, "="*(curses.COLS))
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
    global length
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_RED,-1)
    length = curses.COLS - start
    curses.curs_set(0)
    stdscr.addstr(5, 0,  " 00:00")
    stdscr.addstr(6, 0,  "0██:██")
    stdscr.addstr(7, 0,  "1██:██")
    stdscr.addstr(8, 0,  "2██:██")
    stdscr.addstr(9, 0,  "3██:██")
    stdscr.addstr(10, 0, "4██:██")
    stdscr.addstr(11, 0, "5██:██")
    stdscr.addstr(12, 0, "6██:██")
    stdscr.addstr(13, 0, "7██:██")
    stdscr.addstr(14, 0, "8██:██")
    stdscr.addstr(15, 0, "9██:██")
    coords(stdscr, length, start, depth)
    stdscr.refresh()
    hellpup(stdscr, ["s : START POMODORO", "q : QUIT"])
    x = stdscr.getch()
    while True:
        startit(stdscr)
        subprocess.getoutput("cvlc --play-and-exit temp.opus")


start = 10
depth = 5
length = 20


def statfill(stdscr, x="", color=0, stay=0):
    coords(stdscr, length, start, depth)
    stdscr.refresh()
    if x != "":
        j = 0
        while j < len(x) and j < length - 6:
            stdscr.addstr(depth+1, start+4+j, "_", curses.color_pair(color))
            stdscr.refresh()
            time.sleep(0.05)
            stdscr.addstr(depth+1, start+4+j, x[j], curses.color_pair(color))
            stdscr.refresh()
            time.sleep(0.05)
            j = j + 1
        while j < len(x):
            stdscr.addstr(depth+1, start+4, x[j-length+6:j+1],
                          curses.color_pair(color))
            stdscr.refresh()
            time.sleep(0.1)
            j = j + 1
        time.sleep(1)
    if stay != 1:
        for k in ['*', '+', '-', '.', ' ']:
            fillstatus(stdscr, k)
            time.sleep(0.1)
    time.sleep(1)


def fillstatus(stdscr, x=" "):
    stdscr.addstr(depth + 1, start+4, x*(length-5))
    stdscr.refresh()


def coords(stdscr, length=10, start=10, depth=3):
    stdscr.addstr(depth, start, "+"+"-"*(length-2)+"+")
    stdscr.addstr(depth+1, start, "| >")
    stdscr.addstr(depth+1, start + length - 1, "|")
    stdscr.addstr(depth+2, start, "+"+"-"*(length-2)+"+")


curses.wrapper(main)
