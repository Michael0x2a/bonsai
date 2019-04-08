#!/usr/bin/env python3

import math
from solid import *
from solid.utils import *
from solid_toolbox import *
from euclid3 import Vector3, Quarternion

def force_str(vec):
    return '[{}]'.format(', '.join(map(str, vec)))


# TODO: Remove this workaround once an upstream patch to solidpython lands
Vector3.__repr__ = force_str
Vector3.__str__ = force_str


class Turtle:
    def __init__(self, location=Vector3(0, 0, 0), models=None):
        self.location = location
        self.orientation = Quarternion()
        self.models = [] if models is None else models

    def spawn(self):
        return Turtle(self.location, self.orientation, self.models)

    def apply(self, distance):
        def wrapper(model):
            self.models.append(translate(self.location)(
                rotate(self.orientation)(
                    model,
                ),
            ))
            self.location += self.orientation * distance

        return wrapper

    def rotate(self, axis, angle):
        self.orientation = self.orientation * Quarternion.new_rotate_axis(angle, axis)

    def union(self):
        return union()(*self.models)


def generate_model():
    t = Turtle()
    t.apply(10*cm)(
        cylinder(r=1*cm, h=10*cm),
    )
    t.rotate(Vec(0, 1, 0))
    t.apply(5*cm)(
        cylinder(r=0.5*cm, h=5*cm),
    )
    return t.union()


if __name__ == '__main__':
    model = generate_model()
    scad_render_to_file(
        model,
        'generated/bonsai.scad',
        include_orig_code=False,
    )
