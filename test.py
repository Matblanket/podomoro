import curses
import time


def main(stdscr, x="hellllllllpip"):
    curses.curs_set(0)
    stdscr.addstr(8, 8, "+"+"-"*(curses.COLS - 20))
    stdscr.addstr(9, 8, "| >")
    stdscr.addstr(10, 8, "+"+"-"*(curses.COLS - 20))
    x = x+"/"*curses.COLS
    j = 20
    i = 1
    if x != "":
        while curses.COLS - j > 11:
            stdscr.addstr(9, curses.COLS - j, x[0:i])
            stdscr.refresh()
            time.sleep(0.01)
            j = j+1
            i = i+1
        for j in ['*', '+', '-', '.', ' ']:
            fillstatus(stdscr, j)
            time.sleep(0.2)
    time.sleep(1)


def fillstatus(stdscr, x=" "):
    stdscr.addstr(9, 11, x*(curses.COLS - 11))
    stdscr.refresh()


curses.wrapper(main)
