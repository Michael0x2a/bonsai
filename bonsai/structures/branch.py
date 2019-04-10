from __future__ import annotations

from typing import NewType, Dict, List, Optional, TypeVar
from dataclasses import dataclass
from math import inf

BranchId = NewType('BranchId', int)
BranchKind = NewType('BranchKind', int)
BranchGraph = Dict[BranchId, List[BranchId]]

DEFAULT_KIND = BranchKind(0)

T = TypeVar('T')


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
    resistance: float = inf

    # How much "energy" this branch inherently contains/consumes
    # per tick, not taking into account any children.
    energy: float = 1.0

    # What "kind" of branch this is -- e.g. trunk, branch, leaf, flower...
    kind: BranchKind = DEFAULT_KIND

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
