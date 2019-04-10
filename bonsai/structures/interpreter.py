from __future__ import annotations

from typing import List, Callable
from .branch import Command, Branch, Push, Pop
from bonsai.turtle_wrapper import TurtleWrapper, TurtleSnapshot


def interpret(t: TurtleWrapper,
              commands: List[Command],
              branch_handler: Callable[[TurtleSnapshot, Branch], List[Command]],
              ) -> List[Command]:
    state_stack = []
    output: List[Command] = []
    for cmd in commands:
        if isinstance(cmd, Push):
            state_stack.append(t.snapshot())
            output.append(cmd)
        elif isinstance(cmd, Pop):
            t.restore(state_stack.pop())
            output.append(cmd)
        elif isinstance(cmd, Branch):
            new_commands = branch_handler(t.snapshot(), cmd)
            naive_interpret(t, new_commands)
            output.extend(new_commands)
        else:
            raise Exception(f"Unrecognized command: {cmd}", cmd)
    return output


def naive_interpret(t: TurtleWrapper, commands: List[Command]) -> None:
    state_stack = []
    for cmd in commands:
        if isinstance(cmd, Push):
            state_stack.append(t.snapshot())
        elif isinstance(cmd, Pop):
            t.restore(state_stack.pop())
        elif isinstance(cmd, Branch):
            t.left(cmd.angle)
            t.forward(cmd.length)
        else:
            raise Exception(f"Unrecognized command: {cmd}", cmd)
