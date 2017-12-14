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
quantile = 0.0008
#quantile = 0.05
shift = 100

# the limits for selecting clusters
minClusterSize = 1
maxClusterSize = 10000

printOut = False
####################

if len(sys.argv) == 4:
	fileName = sys.argv[1]
	minClusterSize = int(sys.argv[2])
	maxClusterSize = int(sys.argv[3])
	
	if minClusterSize > maxClusterSize:
		minClusterSize, maxClusterSize = maxClusterSize, minClusterSize

if len(sys.argv) == 2:
	fileName = sys.argv[1]

if len(sys.argv) == 1:
	fileName = "PDG211_50GeV_endcap_rec_0.slcio"


eventNumber = 1
reader = LcioReader( fileName )
print 'Loaded file: ', fileName

event = None

########################################
# recalc event parameters

# merge two events in one
nevt  = 0

# due to the shift in x and y direction
shift = shift / 1.41
########################################


allHitPos = []

for event in reader:

	if skip > 0 :
		skip = skip - 1
		continue

	nevt = nevt + 1
	if nevt > maxEvt:
		break

	#hcalHits = event.getCollection('HCALBarrel')
	hcalHits = event.getCollection('ECALBarrel')
	nHit = hcalHits.getNumberOfElements()
	print 'hit number: ', nHit
	cellIdEncoding = hcalHits.getParameters().getStringVal( EVENT.LCIO.CellIDEncoding )
	idDecoder = UTIL.BitField64( cellIdEncoding )

	for iHit in range(0, nHit) :
		caloHit = hcalHits.getElementAt( iHit )
		pos = caloHit.getPositionVec()
		cellID = long( caloHit.getCellID0() & 0xffffffff ) | ( long( caloHit.getCellID1() ) << 32 )
		idDecoder.setValue( cellID )
		#layer = idDecoder['S-1'].value()

		allHitPos.append( [pos[0], pos[1], pos[2]] )

	print len(allHitPos)

	########################################################################################################################
	#plt.style.use(['classic'])
	plt.style.use(['seaborn-notebook'])

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

	hitClusters = list(y_pred)

	clustersSelected = []
	cluColor = []

	iClu = 0
	
	while True:
		hitsNum = hitClusters.count(iClu)

		if hitsNum == 0:
			break

		allHits = len(hitClusters)

		idx = [i for i in range(allHits) if hitClusters[i] == iClu]
		
		if printOut:
			print '----> Cluster ', iClu, ': hits number: ', hitsNum, ' =================== '
			print idx, '\n'

		###########################################
		# select clusters to show by hit number
		###########################################
		if hitsNum > minClusterSize and hitsNum < maxClusterSize:
			hitPos = [Xdata[i] for i in idx]
			for pos in hitPos:
				clustersSelected.append( pos )
				cluColor.append(iClu)

		iClu = iClu + 1

	#print clustersSelected
	xPos = [x[0] for x in clustersSelected]
	yPos = [x[1] for x in clustersSelected]
	zPos = [x[2] for x in clustersSelected]

	f, (ax1, ax2, ax3)  = plt.subplots(1, 3)
	f.tight_layout()

	markerSize = 30

	ax1.scatter(xPos, zPos, c=colors[cluColor], marker='.', s=markerSize)
	ax1.set_xlabel('X')
	ax1.set_ylabel('Z')

	ax2.scatter(xPos, yPos, c=colors[cluColor], marker='.', s=markerSize)
	ax2.set_xlabel('X')
	ax2.set_ylabel('Y')

	ax3 = f.add_subplot(1, 3, 3, projection='3d')
	ax3.scatter(xPos, yPos, zPos, c=colors[cluColor], marker='.', s=markerSize)
	ax3.set_xlabel('X')
	ax3.set_ylabel('Y')
	ax3.set_zlabel('Z')

	plt.show()

	text = raw_input('enter to next event: ')

	if text == '':
		#print '...'
		del allHitPos[:]
	else:
		print 'exit'
		break
