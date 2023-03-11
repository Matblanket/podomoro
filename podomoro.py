import curses, sys, select, queue, threading, time

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


def letter(i, offsetx=0, offsety=0):
    i = int(i)
    temp = krys[i]
    for u in temp:
        block(u[0] * 2 + offsety, u[1] * 2 + offsetx, i)


def block(y, x, char=61):
    if char == 10:
        char = 32
    else:
        char = 9608
    joblist.put([y + 0, x, chr(char) * 3])
    joblist.put([y + 1, x, chr(char) * 3])


def waitforme(stdscr):
    hellpup(["c : CONTINUE POMODORO", "q : QUIT"])
    while True:
        statfill("Podomoro session paused :/")
        t = stdscr.getch()
        if t == ord('c'):
            return 1
        if t == ord('q'):
            return 0

def startit():
    j = 10
    global prevpi3
    global prevpi1
    global prevpi0
    hellpup(["p : PAUSE POMODORO", "r : RESET POMODORO", "q : QUIT"])
    statlinelock.acquire()
    #statfill("Time to get productive (' ' )_/*")
    statlinelock.release()
    print("here")
    while not tkillpill.wait(1) and j > 0:
        pi = str(int(j / 60))+':'+str(int(j % 60))
        if len(pi) != 5:
            if pi.find(':') < 2:
                while pi.find(':') != 2:
                    pi = '0'+pi
            while len(pi) != 5:
                pi = pi[:3]+'0'+pi[3:]
        joblist.put([5, 1, str(pi)])



        letter(10, 9, 9)
        letter(pi[0], 9, 9)
        letter(10, 19, 9)
        letter(pi[1], 19, 9)
        letter(10, 29, 9)
        letter(pi[3], 29, 9)
        letter(10, 39, 9)
        letter(pi[4], 39, 9)



        highlight(4+1, int(pi[4]))
        if prevpi3 != pi[3]:
            highlight(3+1, int(pi[3]))
        prevpi3 = pi[3]
        if prevpi1 != pi[1]:
            highlight(1+1, int(pi[1]))
        prevpi1 = pi[1]
        if prevpi0 != pi[0]:
            highlight(0+1, int(pi[0]))
        prevpi0 = pi[0]



#        x = stdscr.getch()
#        if x == ord('p'):
#            if waitforme(stdscr) == 0:
#                break
#            else:
#                hellpup(["p : PAUSE POMODORO", "r : RESET POMODORO",
#                                 "q : QUIT"])
#                statfill(stdscr, "Continuing podomoro session..")
#        elif x == ord('q'):
#            break
#        elif x == ord('r'):
#            stdscr.nodelay(False)
#            statfill(stdscr, "Reset podomoro session?(y/n)", color=1, stay=1)
#            x = stdscr.getch()
#            if x == ord('y'):
#                j = 2500
#            statfill(stdscr, "")
#            time.sleep(0.1)
#            stdscr.nodelay(True)
        j = j - 1


def highlight(unit, val):
    joblist.put([6+val, unit, chr(9608), curses.color_pair(1)])
    if unit == 5:
        global sec1
        clearprev(unit, sec1)
        sec1 = val
    elif unit == 4:
        global sec2
        clearprev(unit, sec2)
        sec2 = val
    elif unit == 2:
        global min1
        clearprev(unit, min1)
        min1 = val
    elif unit == 1:
        global min2
        clearprev(unit, min2)
        min2 = val


def clearprev(unit, num):
    joblist.put([6+num, unit, "█"])


def hellpup(str):
    joblist.put([0, 0, "="*(curses.COLS)])
    joblist.put([1, 0, beaut(["hellpup from podomoro", "inital write v2"], curses.COLS)])
    joblist.put([2, 0, beaut(str, curses.COLS) ])
    joblist.put([3, 0, "="*(curses.COLS)])


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


def inputer():
    while True:
        r, w, e = select.select([sys.stdin], [], [], 0)
        if sys.stdin in r:
            inputlist.put(sys.stdin.read(1))
        joblist.put([100,100,inputlist.get()])


def main():
    global length
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_RED,-1)
    length = curses.COLS - start
    curses.curs_set(0)
    joblist.put([5, 0,  " 00:00"])
    joblist.put([6, 0,  "0██:██"])
    joblist.put([7, 0,  "1██:██"])
    joblist.put([8, 0,  "2██:██"])
    joblist.put([9, 0,  "3██:██"])
    joblist.put([10, 0, "4██:██"])
    joblist.put([11, 0, "5██:██"])
    joblist.put([12, 0, "6██:██"])
    joblist.put([13, 0, "7██:██"])
    joblist.put([14, 0, "8██:██"])
    joblist.put([15, 0, "9██:██"])
    coords(length, start, depth)
    hellpup(["s : START POMODORO", "q : QUIT"])
#        subprocess.getoutput("cvlc --play-and-exit temp.opus")


start= 10
depth = 5
length = 20


def statfill(x="", color=0, stay=0):
    coords(length, start, depth)
    if x != "":
        j = 0
        while j < len(x) and j < length - 6:
            joblist.put([depth+1, start+4+j, "_", curses.color_pair(color)])
            time.sleep(0.05)
            joblist.put([depth+1, start+4+j, x[j], curses.color_pair(color)])
            time.sleep(0.05)
            j = j + 1
        while j < len(x):
            joblist.put([depth+1, start+4, x[j-length+6:j+1], curses.color_pair(color)])
            time.sleep(0.1)
            j = j + 1
        time.sleep(1)
    if stay != 1:
        for k in ['*', '+', '-', '.', ' ']:
            fillstatus(k)
            time.sleep(0.1)
    time.sleep(1)


def fillstatus(x=" "):
    joblist.put([depth + 1, start+4, x*(length-5)])


def coords(length=10, start=10, depth=3):
    joblist.put([depth, start, "+"+"-"*(length-2)+"+"])
    joblist.put([depth+1, start, "| >"])
    joblist.put([depth+1, start + length - 1, "|"])
    joblist.put([depth+2, start, "+"+"-"*(length-2)+"+"])


def starter():
    curses.wrapper(damn)


def damn(stdscr):
    stdscr.clear()
    while not tkillpill.wait(0):
        a = joblist.get(block=True,timeout=5)
        stdscr.addstr(a[0],a[1],a[2])
        stdscr.refresh()
        time.sleep(0.009)


statlinelock = threading.Lock()
tkillpill = threading.Event()
tinputproc = threading.Thread(target=inputer)
tinputproc.start()
joblist = queue.Queue()
inputlist = queue.Queue()
threading.Thread(target=starter).start()
main()
startit()
