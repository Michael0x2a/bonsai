from __future__ import annotations

from typing import List
import turtle

from bonsai.structures import Command, naive_interpret
from bonsai.turtle_wrapper import TurtleWrapper


def draw_and_wait(t: TurtleWrapper, commands: List[Command]) -> None:
    turtle.tracer(0)
    t.pendown()
    naive_interpret(t, commands)
    turtle.update()
    turtle.mainloop()

'''




def animate(fps, command_generator, command_drawer):
    turtle.tracer(0)
    t = TurtleWrapper(0, -250, 90)

    tick = 0
    delay = int(round(1000 / fps))
    commands = None

    def refresh_model(*args, **kwargs):
        nonlocal commands
        commands = command_generator()

    def advance_frame():
        nonlocal tick
        t.reset()

        command_drawer(t, tick, commands)
        turtle.update()
        tick += delay
        turtle.ontimer(advance_frame, delay)

    turtle.onscreenclick(refresh_model)

    refresh_model()
    advance_frame()

    turtle.mainloop()


def main():
    lsystem = windswept_tree(random, 50)

    wind = 0
    wind_acceleration = 0

    def regenerate():
        return expand(lsystem, 10)

    def draw(t, tick, commands):
        step = tick / 1000.0 * math.pi

        hi, lo = 0.15, 0.1
        wind = (math.sin(step) / 2 + 0.5) * (hi - lo) + lo

        commands_with_wind = apply_force(t.original_snapshot, commands, 0, wind)
        interpret(t, commands_with_wind)

    animate(60, regenerate, draw)
'''
