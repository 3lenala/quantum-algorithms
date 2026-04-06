from qiskit.circuit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile

NUM_INPUT_QUBITS = 4
TOTAL_STATES = 2**NUM_INPUT_QUBITS
SHOTS = 1
TARGET = NUM_INPUT_QUBITS
CONTROLS = list(range(NUM_INPUT_QUBITS))
OUTPUT_FILE = 'oracle.txt'

def oracle(qc: QuantumCircuit) -> None:
    """Apply the oracle to a circuit whose input qubits encode a computational basis state.

    The target qubit is flipped to |1> if and only if the encoded input state is one of
    the marked states.

    Qiskit uses little-endian ordering, where q0 is the least significant bit.
    The marked states in this exercise are written in big-endian order, so the
    qubit order is reversed using swaps to match that representation
    """
  
    qc.swap(0, 3)
    qc.swap(1, 2)

    qc.x(0)
    qc.mcx(CONTROLS, TARGET)

    qc.x(2)
    qc.mcx(CONTROLS, TARGET)
    qc.x(0)
    qc.x(2)

    qc.x(3)
    qc.mcx(CONTROLS, TARGET)
    qc.x(3)



def evaluate_oracle(qc: QuantumCircuit) -> int:
    """Measure the target qubit, simulate the circuit, and return the measured bit."""
    qc.measure(TARGET, 0)

    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled, shots=SHOTS).result()
    counts = result.get_counts()
    measured_bit = max(counts, key=counts.get)
    return int(measured_bit)

if __name__ == '__main__':
    # Check that only the marked basis states produce output 1
    with open(OUTPUT_FILE, 'w') as output_file:
        for state in range(TOTAL_STATES):
            qc = QuantumCircuit(NUM_INPUT_QUBITS + 1, 1)
            # Prepare each computational basis state on the input qubits
            for k in range(NUM_INPUT_QUBITS):
                if (state >> k) & 1:
                    qc.x(k)

            oracle(qc)
            result = evaluate_oracle(qc)
            output_file.write(f'{state:0{NUM_INPUT_QUBITS}b}: {result}\n')
