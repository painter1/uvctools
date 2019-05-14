#!/usr/bin/env python

# I have multiple sftlf files with time-dependence, but sftlf is really a constant.  This just
# reads a random one and writes out a single time-independent sftlf file.

import cdms2

cdms2.setNetcdf4Flag(0)
cdms2.useNetcdf3()

f = cdms2.open('b.e11.BRCP85C5CNBDRD.f09_g16.029.cam.h0.sftlf.200601-208012.nc')
sftlf = f('sftlf')
g = cdms2.open('sftlf.py','w')
g.write( sftlf[0,:,:], id='sftlf' )  # time is the first axis
f.close()
g.close()
