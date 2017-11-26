import numpy as np
from utils import *


class Unit:

    def __init__(self, value, grad=None):
        self.value = value
        self.grad = np.zeros(value.shape) if grad is None else grad

    def __repr__(self):
        return 'U(V = %s, G = %s)' % (self.value, self.grad)


class Gate:

    def __init__(self):
        self.x = None
        self.y = None
        self.z = None

    def __repr__(self):
        if 'elements' in self.__dict__:
            return 'G(E = %r, Z = %s)' % (self.elements, self.z)
        return 'G(X = %s, Y = %s, Z = %s)' % (self.x, self.y, self.z)


class AddGate(Gate):

    def forward(self, x, y):
        self.x = x
        self.y = y
        self.x.grad = 0.0
        self.y.grad = 0.0
        self.z = Unit(self.x.value + self.y.value, 0.0)
        return self.z

    def backward(self):
        self.x.grad += 1 * self.z.grad
        self.y.grad += 1 * self.z.grad


class MultiplyGate(Gate):

    def forward(self, x, y):
        self.x = x
        self.y = y
        self.x.grad = 0.0
        self.y.grad = 0.0
        self.z = Unit(self.x.value * self.y.value, 0.0)
        return self.z

    def backward(self):
        self.x.grad += self.y.value * self.z.grad
        self.y.grad += self.x.value * self.z.grad


class MaxGate(Gate):

    def forward(self, x, y):
        self.x = x
        self.y = y
        self.x.grad = 0.0
        self.y.grad = 0.0
        self.z = Unit(max(1 - x.value, y.value), 0.0)
        return self.z

    def backward(self):
        self.x.grad += 0 if self.x.value < 0 else self.x.value * self.z.grad


class DotProductGate(Gate):

    def forward(self, x, y):
        self.x = x
        self.y = y
        self.x.grad = 0.0
        self.y.grad = 0.0
        self.z = Unit(self.x.value.dot(self.y.value), 0.0)
        return self.z

    def backward(self):
        self.x.grad += self.y.value * self.z.grad
        self.y.grad += self.x.value * self.z.grad


class SumGate(Gate):

    def forward(self, *args):
        self.elements = args
        for unit in self.elements:
            unit.grad = 0
            unit.grad = 0
        self.z = Unit(sum(i.value for i in self.elements), 0.0)
        return self.z

    def backward(self):
        for i in self.elements:
            i.grad += self.z.grad



class ComputationalGraph:


    def forward(self, w, X, y, b, _lambda):
        for i in range(len(self.hinge_gates)):
            gh1 = self.hinge_gates[i][0].forward(w, X[i])
            gh2 = self.hinge_gates[i][1].forward(gh1, b)
            gh3 = self.hinge_gates[i][2].forward(gh2, y[i])
            gh4 = self.hinge_gates[i][3].forward(gh3, Unit(0, 0.0))
        # z = Unit(np.array([i[3].z.value for i in self.hinge_gates]))
        # g_sum = self.sum_gate.forward(z, Unit(np.ones(len(self.hinge_gates))))
        g_sum = self.sum_gate.forward(*[i[3].z for i in self.hinge_gates])

        gr1 = self.reg_gates[0].forward(w, w)
        gr2 = self.reg_gates[1].forward(gr1, _lambda)

        return self.final_gate.forward(g_sum, gr2)


    def backward(self, output):
        output.grad = 1.0;
        self.final_gate.backward()
        log('Final gate:', self.final_gate, level=DEBUG)
        self.reg_gates[1].backward()
        self.reg_gates[0].backward()
        log('Reg gate:', self.reg_gates, level=DEBUG)
        self.sum_gate.backward()
        log('Sum gate:', self.sum_gate, level=DEBUG)
        for hinge_gates in self.hinge_gates:
            for gate in hinge_gates[::-1]:
                gate.backward()
                log('Hinge gate %d:' % hinge_gates.index(gate), gate, level=DEBUG)


    def gradient_descent(self, w, X, y, b, _lambda, alpha, mb_size, epochs):
        self.hinge_gates = [[DotProductGate(), AddGate(), MultiplyGate(), MaxGate()] for i in range(mb_size)]
        self.sum_gate = SumGate()
        self.reg_gates = [DotProductGate(), MultiplyGate()]
        self.final_gate = AddGate()

        w = Unit(w)
        X = [Unit(i) for i in X]
        y = [Unit(i, 0.0) for i in y]
        b = Unit(b, 0.0)
        _lambda = Unit(_lambda / 2, 0.0)

        log('Initial:', objective_function(w, b, X, y, _lambda), level=ERROR)
        for i in range(epochs):
            log('Epoch %d:' % (i + 1), level=INFO)
            for j in range(len(X) // mb_size):
                partial_X = X[j * mb_size: (j + 1) * mb_size]
                partial_y = y[j * mb_size: (j + 1) * mb_size]

                s = self.forward(w, partial_X, partial_y, b, _lambda)
                self.backward(s)
                w.value -= alpha * w.grad
                b.value -= alpha * b.grad
                log('\tStep %d:' % (j + 1), level=INFO)
                log('\t\tFx =  %s' % s.value, level=INFO)
                log('\t\tw = %s' % list(w.value), level=INFO)
                log('\t\tb = %s' % b.value, level=INFO)
            log('  FX:', objective_function(w, b, X, y, _lambda), level=INFO)
        return objective_function(w, b, X, y, _lambda), w.value, b.value


def objective_function(w, b, X, y, _lambda):
    reg = w.value.dot(w.value) * _lambda.value
    hinge = sum(max(0, (1 - (y[i].value * (w.value.dot(X[i].value) + b.value)))) for i in range(len(X)))
    return reg + hinge


if __name__ == '__main__':
    w = np.array([1., 1.])
    X = np.array([[1., 1.], [2., 1], [1., 2.], [3., 3.], [3., 4.], [4., 3.]])
    y = np.array([-1., -1., -1., 1., 1., 1.])
    b = 1.
    _lambda = 2
    alpha = 0.01
    mb_size = 2
    epochs = int(1e3)

    logger.LOG_LEVEL = INFO

    cg = ComputationalGraph()

    result, output_w, output_b = cg.gradient_descent(w, X, y, b, _lambda, alpha, mb_size, epochs)

    log('\nFinal:', result, level=ERROR)
    log('\tw: %r\n\tb: %r' % (list(output_w), output_b), level=ERROR)
