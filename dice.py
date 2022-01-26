#!/usr/bin/env python3

"""
A simple program for rolling virtual dice of various sizes. Right now it can
only handle simple rolls of polyhedral dice, but in the future it will also
be able to handle things like addition and counting successes. There's also
a plan to test using Pyglet for a GUI.

I'll also add support for Genesys RPG dice, which would actually be useful to
have. It'll probably use the number conversion table from the core book, but
will have to handle things like canceling success/failure and advantage/threat.
"""

from random import randint

roll = input("Please enter your dice roll in the form XdY: ")
roll = [eval(num) for num in roll.split("d")]

print(f"Your roll is {roll[0]}d{roll[1]}.")
roll = [randint(1, roll[1]) for x in range(roll[0])]
print(f"Your result is {sum(roll)}: {roll}\n")
