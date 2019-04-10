from __future__ import annotations

import math

def sigmoid(x: float) -> float:
    max_value = 1
    x_midpoint = 0.5
    steepness = 10
    return max_value / (1 + math.e**(-steepness * (x - x_midpoint)))


