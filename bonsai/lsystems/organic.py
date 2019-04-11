from __future__ import annotations

from typing import List
import random

from bonsai.structures import Command, Branch, Push, Pop, BranchKind, BranchSnapshot, LSystem, DEFAULT_KIND
from bonsai.turtle_wrapper import TurtleWrapper


def weed_plant(start_energy: float = 100) -> LSystem:
    def energy_to_length(energy: float) -> int:
        return int(round(energy / 4))

    START = BranchKind(1)
    BRANCH = BranchKind(2)
    LEAF = BranchKind(3)

    start_length = energy_to_length(start_energy)

    system = LSystem(
        seed=[Branch(angle=0, length=start_length, resistance=1.0, energy=start_energy, kind=START)],
        recommended_depth=20,
    )

    @system.add_rule(START)
    def handle_start(_: BranchSnapshot) -> List[Command]:
        out = [
            Branch(angle=0, length=start_length, energy=start_energy)
        ]
        for _ in range(2):
            out.append(Branch(
                angle=random.randint(-10, 10),
                length=start_length,
                energy=start_energy,
            ))
        out[-1].kind = BRANCH
        return out

    @system.add_rule(BRANCH)
    def handle_branch(snapshot: BranchSnapshot) -> List[Command]:
        def constrain_heading(relative_angle: float) -> float:
            new_global_heading = snapshot.heading + relative_angle
            too_large = True
            while too_large:
                if new_global_heading >= 190:
                    new_global_heading = 190 - random.uniform(0, 10)
                elif new_global_heading <= -10:
                    new_global_heading = -10 + random.uniform(0, 10)
                else:
                    too_large = False
            new_relative_heading = new_global_heading - snapshot.heading
            return new_relative_heading

        branch = snapshot.branch
        energy = branch.energy
        if energy <= 30:
            return [branch.clone(kind=LEAF)]

        if random.random() <= 0.6:
            left_energy = branch.energy * random.uniform(0.85, 0.9)
            right_energy = branch.energy * random.uniform(0.85, 0.9)
            gap_energy = random.uniform(0, branch.energy * random.uniform(0.85, 0.9))

            # Branch into two
            left = [
                Push(),
                Branch(
                    angle=constrain_heading(random.randint(-30, -20)),
                    length=energy_to_length(left_energy),
                    energy=left_energy,
                    kind=BRANCH,
                ),
                Pop(),
            ]
            right = [
                Push(),
                Branch(
                    angle=constrain_heading(random.randint(20, 30)),
                    length=energy_to_length(right_energy),
                    energy=right_energy,
                    kind=BRANCH,
                ),
                Pop(),
            ]
            gap = Branch(angle=0, length=energy_to_length(gap_energy), energy=gap_energy)

            if random.random() <= 5:
                return [branch.clone(kind=DEFAULT_KIND), *left, gap, *right]
            else:
                return [branch.clone(kind=DEFAULT_KIND), *right, gap, *left]
        else:
            # Continue straight-ish
            new_energy = branch.energy * 0.95
            return [
                branch.clone(kind=DEFAULT_KIND),
                Branch(
                    angle=constrain_heading(random.randint(-10, 10)),
                    length=energy_to_length(new_energy),
                    energy=new_energy,
                    kind=BRANCH,
                ),
            ]

    @system.add_render_rule(LEAF)
    def render_leaf(t: TurtleWrapper, branch: Branch) -> None:
        t.shape("circle")
        t.shapesize(0.2, 1.0, 0)
        t.fillcolor(0.8, 1.0, 0.8)
        t.left(branch.angle)
        t.forward(branch.length // 2)
        t.pendown()
        t.stamp()
        t.penup()

    return system




'''


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

'''
