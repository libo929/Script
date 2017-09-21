#!/usr/bin/env python

import math
import random
from array import array

# --- LCIO dependencies ---
from pyLCIO import UTIL, EVENT, IMPL, IO, IOIMPL

#---- number of events per momentum bin -----
nevt = 3
#--------------------------------------------

random.seed()


#========== particle properties ===================

configs = [ [10, 30, 50], [10, 30, 100], [10, 30, 200] ]

genstat  = 1
decayLen = 1.e32 
#=================================================

#================================================


for p1, p2, shifty in configs:
    outfile = 'PDG130211_' + str(p1) + 'GeV_' + str(p2) +'GeV_' + str(shifty) + 'mm.slcio'

    # write a RunHeader
    run = IMPL.LCRunHeaderImpl() 
    run.setRunNumber( 0 ) 
    run.parameters().setValue("Generator","${lcgeo}_DIR/examples/lcio_particle_gun.py")

    wrt = IOIMPL.LCFactory.getInstance().createLCWriter( )
    wrt.open( outfile , EVENT.LCIO.WRITE_NEW ) 
    wrt.writeRunHeader( run ) 

    print "---> created outfile: " , outfile
    
    for j in range( 0, nevt ):

        col = IMPL.LCCollectionVec( EVENT.LCIO.MCPARTICLE ) 
        evt = IMPL.LCEventImpl() 

        evt.setEventNumber( j ) 
        evt.addCollection( col , "MCParticle" )

		# K0L
        pdg1    = 130
        charge1 = 0
        mass1   = 0.497611

		# pion
        pdg2    = 211
        charge2 = 1
        mass2   = 0.139570

        energy1   = math.sqrt( mass1*mass1  + p1 * p1 ) 
        energy2   = math.sqrt( mass2*mass2  + p2 * p2 ) 

        phi1 =  random.random() * math.pi * 2.
        phi2 =  random.random() * math.pi * 2.

        theta1 = random.random() * math.pi / 180. # constained in one degree
        theta2 = random.random() * math.pi / 180.
        
        px1 = p1 * math.cos( phi1 ) * math.sin( theta1 ) 
        py1 = p1 * math.sin( phi1 ) * math.sin( theta1 )
        pz1 = p1 * math.cos( theta1 ) 

        px2 = p2 * math.cos( phi2 ) * math.sin( theta2 ) 
        py2 = p2 * math.sin( phi2 ) * math.sin( theta2 )
        pz2 = p2 * math.cos( theta2 ) 

        momentum1  = array('f',[ px1, py1, pz1 ] )  
        momentum2  = array('f',[ px2, py2, pz2 ] )  

		# start from HCAL endcap
        vtx1 = array('d',[ 50., 1400., 2650 ] )  
        vtx2 = array('d',[ 50., 1400 - shifty, 2650 ] )  

        #epx = decayLen * math.cos( phi ) * math.sin( theta ) 
        #epy = decayLen * math.sin( phi ) * math.sin( theta )
        #epz = decayLen * math.cos( theta ) 

        #endpoint = array('d',[ epx, epy, epz ] )  
        

#--------------- create MCParticle -------------------
        
        mcp1 = IMPL.MCParticleImpl() 
        mcp1.setGeneratorStatus( genstat ) 
        mcp1.setMass( mass1 )
        mcp1.setPDG( pdg1 ) 
        mcp1.setMomentum( momentum1 )
        mcp1.setCharge( charge1 ) 
        mcp1.setVertex( vtx1 ) 

        #if( decayLen < 1.e9 ) :   # arbitrary ...
        #    mcp.setEndpoint( endpoint ) 

        mcp2 = IMPL.MCParticleImpl() 
        mcp2.setGeneratorStatus( genstat ) 
        mcp2.setMass( mass2 )
        mcp2.setPDG( pdg2 ) 
        mcp2.setMomentum( momentum2 )
        mcp2.setCharge( charge2 ) 
        mcp2.setVertex( vtx2 ) 

#-------------------------------------------------------

      

#-------------------------------------------------------


        col.addElement( mcp1 )
        col.addElement( mcp2 )

        wrt.writeEvent( evt ) 

    wrt.close() 


#
#  longer format: - use ".hepevt"
#

#
#    int ISTHEP;   // status code
#    int IDHEP;    // PDG code
#    int JMOHEP1;  // first mother
#    int JMOHEP2;  // last mother
#    int JDAHEP1;  // first daughter
#    int JDAHEP2;  // last daughter
#    double PHEP1; // px in GeV/c
#    double PHEP2; // py in GeV/c
#    double PHEP3; // pz in GeV/c
#    double PHEP4; // energy in GeV
#    double PHEP5; // mass in GeV/c**2
#    double VHEP1; // x vertex position in mm
#    double VHEP2; // y vertex position in mm
#    double VHEP3; // z vertex position in mm
#    double VHEP4; // production time in mm/c
#
#    inputFile >> ISTHEP >> IDHEP 
#    >> JMOHEP1 >> JMOHEP2
#    >> JDAHEP1 >> JDAHEP2
#    >> PHEP1 >> PHEP2 >> PHEP3 
#    >> PHEP4 >> PHEP5
#    >> VHEP1 >> VHEP2 >> VHEP3
#    >> VHEP4;
