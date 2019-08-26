#!/usr/bin/env python

import generators as gen
import manual_game

print(gen.random_elevator().str_with_arrow(+1))
manual_game.play(gen.random_elevator())
