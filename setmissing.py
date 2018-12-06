# Change the missing_value and _FillValue to 1.0e20 for one variable in one file.
# Specify the file and variable name as runline arguments.
# And I assume that the variable has exactly 2,3,or 4 dimensions.
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

cdms2.useNetcdf3()

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
                    if varm[i,j,k] or numpy.isnan(varv[i,j,k]):
                        # Note that setting var[i,j,k] implicitly un-masks it at i,j,k.
                        # Also, I'm creating a mask wherever there is a NaN.
                       var[i,j,k] = new_FillValue
                       varm[i,j,k] = True
                elif len(varv.shape)==4:
                    for l in range(varv.shape[3]):
                        if varm[i,j,k,l] or numpy.isnan(varv[i,j,k,l]):
                            # Note that setting var[i,j,k,l] implicitly un-masks it at i,j,k,l.
                            # Also, I'm creating a mask wherever there is a NaN.
                            var[i,j,k,l] = new_FillValue
                            varm[i,j,k,l] = True
    var.setMissing(new_FillValue)  # If done sooner, would set mask to all False.
    # You cannot set explicitly _FillValue except when creating variable.
    # (added 2018.01.23: I think that you can now, the _setmissing() method does it on a TransientVariable as of cdat 2.8
    # However, if the _FillValue attribute does NOT exist, then when the file is re-opened,
    # var._FillValue has the correct value in Python.
    # This _FillValue doesn't show up with ncdump.
elif len(varv.shape)==2:
    for i in range(varv.shape[0]):
        for j in range(varv.shape[1]):
            if varm[i,j] or numpy.isnan(varv[i,j]):
                var[i,j] = new_Fill_Value
                varm[i,j] = True
    var.setMissing(new_FillValue)
else:
    print "cannot handle a variable of shape",varv.shape

f.close()




