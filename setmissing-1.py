# Change the missing_value and _FillValue to 1.0e20 for one variable in one file.
# This is a one-off tool, so the variable and file are just specified at the beginning.
# And I ASSUME that the variable has exactly 3 dimensions.
# You also can set the new fill value to something other than 1.0e20.

# The file must be NetCDF3 because cdms2 currently has a bug
# where you can't change the _FillValue attribute of a FileVariable from a NetCDF4 file.

# filen = 'TMT_3.nc'
# varn = 'tmt'   # N.B.  I'm assuming that it has 3 dimensions, e.g. time,lat,lon

import sys
import numpy
import cdms2
import debug

if len(sys.argv)<3:
    print "Please provide a filename and variable name argument."
    filen = 'ts2.nc'  # for testing convenience
else:
    filen = sys.argv[1]
    varn = sys.argv[2]

new_FillValue = 1.0e20

f = cdms2.open(filen,'r+')
var = f[varn]

varv = var.getValue()
varm = numpy.ma.getmaskarray(varv)

# Normally var has three dimensions.  That is common: time,lat,lon.
if len(varv.shape)==3 or  len(varv.shape)==4:
    for i in range(varv.shape[0]):
        for j in range(varv.shape[1]):
            for k in range(varv.shape[2]):
                if len(varv.shape)==3:
                    if varm[i,j,k]:
                       # Note that setting var[i,j,k] implicitly un-masks it at i,j,k.
                       var[i,j,k] = new_FillValue
                       varm[i,j,k] = True
                elif len(varv.shape)==4:
                    for l in range(varv.shape[3]):
                        if varm[i,j,k,l]:
                            # Note that setting var[i,j,k,l] implicitly un-masks it at i,j,k,l.
                            var[i,j,k,l] = new_FillValue
                            varm[i,j,k,l] = True
else:
    print "cannot handle a variable of shape",varv.shape

var.setMissing(new_FillValue)  # If done sooner, would set mask to all False.
# Sometimes the following will lead to a segfault on close.
# You cannot set _FillValue except when creating variable.
# setMissing should do it, this is a bug in my opintion.
#var._FillValue = var.missing_value # setMissing doesn't do this!
f.write(var)

f.close()




