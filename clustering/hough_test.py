#!/usr/bin/env python

import sys
from array import array

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
from ROOT import TH2F
from ROOT import TF1
from ROOT import TVector3
from ROOT import TMath

# LCIO
#from pyLCIO.io.LcioReader import LcioReader
#from pyLCIO import EVEN pyLCIO import UTIL

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import math

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import kneighbors_graph
from sklearn import cluster, datasets, mixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances

from itertools import cycle, islice

########################################################################################################################
hits_pos = []

XMAX = 20
sigmaX = 0.5
sigmaY = 2

for x in range(0, XMAX) :
	randx = np.random.normal(0, sigmaX)
	randy = np.random.normal(0, sigmaY)
	xPos = x + randx
	yPos = 3.12 * xPos + randy + 30

	hits_pos.append( [xPos, yPos] ) 

########################################################################################################################
grRangeY1 = hits_pos[0][1]
grRangeY2 = hits_pos[XMAX-1][1]

if grRangeY1 > grRangeY2:
	grRangeY1, grRangeY2 = grRangeY2, grRangeY1

grRangeY1 = grRangeY1 - 3
grRangeY2 = grRangeY2 + 3

#print grRangeY1, grRangeY2

########################################################################################################################
rho_min = -60
rho_max = 60
nBin_x = 200
nBin_y = 100

#theta_min = -math.pi
theta_min = 0
theta_max = math.pi

hist = TH2F("", "", nBin_x, theta_min, theta_max, nBin_y, rho_min, rho_max)

# Hough transform
for hit in hits_pos :
	x = hit[0]
	y = hit[1]

	for t in np.arange(theta_min, theta_max, (theta_max - theta_min)/nBin_x) : 
		r = math.cos(t) * x + math.sin(t) * y

		hist.Fill(t, r)

########################################################################################################################
"""
c1 = TCanvas( 'c1', 'Example with Formula', 200, 10, 700, 500 )
c1.SetGridx()
c1.SetGridy()

funs = []

for i in range(0, len(hits_pos)) :
	funcName = 'func_' + str(i)
	fun = TF1( funcName, 'sin(x) * [0] + cos(x) * [1]', 0, TMath.Pi() )
	funs.append(fun)
	fun.SetParameter(0, hits_pos[i][0])
	fun.SetParameter(1, hits_pos[i][1])
	if i == 0:
		fun.GetYaxis().SetRangeUser(-40, 40)
		fun.Draw()
	else:
		fun.Draw('same')

c1.Update()
"""
########################################################################################################################
c2 = TCanvas( 'c2', 'Example with Formula', 200, 10, 700, 600 )
c2.SetGridx()
c2.SetGridy()

c2.Divide(2, 1)

c2.cd(1)
hist.Draw('colz')

### find the position of peak
maxBinContent = 0
maxBin_x = 0
maxBin_y = 0

for xbin in range(1, hist.GetXaxis().GetNbins()+1):
	for ybin in range(1, hist.GetYaxis().GetNbins()+1):
		if hist.GetBinContent(xbin, ybin) > maxBinContent:
			maxBinContent = hist.GetBinContent(xbin, ybin)
			maxBin_x = xbin
			maxBin_y = ybin

max_x = hist.GetXaxis().GetBinCenter(maxBin_x)
max_y = hist.GetYaxis().GetBinCenter(maxBin_y)

print 'theta: ', max_x, 'rho', max_y

#########
xpos = [hit[0] for hit in hits_pos]
ypos = [hit[1] for hit in hits_pos]

c2.cd(2)
gr = TGraph(len(xpos), array('d', xpos), array('d', ypos))
gr.SetMarkerStyle(20)
gr.GetYaxis().SetRangeUser(grRangeY1, grRangeY2)
gr.Draw('AP')

k  = math.tan(max_x + math.pi/2.)
y0 = max_y/math.sin(max_x)

funFit = TF1( 'HT_fit ', '[0] * x + [1]', 0, TMath.Pi() )
funFit.SetParameter(0, k)
funFit.SetParameter(1, y0)
funFit.SetRange(0, XMAX)
funFit.Draw('same')

c2.Update()
########################################################################################################################
text = raw_input('press any key to exit: ')
