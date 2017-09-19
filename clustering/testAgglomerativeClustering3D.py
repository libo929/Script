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
from mpl_toolkits.mplot3d import Axes3D

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
sigma = 0.5

X = []
Y = []
XY = []
XYZ = []

#n_samples = 50
#noisy_moons = datasets.make_moons(n_samples=n_samples, noise=.05)

#######
#random_state = 170
#X1, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state)
#transformation = [[0.6, -0.6], [-0.4, 0.8]]
#X_aniso = np.dot(X1, transformation)
#aniso = (X_aniso, y)
#
#X2, y2 = aniso

#print noisy_moons
#print noisy_moons[0][0][0]

n_points = 50

for i in range(0, n_points):
	rand = np.random.normal(mu, sigma)
	k = 5.1/3
	x = np.random.uniform(0, 100)
	x = i
	y = k * x + rand
	z = 1.2 * k * x + np.random.normal(mu, sigma)
	X.append( x )
	Y.append( y )
	XY.append( [x, y] ) 
	XYZ.append( [x, y, z] )

for i in range(0, n_points):
	rand = np.random.normal(mu, sigma)
	k = 5./3
	x = np.random.uniform(0, 100)
	x = i
	y = k * x + rand + 10.
	z = 1.5 * k * x + np.random.normal(mu, sigma)
	X.append( x )
	Y.append( y )
	XY.append( [x, y] ) 
	XYZ.append( [x, y, z] )

#for i in range(0, 100, 2):
#	x = np.random.normal(200, 3)
#	y = np.random.normal(-200, 5)
#	X.append( x )
#	Y.append( y )
#	XY.append( [x, y] ) 
#
#for i in range(0, 100, 2):
#	x = np.random.normal(20, 3)
#	y = np.random.normal(-20, 5)
#	X.append( x )
#	Y.append( y )
#	XY.append( [x, y] ) 

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#plt.clf()

#Xdata, ydata = noisy_moons
Xdata = XYZ
Xdata = StandardScaler().fit_transform(Xdata)

#connectivity = kneighbors_graph(Xdata, n_neighbors=1, include_self=False)
#connectivity = 0.5 * (connectivity + connectivity.T)

connectivity = kneighbors_graph(Xdata, n_neighbors=2, include_self=False)
connectivity = 0.5 * (connectivity + connectivity.T)

ncluster = 2
#average_linkage = cluster.AgglomerativeClustering( linkage="average", affinity="cityblock", n_clusters=ncluster, connectivity=connectivity)
#average_linkage = cluster.AgglomerativeClustering( linkage="average", affinity="euclidean", n_clusters=ncluster, connectivity=connectivity)
average_linkage = cluster.AgglomerativeClustering( linkage="average", affinity="l2", n_clusters=ncluster, connectivity=connectivity)
#average_linkage = cluster.AgglomerativeClustering( linkage="complete", affinity="euclidean", n_clusters=ncluster, connectivity=connectivity)

average_linkage.fit(Xdata)
y_pred = average_linkage.labels_.astype(np.int)

#spectral = cluster.SpectralClustering( n_clusters=3, eigen_solver='arpack',
#		affinity="nearest_neighbors", n_neighbors=19 )
#spectral.fit(X2)

#Xdata = X2
#y_pred = spectral.labels_.astype(np.int)

#y_pred = spectral.predict(aniso)
#y_pred = spectral.predict(Xdata)

#colors = ['b', 'r', 'c', 'm', 'y', 'k']

colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
									 '#f781bf', '#a65628', '#984ea3',
									 '#999999', '#e41a1c', '#dede00']),
                                      int(max(y_pred) + 1))))

#print Xdata
xPos = [x[0] for x in Xdata]
yPos = [x[1] for x in Xdata]
zPos = [x[2] for x in Xdata]

#for x, col in zip(Xdata, y_pred) :
#	color = colors[col]
#	#plt.plot( x[0], x[1], x[2], color + 'o')
#	plt.plot( x[0], x[1], color + 'o')

#print xPos
#print yPos
#print zPos

ax.scatter(xPos, yPos, zPos, c=colors[y_pred], marker='o')
#ax.scatter(xPos, yPos, 0, c=colors[y_pred], marker='o')

print y_pred

plt.show()
