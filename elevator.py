from colorama import Fore as Fg
from typing import List, Optional
import colorama
import numpy as np

import symbols
import utils


colorama.init()


DISPLAY_RELATIVE = True


class Person:
    """A person that wants to go to some floor."""

    def __init__(self, destination: int, location: int = None):
        self.destination = destination
        self.location = location

    @property
    def relative_destination(self):
        return self.destination - self.location

    @property
    def direction(self):
        return utils.sign(self.relative_destination)

    @property
    def happy(self):
        return self.destination == self.location

    @property
    def want_up(self):
        return self.direction > 0

    @property
    def want_down(self):
        return self.direction < 0

    def true_str_length(self):
        """Compute len(str(self)), not including ANSI color codes."""
        return 4

    def __str__(self):
        s = ''
        s += Fg.MAGENTA
        s += symbols.get_arrow(
            self.direction == +1,
            self.direction == -1
        )
        s += Fg.YELLOW
        if DISPLAY_RELATIVE:
            n = self.relative_destination
            if n == 0:
                n = '±0'
            elif n > 0:
                n = f'+{n}'
        else:
            n = self.destination
        s += f'{n:>2}'
        s += Fg.RESET
        return f'({s})'


class Platform(list):
    """A place for people to stand."""

    def __init__(self, location: int = 0, persons: List[Person] = [], *, max_capacity: Optional[int] = None):
        self.max_capacity = max_capacity
        self.location = location
        for person in persons:
            self.add(person)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location
        for person in self:
            person.location = location

    @property
    def full(self):
        return self.max_capacity is not None and len(self) >= self.max_capacity

    def add(self, person: Person):
        """Add a person to this platform; return True if successful, and False
        if the platform is already full.
        """
        if self.full:
            return False
        else:
            self.append(person)
            person.location = self.location
            return True

    @property
    def want_up(self):
        return any(person.want_up for person in self)

    @property
    def want_down(self):
        return any(person.want_down for person in self)

    def true_str_length(self):
        """Compute len(str(self)), not including ANSI color codes."""
        return 3 + len(self) + sum(person.true_str_length() for person in self) + (not self)

    def string_with_arrow(self):
        s = ''
        s += Fg.BLUE
        s += symbols.get_arrow(self.want_up, self.want_down)
        s += Fg.RESET
        s += '  '
        return s + str(self)

    def __str__(self):
        return f'[ {" ".join(map(str, self))} ]'


class Elevator(Platform):
    """An elevator consisting of a stationary platform at each floor and one
    moving platform (the carriage).
    """

    def __init__(self, floors: List[Platform], capacity: int):
        super().__init__(max_capacity=capacity)
        self.floors = floors

    def move(self, amount: int):
        """Move the elevator. (positive = up; negative = down)"""
        self.location += amount

    def go_up(self, amount: int = 1):
        """Move the elevator up."""
        self.move(self, amount)

    def go_down(self, amount: int = 1):
        """Move the elevator down."""
        self.move(self, -amount)

    def open_doors(self, direction_indicated: int):
        """Open the elevator doors, letting people off and on."""
        self.let_off()
        self.let_on(direction_indicated)

    def let_off(self):
        """Let off the elevator anyone who wants to get off on this floor."""
        for person in self:
            if person.happy:
                self.remove(person)

    def let_on(self, direction_indicated: int):
        """Let on the elevator anyone who wants to travel in the advertised
        direction.
        """
        floor = self.floors[self.location]
        for person in floor:
            if self.full:
                return
            if person.relative_destination == direction_indicated:
                if self.add(person):
                    floor.remove(person)

    def ml_rep(self, floors_visible: int):
        """Generate the data model used by the machine learning system.

        This model only looks at a certain number of floors near the elevator
        carriage, treating all floors above those as a single clumped-together
        "proxy floor" and all floors below as a single clumped-together proxy
        floor. Each floor and proxy floor has three bits, stored as an integer
        from 0 to 7:
        - Lowest bit:   Someone on this floor wants to go up
        -               Someone on this floor wants to go down
        - Highest bit:  Someone on the elevator wants to get off on this floor
        """
        # Get a set of places that people currently inside the elevator want to
        # go.
        destinations = set(person.destination for person in self)
        # Generate the three bits for each floor.
        floorbits = np.ndarray(len(self.floors), dtype=np.byte)
        for floor in self.floors:
            floorbits[floor.location] = [
                floor.want_up << 1 +
                floor.want_down << 2 +
                (floor.location in destinations) << 3
            ]
        # Find the lowest and highest floors that will be represented alone (not
        # clumped).
        bottom = self.location - floors_visible // 2 + 1
        top = self.location + floors_visible // 2 - 1
        # Clump the floors that need to be clumped.
        if bottom <= 0:
            # Don't use negative numbers outright, because that would take from
            # the end of the list.
            pre = []
        else:
            pre = self.floorbits[:bottom]
        post = self.floorbits[top + 1:]
        return np.concatenate(
            [np.bitwise_or.reduce(pre)],
            floor[bottom:top],
            [np.bitwise_or.reduce(post)],
        )

    def str_with_arrow(self, advertised_direction: int):
        s = ''
        for floor in reversed(self.floors):
            s += '\n'
            s += ' ' * 28
            if floor.location == self.location:
                s += ']  '
                s += Fg.YELLOW
                s += symbols.get_arrow(
                    advertised_direction == +1,
                    advertised_direction == -1,
                )
                s += Fg.RESET
            else:
                s += ' ' * 4
            s += ' ' * 4
            s += floor.string_with_arrow()
            s += f'\r  {floor.location:<6}'
            if floor.location == self.location:
                s += super().__str__()[:-1]
            s += '\n'
        return s

    def __str__(self):
        return self.str_with_arrow(0)
