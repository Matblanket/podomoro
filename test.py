import curses

# Initialize ncurses
stdscr = curses.initscr()

# Set the starting coordinates
y = 5  # Desired y-coordinate
x = 10  # Desired x-coordinate

# Multiline string to print
multiline_string = """This
is a
multiline
string."""

# Print the multiline string at the specified coordinates
stdscr.addstr(y, x, multiline_string)

# Refresh the screen to display the output
stdscr.refresh()

# Wait for user input
stdscr.getch()

# End ncurses
curses.endwin()

