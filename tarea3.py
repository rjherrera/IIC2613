from argparse import ArgumentParser
from graph import ComputationalGraph
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
    args = parser.parse_args()

    parameters, X, y = parse_dataset(args.file_name)
    dimensions, _lambda, alpha, mb_size, epochs = parameters

    w = np.ones(int(dimensions))
    b = 1.

    cg = ComputationalGraph()
    cg.gradient_descent(w, X, y, b, _lambda, alpha, int(mb_size), int(epochs))

