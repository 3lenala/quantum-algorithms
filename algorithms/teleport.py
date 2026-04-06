from qiskit import QuantumCircuit
from qiskit import QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

def Bell(qc,q1,q2):
    qc.h(q1) 
    # |q1> = (|0>+|1>)/sqrt(2) & |q2> = |0>
    qc.cx(q1,q2) 
    # |q1,q2> = (|00>+|11>)/sqrt(2)
    return qc

def teleport():
    c = ClassicalRegister(3)
    qreg = QuantumRegister(3)
    # se crea un registro clásico para poder acceder a los valores individuales de los bits
    qc = QuantumCircuit(qreg,c)
    # se crea un circuito con el registro clasico y 3 qubits, para que esten unidos

    qc = Bell(qc,1,2)
    qc.cx(0,1)
    qc.h(0)
    qc.measure([0,1],[0,1])
    #En función del resultado de c0,c1 hay que aplicar una corrección en q0
    with qc.if_test((c[0], 1)):
        qc.z(2)

    with qc.if_test((c[1], 1)):
        qc.x(2)

    qc.measure(2,2)
    return qc

if __name__ == '__main__':
    qc = teleport()
    qc.draw()