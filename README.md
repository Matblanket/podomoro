# Podomoro 

This is a simple Pomodoro Clock written in Python using ncurses library. It allows you to start, pause, reset the timer with keyboard shortcuts.

## Requirements

- Python 3.6 or higher
- ncurses library (pre-installed on most Unix-based systems)

## How to use

1. Download the `pomodoro.py` file to your local machine.
2. Open a terminal window and navigate to the directory where `pomodoro.py` is located.
3. Run the following command: `python3 pomodoro.py`
4. The Pomodoro Clock will start running, and you will see a timer counting down from 25 minutes on the screen.
5. You can use the following keyboard shortcuts to control the timer:
   - `p` - Pause/Resume the timer
   - `r` - Reset the timer
   - `q` - Quit the program

## How it works

The Pomodoro Clock uses the ncurses library to display the timer on the screen and accept keyboard input. The timer is set to 25 minutes by default, but you can easily change this value by editing the `POMODORO_TIME` constant in the code.

The clock uses a loop to update the timer every second and display it on the screen. When the timer reaches 0, the clock will play a sound and display a message indicating that the pomodoro session has ended.

If you find any bugs or issues, please feel free to report them.

