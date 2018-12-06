#!/usr/bin/env python

# Changes level units to Pa.  Assumes that there is a 3-D variable ta in each file.

import sys, argparse
import cdms2
from genutil import udunits

def level_units_to_Pa( filen ):
    f=cdms2.open(filen,'r+')
    ta=f['ta']
    lev=ta.getLevel()
    tmp = udunits(1.0,'lev.units')
    s,i = tmp.how('Pa')
    lev[:] = s*lev[:] + i
    lev.units = 'Pa'
    f.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Change level units to Pa for ta.")
    p.add_argument( "--files", dest="files", help="Names of files to be changed", nargs='+',
                    required=True )
    args = p.parse_args(sys.argv[1:])
    print "input args=", args
    for filen in args.files:
        level_units_to_Pa(filen)
