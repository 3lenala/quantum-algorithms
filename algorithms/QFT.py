from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def QFT(qc):
    number_qubits = qc.num_qubits
    for qubit in range(number_qubits):
        qc.h(qubit)
        for higher_qubit in range(qubit+1, number_qubits):
            qc.cp(np.pi/2**(higher_qubit-qubit),higher_qubit,qubit)
    for qubit in range(number_qubits//2):
        qc.swap(number_qubits, number_qubits-number_qubits-1)
    
    qc.save_statevector()
    return qc

if __name__ == '__main__':
    qc = QuantumCircuit(4)
    qc = QFT(qc)
    qc.draw()
