#!/usr/bin/env python

from ROOT import TCanvas
from ROOT import TGraph
from ROOT import TGraphErrors
from ROOT import gROOT
from ROOT import TLegend
from ROOT import TFile
from ROOT import TGaxis
from ROOT import gDirectory
from ROOT import gStyle
from ROOT import gPad
from ROOT import TH1F
from ROOT import TF1
from ROOT import TVector3

from pyLCIO.io.LcioReader import LcioReader
from pyLCIO import EVENT
from pyLCIO import UTIL

import matplotlib.pyplot as plt
from itertools import cycle, islice

import sys

#from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph

from sklearn import cluster, datasets, mixture
from scipy.stats import norm
from scipy.stats import uniform
import numpy as np

'''

'''
mu = 0.
sigma = 1

X = []
Y = []
XY = []

n_samples = 100
noisy_moons = datasets.make_moons(n_samples=n_samples, noise=.05)

#print noisy_moons
print noisy_moons[0][0][0]

n_points = 100


for i in range(0, n_points):
	rand = np.random.normal(mu, sigma)
	k = 5.1/3
	x = np.random.uniform(0, 100)
	y = k * x + rand
	X.append( x )
	Y.append( y )
	XY.append( [x, y] ) 

for i in range(0, n_points):
	rand = np.random.normal(mu, sigma)
	k = 5./3
	x = np.random.uniform(0, 100)
	y = k * x + rand + 60.
	X.append( x )
	Y.append( y )
	XY.append( [x, y] ) 

for i in range(0, 100, 2):
	x = np.random.normal(200, 3)
	y = np.random.normal(-200, 5)
	X.append( x )
	Y.append( y )
	XY.append( [x, y] ) 

for i in range(0, 100, 2):
	x = np.random.normal(20, 3)
	y = np.random.normal(-20, 5)
	X.append( x )
	Y.append( y )
	XY.append( [x, y] ) 

plt.figure(1)
plt.clf()

#Xdata, ydata = noisy_moons
Xdata = XY
Xdata = StandardScaler().fit_transform(Xdata)

connectivity = kneighbors_graph(Xdata, n_neighbors=10, include_self=False)
connectivity = 0.5 * (connectivity + connectivity.T)

average_linkage = cluster.AgglomerativeClustering( linkage="average", affinity="cityblock", n_clusters=4, connectivity=connectivity)

average_linkage.fit(Xdata)
y_pred = average_linkage.labels_.astype(np.int)

colors = ['b', 'r', 'c', 'm', 'y', 'k']

for x, col in zip(Xdata, y_pred) :
	color = colors[col]
	plt.plot( x[0], x[1], color + 'o')

print y_pred

plt.show()
