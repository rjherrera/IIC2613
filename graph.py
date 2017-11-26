import numpy as np


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


class ComputationalGraph:


    def forward(self, w, X, y, b, _lambda):
        for i in range(len(self.hinge_gates)):
            gh1 = self.hinge_gates[i][0].forward(w, X[i])
            gh2 = self.hinge_gates[i][1].forward(gh1, b)
            gh3 = self.hinge_gates[i][2].forward(gh2, y[i])
            gh4 = self.hinge_gates[i][3].forward(gh3, Unit(0, 0.0))
        z = Unit(np.array([i[3].z.value for i in self.hinge_gates]))
        g_sum = self.sum_gate.forward(z, Unit(np.ones(len(self.hinge_gates))))

        gr1 = self.reg_gates[0].forward(w, w)
        gr2 = self.reg_gates[1].forward(gr1, _lambda)

        return self.final_gate.forward(g_sum, gr2)


    def backward(self, output):
        output.grad = 1.0;
        self.final_gate.backward()
        # print(final_gate)
        self.reg_gates[1].backward()
        self.reg_gates[0].backward()
        # print(*reg_gates, sep='\t\t')
        self.sum_gate.backward()
        # print(sum_gate)
        for hinge_gates in self.hinge_gates:
            for gate in hinge_gates[::-1]:
                gate.backward()


    def gradient_descent(self, w, X, y, b, _lambda, alpha, mb_size, epochs):
        self.hinge_gates = [[DotProductGate(), AddGate(), MultiplyGate(), MaxGate()] for i in range(mb_size)]
        self.sum_gate = DotProductGate()
        self.reg_gates = [DotProductGate(), MultiplyGate()]
        self.final_gate = AddGate()

        w = Unit(w)
        X = [Unit(i) for i in X]
        y = [Unit(i, 0.0) for i in y]
        b = Unit(b, 0.0)
        _lambda = Unit(_lambda / 2, 0.0)

        print('FX before:', objective_function(w, b, X, y, _lambda))
        for i in range(epochs):
            print('Epoch %d:' % (i + 1))
            for j in range(len(X) // mb_size):
                partial_X = X[j * mb_size: (j + 1) * mb_size]
                partial_y = y[j * mb_size: (j + 1) * mb_size]

                s = self.forward(w, partial_X, partial_y, b, _lambda)
                self.backward(s)
                w.value -= alpha * w.grad
                b.value -= alpha * b.grad
                print('\tStep %d:' % (j + 1))
                print('\t\tFx =  %s' % s.value)

                print('\t\tw = %s' % list(w.value))
                # print(X)
                print('\t\tb = %s' % b.value)
            print('  FX:', objective_function(w, b, X, y, _lambda))


def objective_function(w, b, X, y, _lambda):
    reg = w.value.dot(w.value) * _lambda.value / 2
    hinge = sum(max(0, (1 - (y[i].value * (w.value.dot(X[i].value) + b.value)))) for i in range(len(X)))
    return reg + hinge


if __name__ == '__main__':
    w = np.array([1., 1.])
    X = np.array([[1., 1.], [2., 1], [1., 2.], [3., 3.], [3., 4.], [4., 3.]])
    y = np.array([-1., -1., -1., 1, 1, 1])
    b = 1
    _lambda = 2
    alpha = 0.01
    mb_size = 2
    epochs = 100

    cg = ComputationalGraph()

    cg.gradient_descent(w, X, y, b, _lambda, alpha, mb_size, epochs)
