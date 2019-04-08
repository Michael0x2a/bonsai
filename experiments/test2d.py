from __future__ import annotations

from typing import List, Dict, Iterator, Tuple, Mapping, Optional, NewType, Callable, TypeVar

import turtle
import random
import math
from contextlib import contextmanager
from euclid3 import Vector2
from dataclasses import dataclass

PenState = Mapping[str, object]

BranchId = NewType('BranchId', int)
BranchKind = NewType('BranchKind', int)
Hormone = NewType('Hormone', int)
BranchGraph = Dict[BranchId, List[BranchId]]

class TurtleWrapper(turtle.Turtle):
    def __init__(self, start_x: float, start_y: float, start_heading: float) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.original_snapshot = TurtleSnapshot(
            pos=(start_x, start_y),
            heading=start_heading,
            pen=self.pen(),
        )
        self.restore(self.original_snapshot)

    @staticmethod
    def from_snapshot(snapshot: TurtleSnapshot) -> TurtleWrapper:
        return TurtleWrapper(
            start_x=snapshot.pos[0],
            start_y=snapshot.pos[1],
            start_heading=snapshot.heading,
        )

    @contextmanager
    def no_draw(self) -> Iterator[None]:
        state = self.pen()
        self.penup()
        yield None
        self.pen(pendown=state["pendown"])

    def jump(self, x, y):
        with self.no_draw():
            self.goto(x, y)

    def snapshot(self) -> TurtleSnapshot:
        return TurtleSnapshot(
            pos=self.position(),
            heading=self.heading(),
            pen=self.pen(),
        )

    def restore(self, snapshot: TurtleSnapshot) -> None:
        with self.no_draw():
            self.setposition(snapshot.pos)
            self.setheading(snapshot.heading)
            self.pen(snapshot.pen)

    def reset(self) -> None:
        super().reset()
        self.restore(self.original_snapshot)


@dataclass
class TurtleSnapshot:
    pos: Tuple[float, float]
    heading: float
    pen: PenState


T = TypeVar('T')


def sigmoid(x: float) -> float:
    max_value = 1
    x_midpoint = 0.5
    steepness = 10
    return max_value / (1 + math.e**(-steepness * (x - x_midpoint)))


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


def apply_force(start, commands, global_heading, force):
    t = TurtleWrapper.from_snapshot(start)
    t.speed(0)
    t.hideturtle()
    t.penup()

    state = []
    output = []
    for cmd in commands:
        if isinstance(cmd, Branch):
            new_heading = interpolate_headings(
                t.heading() + cmd.angle,
                global_heading, 
                cmd.resistance, 
                force,
            )
            angle = new_heading - t.heading()
            output.append(cmd.clone(angle=angle))
            t.left(angle)
            t.forward(cmd.length)
        elif isinstance(cmd, Push):
            output.append(cmd)
            state.append(t.snapshot())
        elif isinstance(cmd, Pop):
            output.append(cmd)
            t.restore(state.pop())
        else:
            raise Exception(f"Unknown command: {cmd}")

    return output


def expand(lsystem, depth):
    axiom, productions = lsystem

    output = axiom
    for i in range(depth):
        new_output = []
        for cmd in output:
            if isinstance(cmd, Branch) and cmd.hormone in productions:
                new_output.extend(productions[cmd.hormone](cmd))
            else:
                new_output.append(cmd)
        output = new_output

    return output


def invert_graph(graph: BranchGraph) -> BranchGraph:
    out = {}
    for parent, children in graph.items():
        if parent not in out:
            out[parent] = []
        for child in children:
            if child not in out:
                out[child] = []
            out[child].append(parent)
    return out


@dataclass
class TreeSnapshot:
    branches: List[Branch]
    parent_to_child: BranchGraph
    hormones_forward: Dict[BranchId, List[Hormone]]
    hormones_back: Dict[BranchId, List[Hormone]]


def advance_tree(old: TreeSnapshot,
                 simulator: Callable[[BranchSnapshot], ???]
                 ) -> TreeSnapshot:
    new_branches = []
    for old_id, old_branch in enumerate(old.branches):
        parent_ids = self.child_to_parent[old_id]
        children_ids = self.parent_to_child[old_id]

        old_children = [old.branches[i] for i in children_ids]

        hormones_from_children = [*self.hormones_back[c] for c in children]
        hormones_from_parent = [self.hormones_forward[p] for p in parent]

        new_id = len(new_branches)

        branch_modified, children = simulator()


