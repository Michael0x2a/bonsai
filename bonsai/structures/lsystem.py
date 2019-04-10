from __future__ import annotations

from typing import Optional, List, Dict, Callable, Tuple
from dataclasses import dataclass

from bonsai.turtle_wrapper import TurtleWrapper, TurtleSnapshot
from .branch import Command, Branch, BranchKind, DEFAULT_KIND
from .interpreter import interpret


BranchTransformer = Callable[['BranchSnapshot'], List[Command]]


@dataclass
class BranchSnapshot:
    branch: Branch
    energy_surplus: float
    pos: Tuple[float, float]
    heading: float


class LSystem:
    def __init__(self, seed: List[Command],
                       rules: Optional[Dict[BranchKind, BranchTransformer]] = None,
                       recommended_depth: int = 3) -> None:
        self.seed = seed
        if rules is None:
            rules = {}
        self.rules = rules
        self.recommended_depth = recommended_depth

    def add_rule(self, kind: BranchKind) -> Callable[[BranchTransformer], BranchTransformer]:
        def adder(transformer: BranchTransformer) -> BranchTransformer:
            if kind in self.rules:
                raise Exception(f"Rule for kind {kind} already present")
            self.rules[kind] = transformer
            return transformer
        return adder

    def add_default_rule(self) -> Callable[[BranchTransformer], BranchTransformer]:
        return self.add_rule(DEFAULT_KIND)

    def expand(self, t: TurtleWrapper, depth: Optional[int] = None, available_energy: float = 100) -> List[Command]:
        if depth is None:
            depth = self.recommended_depth
        t.penup()
        output = self.seed
        for i in range(depth):
            output = self._step_lsystem(t.clone(), output, available_energy)
        return output

    def _step_lsystem(self, t: TurtleWrapper, commands: List[Command], available_energy: float = 100) -> List[Command]:
        total_energy_used = sum(b.energy for b in commands if isinstance(b, Branch))
        surplus = max(available_energy - total_energy_used, 0)

        def handler(_: TurtleSnapshot, branch: Branch) -> List[Command]:
            if branch.kind in self.rules:
                snapshot = BranchSnapshot(branch, energy_surplus=surplus, pos=t.pos(), heading=t.heading())
                return self.rules[branch.kind](snapshot)
            else:
                return [branch]

        return interpret(t, commands, handler)

