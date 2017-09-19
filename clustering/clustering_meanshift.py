#!/usr/bin/env python

import sys

# ROOT
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

# LCIO
from pyLCIO.io.LcioReader import LcioReader
from pyLCIO import EVENT
from pyLCIO import UTIL

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph
from sklearn import cluster, datasets, mixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances

from itertools import cycle, islice

####################
maxEvt = 100
skip = 0
quantile = 0.05
shift = 100
####################

if len(sys.argv) == 1:
	fileName = "PDG211_50GeV_endcap_rec_0.slcio"
	print 'default file: ', fileName
else:
	fileName = sys.argv[1]

eventNumber = 1
reader = LcioReader( fileName )
event = None

########################################
# recalc event parameters

# merge two events in one
nevt  = 0
skip = 2 * skip
maxEvt = 2 * maxEvt

# due to the shift in x and y direction
shift = 150 / 1.41
########################################


allHitPos = []

for event in reader:

	if skip > 0 :
		skip = skip - 1
		continue

	nevt = nevt + 1
	if nevt > maxEvt:
		break

	hcalHits = event.getCollection('HCALOther')
	nHit = hcalHits.getNumberOfElements()
	cellIdEncoding = hcalHits.getParameters().getStringVal( EVENT.LCIO.CellIDEncoding )
	idDecoder = UTIL.BitField64( cellIdEncoding )

	for iHit in range(0, nHit) :
		caloHit = hcalHits.getElementAt( iHit )
		pos = caloHit.getPositionVec()
		cellID = long( caloHit.getCellID0() & 0xffffffff ) | ( long( caloHit.getCellID1() ) << 32 )
		idDecoder.setValue( cellID )
		layer = idDecoder['layer'].value()
		shiftx = shifty = 0.

		if nevt%2 == 0:
			shiftx = shifty = shift
			
		allHitPos.append( [pos[0] + shiftx, pos[1] + shifty, pos[2]] )

	### continue to read the next event
	if nevt%2 == 1:
		continue

	########################################################################################################################
	fig = plt.figure()
	#ax = fig.gca(projection='3d')
	ax = fig.add_subplot(111, projection='3d')

	Xdata = StandardScaler().fit_transform(allHitPos)

	######
	"""
	connectivity = kneighbors_graph(Xdata, n_neighbors=2, include_self=False)
	connectivity = 0.5 * (connectivity + connectivity.T)
	ncluster = 10
	average_linkage = cluster.AgglomerativeClustering( linkage="average", affinity="l2", n_clusters=ncluster, connectivity=connectivity )
	average_linkage.fit(Xdata)
	y_pred = average_linkage.labels_.astype(np.int)
	"""
	######

	######
	"""
	dbscan = cluster.DBSCAN(eps=0.8)
	dbscan.fit(Xdata)
	y_pred = dbscan.labels_.astype(np.int)
	"""
	######

	######
	"""
	two_means = cluster.MiniBatchKMeans(n_clusters=2)
	two_means.fit(Xdata)
	y_pred = two_means.labels_.astype(np.int)
	"""
	######

	######
	bandwidth = cluster.estimate_bandwidth(Xdata, quantile=quantile)
	ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
	ms.fit(Xdata)
	y_pred = ms.labels_.astype(np.int)
	######

	colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
										 '#f781bf', '#a65628', '#984ea3',
										 '#999999', '#e41a1c', '#dede00']),
			                              int(max(y_pred) + 1))))

	xPos = [x[0] for x in Xdata]
	yPos = [x[1] for x in Xdata]
	zPos = [x[2] for x in Xdata]

	ax.scatter(xPos, yPos, zPos, c=colors[y_pred], marker='o')

	plt.show()

	text = raw_input('enter to next event: ')
	if text == '':
		#print '...'
		del allHitPos[:]
	else:
		print 'exit'
		break
