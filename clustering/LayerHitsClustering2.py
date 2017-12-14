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

from itertools import cycle

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph
from sklearn import cluster, datasets, mixture

import sys

#from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
import numpy as np
from itertools import cycle, islice

'''

'''
if len(sys.argv) == 1:
	fileName = "PDG211_50GeV_endcap_rec_0.slcio"
	print 'default file: ', fileName
else:
	fileName = sys.argv[1]

eventNumber = 1

#print fileName
reader = LcioReader( fileName )
    
event = None
nevt  = 0

maxEvt = 1

for event in reader:
	hcalHits = event.getCollection('HCALBarrel')
	nHit = hcalHits.getNumberOfElements()
	cellIdEncoding = hcalHits.getParameters().getStringVal( EVENT.LCIO.CellIDEncoding )
	idDecoder = UTIL.BitField64( cellIdEncoding )

	nevt = nevt + 1
	if nevt > maxEvt:
		break

	allHitPos = []
	
	for iHit in range(0, nHit) :
		caloHit = hcalHits.getElementAt( iHit )
		pos = caloHit.getPositionVec()
		cellID = long( caloHit.getCellID0() & 0xffffffff ) | ( long( caloHit.getCellID1() ) << 32 )
		idDecoder.setValue( cellID )
		layer = idDecoder['S-1'].value()
		allHitPos.append( [pos[0], pos[1], pos[2]] )

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
	ncluster = 5
	Xdata = allHitPos

	#average_linkage.fit(Xdata)
	#y_pred = average_linkage.labels_.astype(np.int)
	#colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
	#									 '#f781bf', '#a65628', '#984ea3',
	#									 '#999999', '#e41a1c', '#dede00']),
	#		                              int(max(y_pred) + 1))))

	xPos = [x[0] for x in Xdata]
	yPos = [x[1] for x in Xdata]
	zPos = [x[2] for x in Xdata]

	#ax.scatter(xPos, yPos, zPos, c='r', marker='o')
	ax.scatter(xPos, yPos, zPos, c='r', marker='.')

	plt.show()
