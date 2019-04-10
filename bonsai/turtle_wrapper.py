from __future__ import annotations

from typing import Iterator, Tuple, Dict, cast

import turtle
from contextlib import contextmanager
from dataclasses import dataclass


PenState = Dict[str, object]


class TurtleWrapper(turtle.Turtle):
    def __init__(self, start_x: float, start_y: float, start_heading: float, pendown: bool = False) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        if pendown:
            self.pendown()
        else:
            self.penup()
        self.original_snapshot = TurtleSnapshot(
            pos=(start_x, start_y),
            heading=start_heading,
            pen=self.pen(),
        )
        self.restore(self.original_snapshot)

    def clone(self) -> TurtleWrapper:
        return TurtleWrapper.from_snapshot(self.snapshot())

    @staticmethod
    def from_snapshot(snapshot: TurtleSnapshot, pendown: bool = False) -> TurtleWrapper:
        return TurtleWrapper(
            start_x=snapshot.pos[0],
            start_y=snapshot.pos[1],
            start_heading=snapshot.heading,
            pendown = pendown,
        )

    @contextmanager
    def no_draw(self) -> Iterator[None]:
        state = self.pen()
        self.penup()
        yield None
        self.pen(pendown=cast(bool, state["pendown"]))

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
