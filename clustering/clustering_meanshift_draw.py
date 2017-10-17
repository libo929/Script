#!/usr/bin/env python

#ROOT
import ROOT
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
from ROOT import TEveEventManager

# LCIO
from pyLCIO.io.LcioReader import LcioReader
from pyLCIO import EVENT
from pyLCIO import UTIL

import numpy as np

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph
from sklearn import cluster, datasets, mixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances

from itertools import cycle, islice

import sys


pointColor = {1: ROOT.kRed, 2: ROOT.kGreen, 3: ROOT.kBlue, 4: ROOT.kYellow, 5: ROOT.kMagenta, 6: ROOT.kCyan, 7: ROOT.kOrange, 8: ROOT.kSpring, 9: ROOT.kTeal, 10: ROOT.kAzure}

rnd = ROOT.TRandom(0)

#########################################
def drawPoints(allHitPos, evtNum):
	ps = ROOT.TEvePointSet()
	ps.SetOwnIds(ROOT.kTRUE)
	ps.SetMarkerSize(1)
	ps.SetMarkerStyle(4)

	rc = int(rnd.Uniform(1,10.9))
	#print rc
	pcolor = pointColor[rc]
	ps.SetMarkerColor(pcolor)

	evtName = 'SDHCAL event ' + str(evtNum)
	evt = TEveEventManager(evtName, "")
	eveManager.AddEvent(evt)

	mm2cm = 0.1

	for pos in allHitPos:
		ps.SetNextPoint(pos[0] * mm2cm, pos[1] * mm2cm, pos[2] * mm2cm)
		#ps.SetNextPoint(r.Uniform(-s,s), r.Uniform(-s,s), r.Uniform(-s,s))

	eveManager.AddElement(ps)
	eveManager.Redraw3D()

	return evt

#########################################
def drawClusters(hitClusters, evtNum):
	#print 'clusters: ', hitClusters
	evtName = 'SDHCAL event ' + str(evtNum)
	evt = TEveEventManager(evtName, "")
	eveManager.AddEvent(evt)

	mm2cm = 0.1

	for hitCluster in hitClusters:
		ps = ROOT.TEvePointSet()
		ps.SetOwnIds(ROOT.kTRUE)
		ps.SetMarkerSize(1)
		ps.SetMarkerStyle(4)
		rc = int(rnd.Uniform(1,10.9))
		pcolor = pointColor[rc]
		#print rc, pcolor
		ps.SetMarkerColor(pcolor)
		#ps.SetMarkerColor(2)
		#print 'cluster: ', len(hitCluster)
		#print '----'

		for pos in hitCluster:
			ps.SetNextPoint(pos[0] * mm2cm, pos[1] * mm2cm, pos[2] * mm2cm)
			#print pos[0], pos[1], pos[2]

		eveManager.AddElement(ps)
		eveManager.Redraw3D()


	return evt

#########################################

def readEvent():
    for event in reader:
        allHitPos = []

        hcalHits = event.getCollection('HCALOther')
        evtNum   = event.getEventNumber()

        nHit = hcalHits.getNumberOfElements()
        cellIdEncoding = hcalHits.getParameters().getStringVal( EVENT.LCIO.CellIDEncoding ) 
        idDecoder = UTIL.BitField64( cellIdEncoding )

        for iHit in range(0, nHit):
            caloHit = hcalHits.getElementAt( iHit )
            pos = caloHit.getPositionVec()
            cellID = long( caloHit.getCellID0() & 0xffffffff ) | ( long( caloHit.getCellID1() ) << 32 )
            idDecoder.setValue( cellID )
            layer = idDecoder['layer'].value()

            allHitPos.append( [pos[0], pos[1], pos[2]] )

        quantile = 0.025

        Xdata = StandardScaler().fit_transform(allHitPos)
        bandwidth = cluster.estimate_bandwidth(Xdata, quantile=quantile)
        ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(Xdata)
        y_pred = ms.labels_.astype(np.int)
        hitClusters = list(y_pred)
        
        clustersSelected = []
        
        iClu = 0
        minClusterSize = 0
        maxClusterSize = 10000
        
        while True:
            hitsNum = hitClusters.count(iClu)
        
            if hitsNum == 0:
                break
        
            allHits = len(hitClusters)
        
            idx = [i for i in range(allHits) if hitClusters[i] == iClu]
        	
            printOut = False

            if printOut:
                print '----> Cluster ', iClu, ': hits number: ', hitsNum, ' =================== '
                print idx, '\n'
        
        	###########################################
        	# select clusters to show by hit number
        	###########################################
            if hitsNum > minClusterSize and hitsNum < maxClusterSize:
                hitCluster = [allHitPos[i] for i in idx]
                clustersSelected.append( hitCluster )
        
            iClu = iClu + 1
    
    ###########################################

        evt = drawClusters(clustersSelected, evtNum)
        #evt = drawPoints(allHitPos, evtNum)
        text = raw_input('press any key to exit: ')

        if text == '':
            evt.DisableListElements()
            #print 'next event'
        else:
            print 'exit'
            break


if __name__=='__main__':
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
	
	
	#r = ROOT.TRandom(0)
	eventNumber = 1
	reader = LcioReader( fileName )
	print 'Loaded file: ', fileName
	
	event = None
	
	eveManager = ROOT.TEveManager.Create()
	readEvent()
