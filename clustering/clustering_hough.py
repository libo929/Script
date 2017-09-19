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
quantile = 0.02
####################

if len(sys.argv) == 1:
	fileName = "PDG211_50GeV_endcap_rec_0.slcio"
	print 'default file: ', fileName
else:
	fileName = sys.argv[1]

eventNumber = 1
reader = LcioReader( fileName )
event = None
nevt = 0

########################################


for event in reader:
	allHitPos = []

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
			
		allHitPos.append( [pos[0], pos[1], pos[2]] )

	########################################################################################################################
	plt.style.use(['seaborn-talk'])

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	Xdata = StandardScaler().fit_transform(allHitPos)

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

	ax.set_xlabel('X (mm)')
	ax.set_ylabel('Y (mm)')
	ax.set_zlabel('Z (mm)')

	ax.scatter(xPos, yPos, zPos, c=colors[y_pred], marker='o')
	plt.show()

	text = raw_input('enter to next event: ')

	if text == '':
		print '...'
	else:
		print 'exit'
		break