class Command: pass

class Push(Command): pass

class Pop(Command): pass

@dataclass
class Branch(Command):
    # The angle this branch juts out from (at the start)
    angle: float

    # The length of this branch
    length: float

    # How "stiff" the joint at the start is -- analogous to
    # the internal resistance or friction. Should be in
    # Newton-meters per radians per second, and should always
    # be positive.
    resistance: float
    
    # How much "energy" this branch inherently contains/consumes
    # per tick, not taking into account any children.
    energy: float

    # What "kind" of branch this is -- e.g. trunk, branch, leaf, flower...
    kind: BranchKind

    def clone(self, angle: Optional[float] = None,
                    length: Optional[float] = None,
                    resistance: Optional[float] = None,
                    energy: Optional[float] = None,
                    kind: Optional[BranchKind] = None,
                    ) -> Branch:
        def wrap(curr: T, new: Optional[T]) -> T:
            return curr if new is None else new

        return Branch(
            angle=wrap(self.angle, angle),
            length=wrap(self.length, length),
            resistance=wrap(self.resistance, resistance),
            energy=wrap(self.energy, energy),
            kind=wrap(self.kind, kind),
        )



@dataclass
class BranchSnapshot:
    branch: Branch
    energy_surplus: float
    pos: Tuple[float, float]
    heading: float


class WeedPlant:
    STEM = BranchKind(1)
    LEAF = BranchKind(2)

    def handle_stem(self, snapshot: BranchSnapshot) -> List[Command]:
        assert snapshot.branch.kind == STEM
        branch = snapshot.branch

        if snapshot.energy_surplus > 10:
            if random.rand() <= 0.7:
                # We can branch
                return [
                    snapshot.branch.clone(length * )
                    Branch(
                        angle=random.uniform(-20, 20),
                        length=5,
                        resistance=0.4,
                        energy=10,
                        kind=LEAF,
                    ))


        



def windswept_tree(snapshot):
    branch = snapshot.curr


    if 
                




def windswept_tree(rand, d):
    START = 1
    BRANCH = 2
    IGNORE = 3

    def start_replace(cmd):
        turn = rand.randint(-10, 10)
        out = [
            Branch(angle=0, length=d, energy=cmd.energy, resistance=1.0, hormone=IGNORE),
        ]
        for _ in range(2):
            out.append(Branch(
                angle=rand.randint(-10, 10), 
                length=d,
                energy=cmd.energy,
                resistance=1.0,
                hormone=IGNORE,
            ))
        out[-1].hormone = BRANCH
        return out

    def branch_replace(cmd):
        r = cmd.resistance

        if r <= 0.05:
            # TODO: Add leaf?
            return []

        if rand.random() <= 0.6:
            # Branch into two
            left = [
                Push(),
                Branch(
                    angle=rand.randint(-30, -20),
                    length=d * r,
                    energy=cmd.energy,
                    resistance=rand.uniform(0.85, 0.9) * r,
                    hormone=BRANCH,
                ),
                Pop(),
            ]

            right = [
                Push(),
                Branch(
                    angle=rand.randint(20, 30),
                    length=d * r,
                    energy=cmd.energy,
                    resistance=rand.uniform(0.85, 0.9) * r,
                    hormone=BRANCH,
                ),
                Pop(),
            ]

            gap = Branch(
                angle=0,
                length=rand.randint(0, int(d * r)),
                energy=cmd.energy,
                resistance=r,
                hormone=IGNORE,
            )

            if rand.random() <= 0.5:
                return [cmd.clone(hormone=IGNORE), *left, gap, *right] 
            else:
                return [cmd.clone(hormone=IGNORE), *right, gap, *left]
        else:
            # Continue straight-ish
            return [
                cmd.clone(hormone=IGNORE),
                Branch(
                    angle=rand.randint(-10, 10),
                    length=d * r,
                    resistance=0.95 * r,
                    energy=cmd.energy,
                    hormone=BRANCH,
                )
            ]

    axiom = [Branch(
        angle=0,
        length=0,
        resistance=1.0,
        energy=1.0,
        hormone=START,
    )]

    productions = {
        START: start_replace,
        BRANCH: branch_replace,
    }

    return axiom, productions


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
