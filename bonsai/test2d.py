from __future__ import annotations

from typing import List

from bonsai.structures import Command, Branch, interpret
from bonsai.math_utils import sigmoid
from bonsai.turtle_wrapper import TurtleWrapper, TurtleSnapshot
import bonsai.lsystems.traditional as traditional
import bonsai.lsystems.organic as organic
import bonsai.render_2d as render_2d

def interpolate_headings(h1: float, h2: float, a: float, b: float) -> float:
    bigger = h1 
    smaller = h2 
    if smaller > bigger:
        bigger, smaller = smaller, bigger
        a, b = b, a

    delta = bigger - smaller
    sign = 1
    if delta > 180:
        delta = 360 - delta
        sign = -1

    delta_adjusted = delta * sigmoid(a / (a + b))
    out = smaller + sign * delta_adjusted
    if out < 0:
        out += 360
    return out


def apply_force(t: TurtleWrapper, commands: List[Command],
                global_heading: float, force: float) -> List[Command]:

    def handler(t: TurtleSnapshot, branch: Branch) -> List[Command]:
        new_heading = interpolate_headings(
            t.heading + branch.angle,
            global_heading,
            branch.resistance,
            force,
        )
        angle = new_heading - t.heading
        return [branch.clone(angle=angle)]

    return interpret(t, commands, handler)


def main() -> None:
    import turtle
    turtle.tracer(0)
    t = TurtleWrapper(0, -250, 90)

    print("Fetching lsystem rules...")
    lsystem = organic.weed_plant()

    print("Generating...")
    commands = lsystem.expand(t.clone(), available_energy=1000)

    print(f"Finished generating. Produced final instruction list of length {len(commands)}; now rendering...")
    render_2d.draw_and_wait(t.clone(), commands, render_rules=lsystem.render_rules)


if __name__ == '__main__':
    main()


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


if __name__ == '__main__':
    main()
'''
