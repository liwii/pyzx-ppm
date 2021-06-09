import random
from pyzx.circuit import ZPhase, CZ, CNOT, HAD
from fractions import Fraction

def choose_e(t_rate):
    if random.random() < t_rate:
        return 'T'
    else:
        return 'H' if random.random() >= 0.5 else 'S'

def choose_t():
    return 'CZ' if random.random() >= 0.5 else 'Split'

def generate_block(t_rate=0.05):
    return (choose_e(t_rate), choose_e(t_rate), choose_t())

def block_pattern(width, height, t_rate=0.01):
    blocks = []
    for i in range(height):
        if i % 2 == 0:
            for j in range(0, width - 1, 2):
                blocks.append((j, generate_block(t_rate)))
        else:
            for j in range(1, width - 1, 2):
                blocks.append((j, generate_block(t_rate)))
    return blocks

def add_pattern_to_ppm(pattern, ppm, simple=False):
    i = 0
    for (p, (g1, g2, g3)) in pattern:
        i += 1
        ppm.add_gate(g1, p, simple)
        ppm.add_gate('HSH', p, simple)
        ppm.add_gate('HSH', p + 1, simple)
        ppm.add_gate(g2, p + 1, simple)
        ppm.add_gate(g3, (p, p + 1), simple)
        ppm.add_gate('HSH', p, simple)
        ppm.add_gate('HSH', p + 1, simple)

def add_pattern_to_circuit(pattern, circuit):
    for (p, (g1, g2, g3)) in pattern:
        add_circuit_gate(circuit, g1, p)
        add_circuit_gate(circuit, 'HSH', p)
        add_circuit_gate(circuit, 'HSH', p + 1)
        add_circuit_gate(circuit, g2, p + 1)
        add_circuit_gate(circuit, g3, (p, p + 1))
        add_circuit_gate(circuit, 'HSH', p)
        add_circuit_gate(circuit, 'HSH', p + 1)

def add_circuit_gate(circuit, gate, position):
    if gate == 'HSH':
        circuit.add_gate('XPhase', position, phase=Fraction(1, 2))
    elif gate == 'H':
        circuit.add_gate('HAD', position)
    elif gate == 'S':
        circuit.add_gate('ZPhase', position, phase=Fraction(1, 2))
    elif gate == 'T':
         circuit.add_gate('ZPhase', position, phase=Fraction(1, 4))
    elif gate == 'Split':
        (p1, p2) = position
        circuit.add_gate('ZPhase', p1, phase=Fraction(1, 2))
        circuit.add_gate('ZPhase', p2, phase=Fraction(1, 2))
    elif gate == 'CZ':
        (p1, p2) = position
        circuit.add_gate('CZ', p1, p2)

def add_gate_to_ppm(gate, ppm, simple=False):
    if isinstance(gate, CNOT):
        ppm.add_gate('H', gate.target, simple)
        if gate.control < gate.target:
            ppm.add_gate('CZ', (gate.control, gate.target), simple)
        else:
            ppm.add_gate('CZ', (gate.target, gate.control), simple)
        ppm.add_gate('H', gate.target, simple)

    elif isinstance(gate, CZ):
        if gate.control < gate.target:
            ppm.add_gate('CZ', (gate.control, gate.target), simple)
        else:
            ppm.add_gate('CZ', (gate.target, gate.control), simple)
    elif isinstance(gate, HAD):
        ppm.add_gate('H', gate.target, simple)
    elif isinstance(gate, ZPhase):
        if gate.phase == Fraction(1, 4):
            ppm.add_gate('T', gate.target, simple)
        elif gate.phase == Fraction(1, 2):
            ppm.add_gate('S', gate.target, simple)
        elif gate.phase == Fraction(3, 4):
            ppm.add_gate('T', gate.target, simple)
            ppm.add_gate('S', gate.target, simple)
        elif gate.phase == 1:
            ppm.add_gate('NEGZ', gate.target, simple)
        else:
            ppm.add_gate('NEGZ', gate.target, simple)
            gate.phase -= 1
            add_gate_to_ppm(gate, ppm, simple)
    else:
        raise Exception("Unknown Gate")