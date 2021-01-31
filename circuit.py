#%%
from importlib import reload
import gates as gt
from qiskit import Aer
from qiskit_ionq_provider import IonQProvider 
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.providers.jobstatus import JobStatus
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('PROJECT_API_KEY')

class Circuit:
    def __init__(self, n_qubits=3, API_KEY=API_KEY):
        self._n_qubits = n_qubits
        self._gates = []
        qc = QuantumCircuit(n_qubits, n_qubits)
        for i in range(n_qubits):
            qc.h(i)
        self._circuit = qc
        self.__API_KEY = API_KEY

    def __repr__(self):
        return f"{self.get_n_qubits()}-Qubit Circuit, {len(self.get_gates()) + 3} Gates"

    def get_n_qubits(self):
        return self._n_qubits

    def get_circuit(self):
        return self._circuit

    def draw(self):
        return self.get_circuit().draw()

    def get_gates(self):
        return self._gates

    def apply_gate(self, gate):
        if isinstance(gate, gt.HadamardGate):
            self._circuit.h(gate.get_target())

        elif isinstance(gate, gt.XGate):
            self._circuit.x(gate.get_target())

        elif isinstance(gate, gt.CNOTGate):
            self._circuit.cx(gate.get_control(), gate.get_target())

        elif isinstance(gate, gt.ToffoliGate):
            self._circuit.ccx(gate.get_control()[0], gate.get_control()[1], gate.get_target())

        elif isinstance(gate, gt.SWAPGate):
            self._circuit.swap(gate.get_target()[0], gate.get_target()[1])

        elif isinstance(gate, gt.MeasureGate):
            self._circuit.measure([i for i in range(self.get_n_qubits())], [i for i in range(self.get_n_qubits())])
        
        self._gates.append(gate)
        return self

    def simulate(self):
        provider = IonQProvider(token=self.__API_KEY)
        backend = provider.get_backend("ionq_simulator")
        job = backend.run(self.get_circuit(), shots=100)
        return job.result()

    def run(self):
        provider = IonQProvider(token=self.__API_KEY)
        backend = provider.get_backend("ionq_qpu")
        job = backend.run(self.get_circuit(), shots=1)
        return job.result()
