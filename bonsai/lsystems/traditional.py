from __future__ import annotations
from typing import List
import random

from bonsai.structures import Command, Branch, Push, Pop, BranchKind, LSystem, BranchSnapshot


def koch_island(d: int = 10) -> LSystem:
    FORWARD = BranchKind(1)

    f = Branch(angle=0, length=d, kind=FORWARD)
    tp = Branch(angle=90, length=0)
    tn = Branch(angle=-90, length=0)

    system = LSystem([f, tn, f, tn, f, tn, f], recommended_depth=4)

    @system.add_rule(FORWARD)
    def f_replace(_: BranchSnapshot) -> List[Command]:
        return [f, tn, f, tp, f, tp, f, f, tn, f, tn, f, tp, f]

    return system


def dragon_curve(d: int = 10) -> LSystem:
    T1 = BranchKind(1)
    T2 = BranchKind(2)

    f1 = Branch(angle=0, length=d, kind=T1)
    f2 = Branch(angle=0, length=d, kind=T2)
    tp = Branch(angle=90, length=0)
    tn = Branch(angle=-90, length=0)

    system = LSystem([f1], recommended_depth=10)

    @system.add_rule(T1)
    def f1_replace(_: BranchSnapshot) -> List[Command]:
        return [f1, tp, f2, tp]

    @system.add_rule(T2)
    def f2_replace(_: BranchSnapshot) -> List[Command]:
        return [tn, f1, tn, f2]

    return system


def bushy_tree(d: int = 10) -> LSystem:
    FORWARD = BranchKind(1)

    f = Branch(angle=0, length=d, kind=FORWARD)
    tp = Branch(angle=22.5, length=0)
    tn = Branch(angle=-22.5, length=0)
    push = Push()
    pop = Pop()

    system = LSystem([f], recommended_depth=4)

    @system.add_rule(FORWARD)
    def f_replace(_: BranchSnapshot) -> List[Command]:
        return [f, f, tn, push, tn, f, tp, f, tp, f, pop, tp, push, tp, f, tn, f, tn, f, pop]

    return system


def flower_field(d: int = 10) -> LSystem:
    FORWARD = BranchKind(1)

    f = Branch(angle=0, length=d, kind=FORWARD)
    tp = Branch(angle=30, length=0)
    tn = Branch(angle=-30, length=0)
    push = Push()
    pop = Pop()

    system = LSystem([f], recommended_depth=4)

    @system.add_rule(FORWARD)
    def f_replace(_: BranchSnapshot) -> List[Command]:
        r = random.random()
        if r <= 0.33:
            return [f, push, tp, f, pop, f, push, tn, f, pop, f]
        elif r <= 0.66:
            return [f, push, tp, f, pop, f]
        else:
            return [f, push, tn, f, pop, f]

    return system


def triangle_koch(d: int = 400) -> LSystem:
    c = 1
    p = 0.3
    q = c - p
    h = (p * q)**0.5

    FORWARD = BranchKind(1)
    tp = Branch(angle=86, length=0)
    tn = Branch(angle=-86, length=0)
    def forward(d: float) -> Branch:
        return Branch(angle=0, length=d, kind=FORWARD)

    system = LSystem([forward(d)], recommended_depth=4)

    @system.add_rule(FORWARD)
    def f_replace(snapshot: BranchSnapshot) -> List[Command]:
        x = snapshot.branch.length
        return [forward(x * p), tp, forward(x * h), tn, tn, forward(x * h), tp, forward(x * q)]

    return system

