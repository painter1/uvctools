# experimental functions for reading Grib files using the Python interface of grib_api
# My intent is that eventually this could be migrated to full cdms support

from gribapi import *

class gribmsg:
    # Python object representing a GRIB object, which is normally identified just by a numerical handle.
    # We can put attributes on this, or data in it, unlike the handle.
    def __init__( self, gid ):
        self.gid = gid

class gribf:

    def __init__( self, gribfilename, rw='r' ):
        open(  self, gribfilename, rw='r' )

    def open( gribfilename, rw='r' ):
        # >>> check that it is a grib file (or better, cdms2 would do that and branch here
        # >>> probably other stuff will have to be done here to support normal python/cdat/cdms things
        self.file = open( gribfilename, rw )
        # Get all the messages (records) of the file, following an example count_messages in ecmwf.int, which suggests
        # (to jfp) that grib doesn't have random access to files:
        mcount = grib_count_in_file( self.file )
        gid_list = [ grib_new_from_file(f) for i in range(mcount) ]
        msg_list = [ gribmsg( gid ) for gid in gid_list ]
        # For each message get its keys (aka attributes).
        # I imagine that this is the Product Definition Section (PDS) of the GRIB file:
        for msg in msg_list:
            gid = msg.gid
            iterid = grib_keys_iterator_new(gid)  # no namespace specified gives a long list...
            # ...I'm not certain that it includes all keys in namespaces, need to check that.
            while grib_keys_iterator_next(iterid):
                keyname = grib_keys_iterator_get_name(iterid)
                keyval = grib_get_string(iterid,keyname)
                setattr( msg, keyname, keyval )
            grib_keys_iterator_delete(iterid)

            # For each message get its grid.  This may be described simply by the grid identification octet (search the
            # GRIB guide for "Table B"), but ideally will be described by the Grid Description Section (GDS) of the GRIB file.
            # >>>>not done<<<<

            # For each message get its data.  This is the Binary Data Section (BDS) of the GRIB file.
            # This should also include a mask from the Bit Map Section (BMS) of the GRIB file,
            # but I can't find a way to get it.  Maybe this will help, if it works:
            # missingValue = grib_get( gid, 'missingValue' )
            # after which you could check the data for occurences of missingValue
            # >>>> but until the basics work I won't deal with missing values.
            # >>>> ideally we wouldn't actually read the data yet (like var=f['var'] in cdms),
            # >>>> but for now just read it all in (like var=f('var') in cdms.)
            self.values = grib_get_values( gid )
            # >>>>not finished<<<<

            #            grib_release(gid)    # Once we've built the Python object, we don't need the GRIB object...
            #  ... but for now this is commented-out in case we need the GRIB object for debugging.

        return self.file

    def close():
        self.file.close()
