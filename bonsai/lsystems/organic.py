from __future__ import annotations

from typing import List
import random

from bonsai.structures import Command, Branch, Push, Pop, BranchKind, BranchSnapshot, LSystem

def weed_plant(mean_branch_length: int = 20, mean_leaf_length: int = 5) -> LSystem:
    STEM = BranchKind(1)
    LEAF = BranchKind(2)

    system = LSystem(
        seed=[Branch(angle=0, length=5, resistance=1.0, energy=1, kind=STEM)],
        recommended_depth=40,
    )

    @system.add_rule(STEM)
    def handle_stem(snapshot: BranchSnapshot) -> List[Command]:
        branch = snapshot.branch
        can_grow = snapshot.energy_surplus > 10
        branch_limit = mean_branch_length + random.randrange(-4, 4)

        if can_grow:
            if branch.length < branch_limit:
                energy_ratio = (branch.length + 2) / branch.length
                return [
                    branch.clone(length=branch.length + 2, energy=branch.energy * energy_ratio),
                ]
            else:
                length1 = random.randrange(5, branch.length - 5)
                length2 = branch.length - length1

                energy1 = branch.energy * length1 / branch.length
                energy2 = branch.energy * length2 / branch.length

                return [
                    branch.clone(length=length1, energy=energy1),
                    Push(),
                    Branch(
                        angle=random.uniform(10, 30) * random.choice([1, -1]),
                        length=mean_branch_length + random.randrange(-2, 2),
                        energy=5,
                        resistance=0.2,
                        kind=LEAF,
                    ),
                    Pop(),
                    branch.clone(angle=0, length=length2, energy=energy2),
                ]
        else:
            return [branch]

    @system.add_rule(LEAF)
    def handle_leaf(snapshot: BranchSnapshot) -> List[Command]:
        return [snapshot.branch]

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
