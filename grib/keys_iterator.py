# keys_iterator.py:  How to get the names of all the keys.
# http://www.ecmwf.int/publications/manuals/grib_api/keys_iterator_8py-example.html

import traceback
import sys

from gribapi import *

INPUT='/Users/painter1/src/grib_api-1.9.9/data/regular_latlon_surface.grib1'  # from print_data
# original INPUT='/Users/painter1/src/grib_api-1.9.9/data/reduced_latlon_surface.grib1'
VERBOSE=1 # verbose error reporting

def example():
    f = open(INPUT)

    while 1:
        gid = grib_new_from_file(f)
        if gid is None: break

#original        iterid = grib_keys_iterator_new(gid,'ls')
#another namespace     iterid = grib_keys_iterator_new(gid,'mars')
        iterid = grib_keys_iterator_new(gid)  # no namespace specified gives a long list

        # Different types of keys can be skipped
        # grib_skip_computed(iterid)
        # grib_skip_coded(iterid)
        # grib_skip_edition_specific(iterid)
        # grib_skip_duplicates(iterid)
        # grib_skip_read_only(iterid)
        # grib_skip_function(iterid)

        while grib_keys_iterator_next(iterid):
            keyname = grib_keys_iterator_get_name(iterid)
            keyval = grib_get_string(iterid,keyname)
            print "%s = %s" % (keyname,keyval)

        grib_keys_iterator_delete(iterid)
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

