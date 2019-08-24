import random

from elevator import Elevator, Person, Platform


ELEVATOR_CAPACITY = 3
FLOORS = 8
PEOPLE_PER_FLOOR = 7


def random_elevator():
    e = Elevator(
        [
            Platform(floor, [
                Person(random.randrange(FLOORS))
                for _ in range(PEOPLE_PER_FLOOR)
            ])
            for floor in range(FLOORS)
        ],
        capacity=ELEVATOR_CAPACITY,
    )
    while not e.full:
        e.add(Person(random.randrange(FLOORS)))
    return e
