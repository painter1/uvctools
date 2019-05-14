#!/usr/bin/env python

# Input: a file containing the CESM/E3SM variable LANDFRAC.  This is land area fraction.
#     If you don't supply the filename, this will look for a file named LANDFRAC.nc.
# Output: creates a new file, named sftlf.nc, containing the CMIP-5 variable sftlf.
#     This is land area percentage.

import os, sys, argparse
import cdms2

def make_sftlf_file( infilen, outfilen ):
    print 'Writing from %s to %s' % (infilen, outfilen)

    # Write output in NetCDF-3 format for compatibility with Ben Santer's software:
    cdms2.setNetcdf4Flag(0)
    cdms2.useNetcdf3()

    fi = cdms2.open( infilen )
    fo = cdms2.open( outfilen, 'w' )
    LANDFRAC = fi('LANDFRAC')
    sftlf = LANDFRAC*100
    sftlf.units = '%'
    sftlf.long_name = "Percentage of surface area covered by land"
    sftlf.standard_name = "land_area_fraction"
    sftlf.id = 'sftlf'
    fo.write( sftlf, id='sftlf' )
    fo.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser( description="Convert LANDFRAC to sftlf in a new file" )
    p.add_argument( "--infiles", dest="infiles", help="Names of input LANDFRAC files (mandatory)",
                    nargs='+', required=True )
    args = p.parse_args(sys.argv[1:])
    for infilen in args.infiles:
        outfilen = os.path.basename(infilen).replace('LANDFRAC','sftlf')
        make_sftlf_file( infilen, outfilen )
