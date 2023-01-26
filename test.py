import curses
import time
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
    9: [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (2, 2)]
}


def main(stdscr):
    stdscr.clear()
    for i in range(10):
        letter(stdscr, 2)
        time.sleep(1)
        stdscr.clear()


def grid(i):
    return krys[i]


def letter(stdscr, i, offsetx=0):
    for u in grid(i):
        block(stdscr, u[0] * 3, u[1] * 3 + offsetx)


def block(stdscr, y, x):
    stdscr.addstr(y + 0, x, chr(61) * 3)
    stdscr.addstr(y + 1, x, chr(61) * 3)
    stdscr.addstr(y + 2, x, chr(61) * 3)
    stdscr.refresh()


curses.wrapper(main)
