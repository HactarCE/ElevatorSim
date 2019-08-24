UP_ARROW        = '\N{UPWARDS SANS-SERIF ARROW}'
DOWN_ARROW      = '\N{DOWNWARDS SANS-SERIF ARROW}'
UPDOWN_ARROW    = '\N{UP DOWN SANS-SERIF ARROW}'


def get_arrow(up: bool, down: bool):
    if up and down:
        return UPDOWN_ARROW
    elif up:
        return UP_ARROW
    elif down:
        return DOWN_ARROW
    else:
        return ' '
