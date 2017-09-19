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

n_samples = 1500
noisy_moons = datasets.make_moons(n_samples=n_samples, noise=.05)

#print noisy_moons
print noisy_moons[0][0][0]

n_points = 200


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

plt.figure(1)
plt.clf()

#plt.hist(s)
#colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')

#for x, y in zip(X, Y):
#	plt.plot(x, y, 'ro')

#for i in range(0, n_samples):
#	plt.plot(noisy_moons[0][i][0], noisy_moons[0][i][1], 'ro')

#distance = pairwise_distances(XY)
#print distance[0][1]
#print distance

#model = AgglomerativeClustering(n_clusters=2, linkage="ward", affinity='euclidean')
#model = AgglomerativeClustering(n_clusters=2, linkage="average")
#model.fit(XY)
#fitXY = model.fit_predict(XY)


#Xdata, ydata = noisy_moons
Xdata = XY
Xdata = StandardScaler().fit_transform(Xdata)

#connectivity = kneighbors_graph( Xdata, n_neighbors=params['n_neighbors'], include_self=False)
# make connectivity symmetric
#connectivity = 0.5 * (connectivity + connectivity.T)

#params = default_base.copy()

#connectivity = kneighbors_graph(Xdata, n_neighbors=params['n_neighbors'], include_self=False)
connectivity = kneighbors_graph(Xdata, n_neighbors=10, include_self=False)
## make connectivity symmetric
connectivity = 0.5 * (connectivity + connectivity.T)

######
dbscan = cluster.DBSCAN(eps=0.15)
dbscan.fit(Xdata)
y_pred = dbscan.labels_.astype(np.int)

######
#gmm = mixture.GaussianMixture( n_components=2, covariance_type='full')
#gmm.fit(Xdata)
#y_pred = gmm.predict(Xdata)

######
average_linkage = cluster.AgglomerativeClustering( linkage="average", affinity="cityblock", 
		n_clusters=2, connectivity=connectivity)
average_linkage.fit(Xdata)
y_pred = average_linkage.labels_.astype(np.int)

######
#ward = cluster.AgglomerativeClustering(2, linkage='ward', connectivity=connectivity)
#ward.fit(Xdata)
#y_pred = ward.labels_.astype(np.int)
#y_pred = ward.predict(Xdata)

#colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']), int(max(y_pred) + 1))))

#colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
colors = ['b', 'r', 'c', 'm', 'y', 'k']

#print Xdata
#print '--------->>>>>> ', Xdata[0]

for x, col in zip(Xdata, y_pred) :
	color = colors[col]
	plt.plot( x[0], x[1], color + 'o')

print y_pred

#fitXY = list(fitXY)
#print len(fitXY)
#print '1: ', fitXY.count(1)
#
#print fitXY

#plt.figure()
#plt.axes([0, 0, 1, 1])
#for l in np.arange(model.n_clusters):
#	plt.plot(XY[model.labels_ == l].T)

#plt.axis('tight')
#plt.axis('off')
#plt.suptitle("AgglomerativeClustering(affinity=%s)" % metric, size=20)

#for l, c in zip(np.arange(model.n_clusters), 'rgbk') :
#	plt.plot(XY[model.labels_ == l].T, c=c, alpha=.5)

plt.show()
