#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import mean_shift as ms
from numpy import genfromtxt

from itertools import cycle, islice

def load_points(filename):
    data = genfromtxt(filename, delimiter=',')
    return data

def run_meanshift():
    reference_points = load_points("data.csv")
    mean_shifter = ms.MeanShift()
    mean_shift_result = mean_shifter.cluster(reference_points, kernel_bandwidth = 1)

    return mean_shift_result
    
##########################################

if __name__ == '__main__':
    result = run_meanshift()

    px = []
    py = []
    cluID = []

    for i in range(len(result.shifted_points)):
        original_point = result.original_points[i]
        cluster_assignment = result.cluster_ids[i]
        #print "(%5.2f,%5.2f)  ->  cluster %i" % (original_point[0], original_point[1], cluster_assignment)

        px.append(original_point[0])
        py.append(original_point[1])
        cluID.append(cluster_assignment)

    colors = ['b', 'r', 'c', 'm', 'y', 'k', 'y', 'b', 'c', 'm', 'r', 'y']

    fig, ax = plt.subplots()

    for x, y, col in zip(px, py, cluID) :
        color = colors[col]
        #print color
        plt.plot(x, y, color + 'o')

    ax.set_xlabel(r'x', fontsize=15)
    ax.set_ylabel(r'y', fontsize=15)
    ax.set_title('')
    ax.grid(True)
    fig.tight_layout()
    plt.show()
