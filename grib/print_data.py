# print_data.py: How to print all the data contained in a grib file.
# http://www.ecmwf.int/publications/manuals/grib_api/print_data_8py-example.html

import traceback
import sys

from gribapi import *

INPUT='/Users/painter1/src/grib_api-1.9.9/data/regular_latlon_surface.grib1'
VERBOSE=1 # verbose error reporting

def example():
    f = open(INPUT)
    gid = grib_new_from_file(f)

    values = grib_get_values(gid)
    for i in xrange(len(values)):
        print "%d %.10e" % (i+1,values[i])

    print '%d values found in %s' % (len(values),INPUT)

    for key in ('max','min','average'):
        print '%s=%.10e' % (key,grib_get(gid,key))

    grib_release(gid)
    f.close()

def main():
    try:
        example()
    except GribInternalError,err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>sys.stderr,err.msg

        return 1

if __name__ == "__main__":
    sys.exit(main())

