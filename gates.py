import qiskit
import os

class Gate:
    def __init__(self, type):
        self._type = type

    def get_type(self):
        return self._type

    def __repr__(self):
        return f"{self.get_type()} Gate"

class OneQubitGate(Gate):
    def __init__(self, type, target):
        self._target = target
        Gate.__init__(self, type)

    def get_target(self):
        return self._target

    def __repr__(self):
        return f"{self.get_type()} Gate, Target = {self.get_target()}"
    

class TwoQubitGate(Gate):
    def __init__(self, type, control, target):
        self._target = target
        self._control = control
        Gate.__init__(self, type)

    def get_target(self):
        return self._target

    def get_control(self):
        return self._control

    def __repr__(self):
        return f"{self.get_type()} Gate, Control = {self.get_control()} Target = {self.get_target()}"

class ThreeQubitGate(Gate):
    def __init__(self, type, control, target):
        self._target = target
        self._control = control
        Gate.__init__(self, type)

    def get_target(self):
        return self._target

    def get_control(self):
        return self._control

    def __repr__(self):
        return f"{self.get_type()} Gate, Control = {self.get_control()} Target = {self.get_target()}"

class MeasureGate(Gate):
    def __init__(self):
        Gate.__init__(self, "Measure") 

class HadamardGate(OneQubitGate):
    def __init__(self, target):
        OneQubitGate.__init__(self, "Hadamard", target)

class XGate(OneQubitGate):
    def __init__(self, target):
        OneQubitGate.__init__(self, "X", target)

class CNOTGate(TwoQubitGate):
    def __init__(self, control, target):
        TwoQubitGate.__init__(self, "X", control, target)

class ToffoliGate(ThreeQubitGate):
    def __init__(self, control, target):
        ThreeQubitGate.__init__(self, "Toffoli", control, target)

class SWAPGate(TwoQubitGate):
    def __init__(self, target):
        TwoQubitGate.__init__(self, "SWAP", None, target)
    