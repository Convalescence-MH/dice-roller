#!/usr/bin/env python3

"""
A simple program for rolling virtual dice of various sizes. Right now it can
only handle simple rolls of polyhedral dice, but in the future it will also
be able to handle things like addition and counting successes.

I'll also add support for Genesys RPG dice, which would actually be useful to
have. It'll probably use the number conversion table from the core book, but
will have to handle things like canceling success/failure and advantage/threat.
"""

from random import randint
import pyglet

window = pyglet.window.Window(caption="Dice Roller")

roll = input("Please enter your dice roll in the form XdY: ")
roll = [eval(num) for num in roll.split("d")]

@window.event
def on_draw():
    window.clear()
    roll_label.draw()
    result.draw()

roll_label = pyglet.text.Label(f"Your roll is {roll[0]}d{roll[1]}",
        font_size = 16,
        x = window.width//2, y = window.height//2,
        anchor_x = "center", anchor_y = "center")

roll = [randint(1, roll[1]) for x in range(roll[0])]

result = pyglet.text.Label(f"Your result is {sum(roll)}: {roll}",
        font_size = 16,
        x = window.width//2, y = window.height//2 - 20,
        anchor_x = "center", anchor_y = "center")

if __name__ == "__main__":
    pyglet.app.run()
