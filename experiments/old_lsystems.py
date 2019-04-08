
def koch_island(d):
    f = Forward(d)
    tp = Turn(90)
    tn = Turn(-90)

    def f_replace(cmd):
        return [f, tn, f, tp, f, tp, f, f, tn, f, tn, f, tp, f]

    axiom = [f, tn, f, tn, f, tn, f]
    productions = [
        (lambda x: isinstance(x, Forward), f_replace),
    ]

    return axiom, productions


def dragon_curve(d):
    f1 = Forward(d, tag=1)
    f2 = Forward(d, tag=2)
    tp = Turn(90)
    tn = Turn(-90)

    def f1_replace(cmd):
        return [f1, tp, f2, tp]

    def f2_replace(cmd):
        return [tn, f1, tn, f2]

    axiom = [f1]
    productions = [
        (lambda x: isinstance(x, Forward) and x.tag == 1, f1_replace),
        (lambda x: isinstance(x, Forward) and x.tag == 2, f2_replace),
    ]

    return axiom, productions

def bushy_tree(d):
    f = Forward(d)
    tp = Turn(22.5)
    tn = Turn(-22.5)
    push = Push()
    pop = Pop()

    def f_replace(cmd):
        return [f, f, tn, push, tn, f, tp, f, tp, f, pop, tp, push, tp, f, tn, f, tn, f, pop]

    axiom = [f]
    productions = [
        (lambda x: isinstance(x, Forward), f_replace),
    ]

    return axiom, productions


def flower_field(d):
    f = Forward(d)
    tp = Turn(30)
    tn = Turn(-30)
    push = Push()
    pop = Pop()

    def f_replace(cmd):
        a, b, c = uniform_probability(random, 0.33, 0.33, 0.34)
        if a:
            return [f, push, tp, f, pop, f, push, tn, f, pop, f]
        elif b:
            return [f, push, tp, f, pop, f]
        elif c:
            return [f, push, tn, f, pop, f]
        else:
            assert False

    axiom = [f]
    productions = [
        (lambda x: isinstance(x, Forward), f_replace),
    ]

    return axiom, productions


def triangle_koch(d):
    c = 1
    p = 0.3
    q = c - p
    h = (p * q)**0.5

    tp = Turn(86)
    tn = Turn(-86)

    def f_replace(cmd):
        x = cmd.distance
        return [Forward(x * p), tp, Forward(x * h), tn, tn, Forward(x * h), tp, Forward(x * q)]

    axiom = [Forward(d)]
    productions = [
        (lambda x: isinstance(x, Forward), f_replace),
    ]

    return axiom, productions


