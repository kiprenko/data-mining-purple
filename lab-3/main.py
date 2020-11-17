import math
import sys
from random import randint
from random import seed

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm

seed(1)


def load_dataset(file_name):
    return pd.read_csv(file_name, header=None, delim_whitespace=True, names=['x', 'y'])


def generate_centers(_data_set, _clusters_count):
    _centers = []
    for _i in range(_clusters_count):
        min_x = _data_set['x'].min()
        max_x = _data_set['x'].max()
        min_y = _data_set['y'].min()
        max_y = _data_set['y'].max()
        _centers.append((randint(min_x, max_x), randint(min_y, max_y)))
    return _centers


def euclidean_range(_x, _y, _center):
    return math.sqrt((_x - _center[0]) ** 2 + (_y - _center[1]) ** 2)


def calculate_centers(_clusters):
    _centers = []
    for _cluster in _clusters:
        xs = 0
        xy = 0
        for dot in _cluster:
            xs += dot[0]
            xy += dot[1]
        _dots_count = len(_cluster)
        _centers.append((xs / _dots_count, xy / _dots_count))
    return _centers


def spread_dots_bw_clusters(_data_set, _centers, _clusters):
    for _index, _row in _data_set.iterrows():
        _x = _row['x']
        _y = _row['y']
        _dists_to_centers = []
        for _center in _centers:
            _dists_to_centers.append(euclidean_range(_x, _y, _center))
            _clusters[_dists_to_centers.index(min(_dists_to_centers))].append((_x, _y))


def draw_plot(_clusters, _colors, _centers):
    for _i, _cluster in enumerate(_clusters):
        plt.scatter([_dot[0] for _dot in _cluster], [_dot[1] for _dot in _cluster], color=_colors[_i])
    for _center in _centers:
        plt.scatter(_center[0], _center[1], c='black', s=30)
    plt.show()


def main():
    clusters_count = int(sys.argv[1])
    data_set_file_name = sys.argv[2]
    colors = cm.rainbow(np.linspace(0, 1, clusters_count))
    data_set = load_dataset(data_set_file_name)
    centers = generate_centers(data_set, clusters_count)
    clusters = [[] for _ in range(clusters_count)]
    spread_dots_bw_clusters(data_set, centers, clusters)
    draw_plot(clusters, colors, centers)
    i = 0
    while True:
        previous_centers = centers.copy()
        centers = calculate_centers(clusters)
        print(f'Current step {i}, Centers are {centers}.')
        i += 1
        if previous_centers == centers:
            print(f'Program used {i} step(-s) to finish.')
            break
        clusters = [[] for _ in range(clusters_count)]
        spread_dots_bw_clusters(data_set, centers, clusters)
    draw_plot(clusters, colors, centers)


if __name__ == '__main__':
    main()
