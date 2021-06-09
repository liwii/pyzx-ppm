from ppm import *
from util import *
import matplotlib.pyplot as plt
import numpy as np
from pyzx import Circuit
import pyzx as zx

trates = np.linspace(0, 0.15, 6)

hs = [20, 200]

lanes = 6

for h in hs:
    heights = [[] for _ in range(4)]
    qubits = [[] for _ in range(4)]
    long_edges = [[] for _ in range(4)]
    tcounts = [[] for _ in range(4)]
    circuit_gates = [[] for _ in range(4)]

    for tr in trates:
        height = np.zeros(4)
        qubit = np.zeros(4)
        long_edge = np.zeros(4)
        tcount = np.zeros(4)
        circuit_gate = np.zeros(2)
        epochs = 4
        for _ in range(epochs):
            pattern = block_pattern(lanes, h, tr)

            ppm = PPM(lanes)
            add_pattern_to_ppm(pattern, ppm)
            height[0] += ppm.height()
            qubit[0] += ppm.qubits()
            long_edge[0] += ppm.long_edges()
            tcount[0] += ppm.tcount

            ppm_simple = PPM(lanes)
            add_pattern_to_ppm(pattern, ppm_simple, True)
            height[1] += ppm_simple.height()
            qubit[1] += ppm_simple.qubits()
            long_edge[1] += ppm_simple.long_edges()
            tcount[1] += ppm_simple.tcount


            circuit = Circuit(lanes)

            add_pattern_to_circuit(pattern, circuit)

            circuit_gate[0] += len(circuit.gates)
            graph = circuit.to_graph()
            zx.simplify.full_reduce(graph)
            c2 = zx.extract_circuit(graph).to_basic_gates()
            circuit_gate[1] += len(c2.gates)

            ppm_result = PPM(lanes)
            for g in c2.gates:
                add_gate_to_ppm(g, ppm_result)
            height[2] += ppm_result.height()
            qubit[2] += ppm_result.qubits()
            long_edge[2] += ppm_result.long_edges()
            tcount[2] += ppm_result.tcount

            ppm_result_simple = PPM(lanes)
            for g in c2.gates:
                add_gate_to_ppm(g, ppm_result_simple, True)
            height[3] += ppm_result_simple.height()
            qubit[3] += ppm_result_simple.qubits()
            long_edge[3] += ppm_result_simple.long_edges()
            tcount[3] += ppm_result_simple.tcount

        height /= epochs
        qubit /= epochs
        long_edge /= epochs
        tcount /= epochs
        circuit_gate /= epochs

        for i in range(4):
            heights[i].append(height[i])
            qubits[i].append(qubit[i])
            long_edges[i].append(long_edge[i])
            tcounts[i].append(tcount[i])
            if i < 2:
                circuit_gates[i].append(circuit_gate[i])

    labels = ["Original Circuit", "Reduced Circuit"]
    plt.figure()
    plt.title("Circuit Size")
    for i in range(2):
        plt.plot(trates, circuit_gates[i],label=labels[i])
    plt.ylabel("Gates")
    plt.xlabel("T-Rate")
    plt.legend()
    plt.savefig(f"circuit-gate-{h}.png")

    labels = ["Original", "Original (Simple)", "Optimized", "Optimized (Simple)"]

    plt.figure()
    plt.title("Height")
    for i in range(4):
        plt.plot(trates, heights[i],label=labels[i])
    plt.ylabel("Height")
    plt.xlabel("T-Rate")
    plt.legend()
    plt.savefig(f"height-{h}.png")

    plt.figure()
    plt.title("Qubit")
    for i in range(4):
        plt.plot(trates, qubits[i],label=labels[i])
    plt.ylabel("Qubit")
    plt.xlabel("T-Rate")
    plt.legend()
    plt.savefig(f"qubit-{h}.png")

    plt.figure()
    plt.title("Long Edge")
    for i in range(4):
        plt.plot(trates, long_edges[i],label=labels[i])
    plt.ylabel("Long Edge")
    plt.xlabel("T-Rate")
    plt.legend()
    plt.savefig(f"long-edge-{h}.png")

    plt.figure()
    plt.title("T-Count")
    for i in range(4):
        plt.plot(trates, tcounts[i],label=labels[i])
    plt.ylabel("T-Count")
    plt.xlabel("T-Rate")
    plt.legend()
    plt.savefig(f"t-count-{h}.png")

