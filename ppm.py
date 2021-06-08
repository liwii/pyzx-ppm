from dataclasses import dataclass
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

@dataclass
class Output:
    p: Tuple[int, int]
    x_error: str
    z_error: str

@dataclass
class Edge:
    p1: Tuple[int, int]
    p2: Tuple[int, int]
    double: bool

@dataclass
class Measurement:
    p: Tuple[int, int]
    var: str
    basis: str


class VarStore:
    def __init__(self):
        self.num = -1

    def create_var(self):
        self.num += 1
        return 'a' + str(self.num)

class PPM:
    def __init__(self, bits=6):
        self.bits=bits
        self.outputs = [Output((2 * i, 0), '0', '0') for i in range(bits)]
        self.measurements = [[] for _ in range(bits * 2)]
        self.edges = []
        self.store = VarStore()


    def add_gate(self, gate, position):
        if gate == 'T':
            (x, y) = self.outputs[position].p
            (x, y) = self.extend(position, x, y)
            a = self.store.create_var()
            b = self.store.create_var()
            c = self.store.create_var()
            d = self.store.create_var()
            e = self.store.create_var()
            self.measurements[x].append(Measurement((x, y), a, '0'))
            self.edges.append(Edge((x, y), (x + 1, y), False))
            self.measurements[x + 1].append(Measurement((x + 1, y), b, '1'))
            self.edges.append(Edge((x, y), (x, y + 1), True))
            self.measurements[x].append(Measurement((x, y + 1), c, '0'))
            self.edges.append(Edge((x, y + 1), (x + 1, y + 1), True))
            self.measurements[x + 1].append(Measurement((x + 1, y + 1), d, '0'))
            self.edges.append(Edge((x, y + 1), (x, y + 2), True))
            self.edges.append(Edge((x, y + 2), (x + 1, y + 2), True))
            self.measurements[x + 1].append(Measurement((x + 1, y + 2), e, f"{b} + {x}"))

            self.outputs[position].p = (x, y + 2)
            z_error = self.outputs[position].z_error
            x_error = self.outputs[position].x_error
            self.outputs[position].z_error = f"{a} + {c} + {d} + {e} + {x_error} + ({b} + {z_error})({c} + {d} + {z_error} + 1)"
            self.outputs[position].x_error = f"{c} + {d} + {z_error} + 1"

        elif gate == 'S':
            (x, y) = self.outputs[position].p
            (x, y) = self.extend(position, x, y)
            a = self.store.create_var()
            b = self.store.create_var()
            c = self.store.create_var()
            d = self.store.create_var()
            e = self.store.create_var()

            self.measurements[x].append(Measurement((x, y), a, '0'))
            self.edges.append(Edge((x, y), (x + 1, y), False))
            self.measurements[x + 1].append(Measurement((x + 1, y), b, '0'))
            self.edges.append(Edge((x, y), (x, y + 1), True))
            self.measurements[x].append(Measurement((x, y + 1), c, '0'))
            self.edges.append(Edge((x, y + 1), (x + 1, y + 1), True))
            self.measurements[x + 1].append(Measurement((x + 1, y + 1), d, '0'))
            self.edges.append(Edge((x, y + 1), (x, y + 2), True))
            self.edges.append(Edge((x, y + 2), (x + 1, y + 2), True))
            self.measurements[x + 1].append(Measurement((x + 1, y + 2), e, "1"))

            self.outputs[position].p = (x, y + 2)
            z_error = self.outputs[position].z_error
            x_error = self.outputs[position].x_error
            self.outputs[position].z_error = f"{a} + {b} + {e} + {x_error} + {z_error} + 1"
            self.outputs[position].x_error = f"{c} + {d} + {x_error} + 1"
        elif gate == 'H':
            (x, y) = self.outputs[position].p
            (x, y) = self.extend(position, x, y)
            a = self.store.create_var()
            b = self.store.create_var()
            c = self.store.create_var()
            d = self.store.create_var()
            e = self.store.create_var()

            self.measurements[x].append(Measurement((x, y), a, '0'))
            self.edges.append(Edge((x, y), (x + 1, y), False))
            self.measurements[x + 1].append(Measurement((x + 1, y), b, '0'))
            self.edges.append(Edge((x, y), (x, y + 1), True))
            self.measurements[x].append(Measurement((x, y + 1), c, '0'))
            self.edges.append(Edge((x, y + 1), (x + 1, y + 1), True))
            self.measurements[x + 1].append(Measurement((x + 1, y + 1), d, '1'))
            self.edges.append(Edge((x, y + 1), (x, y + 2), True))
            self.edges.append(Edge((x, y + 2), (x + 1, y + 2), True))
            self.measurements[x + 1].append(Measurement((x + 1, y + 2), e, "0"))

            self.outputs[position].p = (x, y + 2)
            z_error = self.outputs[position].z_error
            x_error = self.outputs[position].x_error
            self.outputs[position].z_error = f"{c} + {d} + {e} + {x_error} + 1"
            self.outputs[position].x_error = f"{a} + {b} + {c} + {d} + {z_error} + 1"
        elif gate == 'HSH':
            (x, y) = self.outputs[position].p
            a = self.store.create_var()
            self.measurements[x].append(Measurement((x, y), a, '0'))
            self.edges.append(Edge((x, y), (x, y + 1), True))
            self.outputs[position].p = (x, y + 1)
            z_error = self.outputs[position].z_error
            x_error = self.outputs[position].x_error
            self.outputs[position].z_error = f"{z_error} + {a}"
            self.outputs[position].x_error = f"{z_error} + {a} + {x_error} + 1"
        elif gate == 'Split':
            (p1, p2) = position
            (x1, y1) = self.outputs[p1].p
            (x1, y1) = self.extend(p1, x1, y1)
            ((x1, y1), (x2, y2)) = self.match_head(p1, p2)
            a = self.store.create_var()
            b = self.store.create_var()
            self.measurements[x1 + 1].append(Measurement((x1 + 1, y1), b, '1'))
            self.measurements[x1 + 1].append(Measurement((x1 + 1, y1 + 1), a, '0'))

            self.edges.append(Edge((x1, y1), (x1 + 1, y1), True))
            self.edges.append(Edge((x1 + 1, y1), (x1 + 1, y1 + 1), True))
            self.edges.append(Edge((x1 + 1, y1), (x2, y2), True))

            z1_error = self.outputs[p1].z_error
            x1_error = self.outputs[p1].x_error
            z2_error = self.outputs[p2].z_error
            x2_error = self.outputs[p2].x_error

            self.outputs[p1].z_error = f"{z1_error} + {x1_error} + {b}"
            self.outputs[p2].z_error = f"{z2_error} + {x2_error} + {b}"

        elif gate == 'CZ':
            (p1, p2) = position
            (x1, y1) = self.outputs[p1].p
            (x1, y1) = self.extend(p1, x1, y1)
            ((x1, y1), (x2, y2)) = self.match_head(p1, p2)
            a = self.store.create_var()
            b = self.store.create_var()
            self.measurements[x1 + 1].append(Measurement((x1 + 1, y1), b, '0'))
            self.measurements[x1 + 1].append(Measurement((x1 + 1, y1 + 1), a, '1'))

            self.edges.append(Edge((x1, y1), (x1 + 1, y1), True))
            self.edges.append(Edge((x1 + 1, y1), (x1 + 1, y1 + 1), True))
            self.edges.append(Edge((x1 + 1, y1), (x2, y2), True))

            z1_error = self.outputs[p1].z_error
            x1_error = self.outputs[p1].x_error
            z2_error = self.outputs[p2].z_error
            x2_error = self.outputs[p2].x_error

            self.outputs[p1].z_error = f"{z1_error} + {x2_error} + {a} + {b} + 1"
            self.outputs[p2].z_error = f"{z2_error} + {x1_error} + {a} + {b} + 1"

    def match_head(self, p1, p2):
        (x1, y1) = self.outputs[p1].p
        (x2, y2) = self.outputs[p2].p
        if y1 == y2:
            return ((x1, y1), (x2, y2))
        elif abs(y1 - y2) == 1:
            if y1 < y2:
                self.ignore(p1, length=3)
                self.ignore(p2, length=2)
            else:
                self.ignore(p1, length=2)
                self.ignore(p2, length=3)
        else:
            if y1 < y2:
                self.ignore(p1, length=(y2 - y1))
            else:
                self.ignore(p2, length=(y1 - y2))
        (x1, y1) = self.outputs[p1].p
        (x2, y2) = self.outputs[p2].p
        return ((x1, y1), (x2, y2))


    def extend(self, position, x, y):
        if len(self.measurements[x + 1]) > 0 and self.measurements[x + 1][-1].p[1] >= y:
            self.ignore(position)
            (x, y) = self.outputs[position].p
        return (x, y)

    def ignore(self, position, length=2):
        (x, y) = self.outputs[position].p
        length1 = length / 2
        (x, y) = self.outputs[position].p
        a = self.store.create_var()
        b = self.store.create_var()
        self.measurements[x].append(Measurement((x, y), a, '0'))
        self.edges.append(Edge((x, y), (x, y + length1), True))
        self.measurements[x].append(Measurement((x, y + length1), b, '0'))
        self.edges.append(Edge((x, y + length1), (x, y + length), True))

        self.outputs[position].p = (x, y + length)
        self.outputs[position].z_error += f" + {a} + {b}"
        self.outputs[position].x_error = f" + {b} + 1"

    def stats(self):
        pass

    def draw(self, filename):
        width = (2 * self.bits - 1)
        measurements_flat = [m for ms in self.measurements for m in ms]
        height = max([m.p[1] for m in measurements_flat])

        margin = 0.5
        plt.figure(figsize = (width + margin * 2, height + margin * 2))
        plt.xlim(-margin, width + margin)
        plt.ylim(-margin, height + margin)

        epsilon = 0.2
        for e in self.edges:
            color = 'black' if e.double else 'red'
            (x1, y1) = e.p1
            (x2, y2) = e.p2
            if x1 == x2:
                if abs(y1 - y2) == 1:
                    plt.plot([x1, x2], [y1, y2], color=color)
                else:
                    pass
                    y_mid = (y1 + y2) / 2
                    plt.plot([x1, x1 + epsilon], [y1, y_mid], color=color)
                    plt.plot([x1 + epsilon, x2], [y_mid, y2], color=color)
            else:
                if abs(x1 - x2) == 1:
                    plt.plot([x1, x2], [y1, y2], color=color)
                else:
                    pass
                    x_mid = (x1 + x2) / 2
                    plt.plot([x1, x_mid], [y1, y1 + epsilon], color=color)
                    plt.plot([x_mid, x2], [y1 + epsilon, y2], color=color)

        points_x = [m.p[0] for m in measurements_flat] + [o.p[0] for o in self.outputs]
        points_y = [m.p[1] for m in measurements_flat] + [o.p[1] for o in self.outputs]
        measurement_pattern = [f"{m.var} <- {m.basis}" for m in measurements_flat]
        plt.scatter(points_x, points_y, s=100)
        for i in range(len(measurements_flat)):
            plt.text(points_x[i], points_y[i], measurement_pattern[i])

        plt.axis('off')
        plt.savefig(filename)


