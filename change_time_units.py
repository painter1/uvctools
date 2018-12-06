#!/usr/bin/env python

"""This changes the time units of a ts file, i.e. a file containing variables specified below, e.g. 'ts'
with a 'time' axis whose bounds name is also specified below.
 This script should be called with a file name argument.  Thus the usage is like:
   change_time_units.py filename
Note that the file gets changed!  See below for how to specify the variable name and other
characteristics of the file."""
# To specify the new time units, change the next line:
units = 'months since 1800'
# For a file with a variable other than 'ts', change the next line:
varname = 'ta'
#varname = 'tmt'
# For a file with a time bounds variable other than 'time_bnds', change the next line:
time_bnds_name = 'time_bnds'
#time_bnds_name = 'time_bounds'
# To add something to the time and time bounds axis, specify a number here (in the original units):
add2time = False

import sys, os
if len(sys.argv)<2:
    print "Please provide a filename argument."
    filename = 'ts2.nc'  # for testing convenience
else:
    filename = sys.argv[1]
if len(sys.argv)>2:
    varname = sys.argv[2]
print "filename=",filename,"varname=",varname

import cdms2, cdtime, numpy
from cdms2.error import CDMSError
import pdb, debug

def toRelativeTime(time_bnds, units, oldunits=None):
        """Convert values of time_bnds to another unit possibly in another calendar.
        The time variable, time_bnds.getTime(), should have already been converted."""
        # based on AbstractAxis.toRelativeTime(self,units,calendar)
        if not hasattr(time_bnds, 'units'):
            if oldunits==None:
                raise CDMSError, "No time units defined"
            time_bnds.units = oldunits
        tb = time_bnds.getTime()
        n=len(tb[:])
        calendar = tb.getCalendar()
        for i in range(n):
            for j in range(2):
                tmp=cdtime.reltime(time_bnds[i,j], time_bnds.units).tocomp(calendar)
                tmp2 = numpy.array(float(tmp.torel(units, calendar).value)).astype(time_bnds.dtype.char)
                time_bnds[i,j]=tmp2
        time_bnds.units=units
        return

f = cdms2.open( filename, 'r+' )
var = f[varname]
t = var.getTime()
oldunits = t.units
t.toRelativeTime(units)
# ... Note however that this change in t doesn't take effect until f.close().
if hasattr( t, 'bounds' ):
    time_bnds_name = t.bounds
    time_bnds=f[time_bnds_name]
    if not hasattr(time_bnds,'units'):
        time_bnds.units = oldunits
    print "jfp Found time_bnds=",time_bnds_name,time_bnds.__class__.__name__
    print "jfp time_bnds units=",time_bnds.units
    toRelativeTime( time_bnds, units, time_bnds.units)
else:
    boundsax = f.getBoundsAxis(2,boundid='bounds')  # not tested yet
    # boundsax = cdms2.createAxis( [0,1], id='bounds' )
    t.bounds = time_bnds_name
    time_bnds = cdms2.createVariable( t.genGenericBounds(), id=time_bnds_name, axes=[t,boundsax] )
    print "jfp Created time_bnds=",time_bnds.id,time_bnds.__class__.__name__
    time_bnds.units = units
    print "jfp time_bnds units=",time_bnds.units
    f.write(time_bnds)

if add2time:
    t += add2time
    time_bnds += add2time

print "jfp f[",time_bnds_name,"]=",f[time_bnds_name].id,f[time_bnds_name].__class__.__name__
print "jfp f[",time_bnds_name,"] units=",f[time_bnds_name].units

f.close()

# The following can be uncommented if needed for testing:
# f = cdms2.open( filename, 'r+' )
# ts = f['ts']
# t = ts.getTime()
# time_bnds = f['time_bnds']
# bounds=t.getBounds()
# print t,time_bnds,time_bnds[0],time_bnds[-1],bounds[0],bounds[-1]


