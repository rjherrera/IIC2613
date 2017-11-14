from sklearn.neighbors import NearestNeighbors
import os

with open('pasillos.txt') as f:
    hallways = [[j[0], [k.lower() for k in j[1].split(',')]] for j in [i.strip().split(':') for i in f.readlines()]]

with open('classifier_files/retrained_labels.txt') as f:
    clases = [i.strip() for i in f]

for i in range(len(hallways)):
    hallways[i].append(list(map(lambda x: 1 if x in hallways[i][1] else 0, clases)))

samples = list(map(lambda x: x[2], hallways))
neighbors = NearestNeighbors(n_neighbors=1)
neighbors.fit(samples)

if __name__ == '__main__':
    entrada = input('Ingrese productos: ').split(',')
    sample = list(map(lambda x: 1 if x in entrada else 0, clases))
    distance, index = neighbors.kneighbors([sample])
    print(hallways[index[0][0]][0])