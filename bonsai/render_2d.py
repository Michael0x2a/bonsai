from __future__ import annotations

from typing import List, Dict, Optional
import turtle

from bonsai.structures import Command, Branch, BranchRenderer, BranchKind, interpret
from bonsai.turtle_wrapper import TurtleWrapper, TurtleSnapshot


def draw_and_wait(t: TurtleWrapper,
                  commands: List[Command],
                  render_rules: Optional[Dict[BranchKind, BranchRenderer]] = None) -> None:
    if render_rules is None:
        render_rules = {}

    renderer = t.clone()

    def render(snapshot: TurtleSnapshot, branch: Branch) -> List[Command]:
        renderer.restore(snapshot)
        if branch.kind in render_rules:
            render_rules[branch.kind](renderer, branch)
        else:
            renderer.pendown()
            renderer.left(branch.angle)
            renderer.forward(branch.length)
            renderer.penup()
        return [branch]

    turtle.tracer(0)
    t.pendown()
    interpret(t, commands, render)
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
