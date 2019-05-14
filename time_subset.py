#!/usr/bin/env python

# Writes a copy of a file with time subsetted.  For the moment, variable names are hard-coded.
# But I have in mind that this could be generalized in the future.

import sys, argparse, pdb, numpy, cdms2, debug

cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)
cdms2.setNetcdfShuffleFlag(0)   

def subset_time( infn, outfn, ti0, timax ):
    # Input is name of input and output files, and a pair of time indices.
    # The indices are used to subset time.  The output file has the new
    # time axis, other axes as needed, and select variables.
    fi=cdms2.open(infn)
    fo=cdms2.open(outfn,'w')
    # fi('T') won't work for large arrays T due to a bug in libnetcdf...
    time_varbls = [ 'T', 'ps', 'ts' ]
    new_time_varbls = [ fi[var][ti0:timax] for var in time_varbls if var in fi.variables.keys() ]
    for var in new_time_varbls:
        fo.write(var)
    other_varbls = [ 'hyam', 'hybm', 'P0' ]
    new_other_varbls = [ fi[var] for var in other_varbls if var in fi.variables.keys() ]
    for var in new_other_varbls:
        if var.id=='P0':  # The write in dataset.py doesn't work will if no axes.
            attributes=dict(var.attributes) # shallow copy
            if '_FillValue' in attributes:
                attributes.pop('_FillValue')    # It's hard to set _FillValue
            if 'missing_value' in attributes:   # and createVariableCopy copies missing_value
                attributes.pop('missing_value') #  to _FillValue 
            fo.write(var,dtype=numpy.int64,id=var.id,attributes=attributes)
        else:
            fo.write(var)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Subset time between two indices")
    p.add_argument( "--ti0", dest="ti0", help="First time index", nargs=1,
                    type=int, required=True )
    p.add_argument( "--timax", dest="timax", help="Maximum time index", nargs=1,
                    type=int, required=True )
    p.add_argument( "--infile", dest="infile", help="Name of input file", nargs=1,
                    required=True )
    p.add_argument( "--outfile", dest="outfile", help="Name of output file", nargs=1,
                    required=True )
    args = p.parse_args(sys.argv[1:])
    subset_time( args.infile[0], args.outfile[0], args.ti0[0], args.timax[0] )
