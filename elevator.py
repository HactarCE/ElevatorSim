from typing import List, Optional

from utils import sign


ELEVATOR_CAPACITY = 3

FLOORS = 8


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
        return sign(self.destination)

    @property
    def happy(self):
        return self.destination == self.location


class Platform(list):
    """A place for people to stand."""

    def __init__(self, location: int = 0, *, max_capacity: Optional[int] = None, persons: List[Person] = []):
        self.max_capacity = max_capacity
        self.location = location
        for person in persons:
            self.append(person)

    @property
    def location(self):
        return self._floor

    @location.setter
    def location(self, location):
        self._floor = location
        for person in self.persons:
            person.location = location

    @property
    def full(self):
        return len(self) >= self.max_capacity

    def add(self, person: Person):
        if self.full:
            return False
        else:
            return self.append(person)


class Elevator:
    """An elevator consisting of a stationary platform at each floor and one
    moving platform (the carriage).
    """

    def __init__(self, floors: List[Platform], *, capacity: int = ELEVATOR_CAPACITY):
        self.location = 0
        self.floors = floors
        self.carriage = Platform(capacity)

    @property
    def location(self):
        return self.carriage.location

    @location.setter
    def location(self, location):
        self.carriage.location = location

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
        self.let_off(self)
        self.let_on(self, direction_indicated)

    def let_off(self):
        """Let off the elevator anyone who wants to get off on this floor."""
        for person in self.carriage:
            if person.happy:
                self.carriage.remove(person)

    def let_on(self, direction_indicated: int):
        """Let on the elevator anyone who wants to travel in the advertised
        direction.
        """
        floor = self.floors[self.location]
        for person in floor:
            if self.carriage.full:
                return
            if person.relative_destination == direction_indicated:
                self.carriage.add(person)
                floor.remove(person)
