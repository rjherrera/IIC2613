from argparse import ArgumentParser
from graph import ComputationalGraph
from matplotlib import pyplot as plt
from utils import *
import numpy as np
import os


def parse_dataset_pd(file_name):
    import pandas as pd
    if not os.path.isfile(file_name):
        raise Exception('Please enter an existing file.')
    with open(file_name) as f:
        parameters = [float(i) for i in f.readline().strip().split(',')]
    df = pd.read_csv(file_name, header=None, skiprows=1)
    y = np.array(df.iloc[:,-1], dtype=np.float)
    X = np.array(df.iloc[:,:-1], dtype=np.float)
    return parameters, X, y


def parse_dataset(file_name):
    if not os.path.isfile(file_name):
        raise Exception('Please enter an existing file.')
    with open(file_name) as f:
        parameters = [float(i) for i in f.readline().strip().split(',')]
        data = np.array([[float(i) for i in line.strip().split(',')] for line in f.readlines()])
    return parameters, data[:,:-1], data[:,-1]



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('file_name', help='File with data, as described', nargs='?', default='test.txt')
    parser.add_argument('-plt', '--show_plot', action='store_true', help='Show plots, before and after gradient descent (Only works if 2D)')
    parser.add_argument('-l', '--log_level', default=INFO, help='Select log level to display information (0=Debug, 1=Normal, 2=Essentials)')
    args = parser.parse_args()

    SHOW_PLOT = bool(args.show_plot)
    logger.LOG_LEVEL = int(args.log_level)  # DEBUG, INFO, ERROR

    parameters, X, y = parse_dataset(args.file_name)
    dimensions, _lambda, alpha, mb_size, epochs = parameters

    # w = np.ones(int(dimensions))
    w = np.random.rand(int(dimensions))
    previous_w = [i for i in w]
    # b = 1.
    b = np.random.rand()

    cg = ComputationalGraph()
    result, output_w, output_b = cg.gradient_descent(w, X, y, b, _lambda, alpha, int(mb_size), int(epochs))

    log('\nFinal:', result, level=ERROR)
    # log('\tw: %r\n\tb: %r' % (list(output_w), output_b), level=ERROR)

    log('\n---------- Summary ----------', level=ERROR)
    log('Epochs: %d, MiniBatches: %d, Descents: %d, Final function value: %f' % (
        epochs, mb_size, epochs * mb_size, result), level=ERROR)
    log('---------- Summary ----------', level=ERROR)

    if SHOW_PLOT:
        x_prev = np.linspace(4, 7, 100)
        y_prev = -(previous_w[0] * x_prev + b) / previous_w[1]
        plt.figure(1)
        plt.subplot(211)
        plt.scatter(X[:, 0], X[:, 1], c=y)
        plt.plot(x_prev, y_prev)

        plt.subplot(212)
        x_plot = np.linspace(4, 7, 100)
        y_plot = -(output_w[0] * x_plot + output_b) / output_w[1]
        plt.scatter(X[:, 0], X[:, 1], c=y)
        plt.plot(x_plot, y_plot)
        plt.show()

