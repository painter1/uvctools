#!/usr/local/cdat/bin/python

# one-off tool to replace lat and lat_bnds in a sftlf file with values from a ts file
# The bad guy came from BNU.

import cdms2

fts = cdms2.open( 'ts_Amon_BNU-ESM_historical_r1i1p1_185001-200512.nc', 'r' )
fsf = cdms2.open( 'sftlf.nc', 'r+' )

slat = fsf[ 'lat' ]
slatbnds = fsf[ 'lat_bnds' ]
tlat = fts[ 'lat' ]
tlatbnds = fts[ 'lat_bnds' ]

for i in range(64):
    slat[i] = tlat[i]
    slatbnds[i,0] = tlatbnds[i,0]
    slatbnds[i,1] = tlatbnds[i,1]

fts.close()
fsf.close()

