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

import sys

#########################################
def drawPoint(allHitPos, evtNum):
	ps = ROOT.TEvePointSet()
	ps.SetOwnIds(ROOT.kTRUE)
	ps.SetMarkerSize(1)
	ps.SetMarkerStyle(4)
	ps.SetMarkerColor(2)

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
            
        evt = drawPoint(allHitPos, evtNum)
        text = raw_input('press any key to exit: ')

        if text == '':
            evt.DisableListElements()
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
	
	
	r = ROOT.TRandom(0)
	eventNumber = 1
	reader = LcioReader( fileName )
	print 'Loaded file: ', fileName
	
	event = None
	
	eveManager = ROOT.TEveManager.Create()
	readEvent()
