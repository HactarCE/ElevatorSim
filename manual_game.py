from getch import getch
from elevator import toggle_display_relative


def play(elevator):
    arrow = 0
    while not elevator.done:
        print(elevator.str_with_arrow(arrow))
        print("Press Q to move up")
        print("Press A to move down")
        print("Press W to open the doors and let on anyone going up")
        print("Press S to open the doors and let on anyone going down")
        print("Press R to toggle relative numbers")
        c = getch()
        if c == '\x03':
            raise KeyboardInterrupt
        if c == '\x1b':
            return
        c = c.lower()
        arrow = 0
        if c == 'q':
            elevator.move_up()
        if c == 'a':
            elevator.move_down()
        if c == 'w':
            arrow = +1
            elevator.open_doors(+1)
        if c == 's':
            arrow = -1
            elevator.open_doors(-1)
        if c == 'r':
            toggle_display_relative()
