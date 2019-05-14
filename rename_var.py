#!/usr/bin/env python

# Writes a copy of a file with one variable renamed.  Only that one variable, and supporting
# variables such as axes, will be written; any others will be ignored.  Most attributes also
# will be ignored.
# The input file can be in any directory.  The output file is written to the current directory.
# This script is filled with ad-hoc fixes to other data oddities.  Read this before running it!

import os, sys, argparse, numpy
import cdms2, cdutil
from pprint import pprint
import debug

cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)
cdms2.setNetcdfShuffleFlag(0)   

def rename_variable( invar, outvar, infn ):
    outfn = '_'.join([outvar,os.path.basename(infn)])
    print 'Writing from %s to %s' % (infn, outfn)
    fi=cdms2.open(infn)
    fo=cdms2.open(outfn,'w')
    V=fi(invar)
    
    # Various fixups, mostly ad-hoc...

    # Fix up time
    if V.getTime() is not None:
        t=V.getTime()
        ## ad-hoc fix for NCAR data with units in "days since...": put the day in the middle of the month:
        #  t[:] = t[:] - 15.0
        ## For NCAR or other data without time bounds, set them:
        #  cdutil.times.setTimeBoundsMonthly(V)
        # standard time units for Ben Santer's work:
        t.toRelativeTime("months since 1800")

    ## NCAR data from Curt has a missing value in April 1991, but is improperly set to 0,
    ## and the missing value mask hasn't been set...
    #  new_mask = numpy.ma.make_mask( V==0. )
    #  V.mask = numpy.logical_or( V.mask, new_mask )
    #  V[ V==0. ] = V._FillValue

    # Change pressure units, if any, from Pa to mbar.  If necessary, I'll generalize this later.
    # Why mbar?  It's what we get if we use verticalT.py to convert hybrid levels to pressure levels.
    if hasattr( V, 'units' ) and V.units=='Pa':
        V = V * 0.01
        V.units = 'mbar'

    # ...End of fixups, now write the variable to the new file, using the new name.

    V.id = outvar
    fo.write(V,id=outvar)
    fo.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Rename invar to outvar, and other fixups")
    p.add_argument( "--invar", dest="invar", help="Variable to be renamed", nargs=1,
                    required=True )
    p.add_argument( "--outvar", dest="outvar", help="New name of variable", nargs=1,
                    required=True )
    p.add_argument( "--infiles", dest="infiles", help="Names of input files (mandatory)", nargs='+',
                    required=True )
    args = p.parse_args(sys.argv[1:])
    print "input args=", args
    for infn in args.infiles:
        rename_variable( args.invar[0], args.outvar[0], infn )
