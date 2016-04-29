# Adds bounds to an axis in a NetCDF file, if it doesn't already have bounds.  The bounds come
# from genGenericBounds().

import sys
import cdms2

if len(sys.argv)<3:
    print "Please provide a filename and axis name argument."
    filen = 'ts2.nc'  # for testing convenience
else:
    filen = sys.argv[1]
    axn = sys.argv[2]

# When compression is turned off as follows, CDAT will write a NetCDF3 file:
cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)

def getBounds( ax, f, units=None ):
    # Returns the bounds of a variable if they exist; otherwise generates bounds and returns them.
    # f is a cdms-opened file, opened with 'r+' ('r' will work if the variable already has bounds)
    # and var is a FileAxis (TransientAxis will work if it already has bounds)
    # N.B. This uses the units and bounds attribute of ax.  If ax is a recently changed FileAxis
    # and the file had not been closed yet, the new attribute values may not take effect here.
    # That's why there is an optional third argument to specify the units.
    if units==None: units = getattr(ax,'units',None)
    if hasattr( ax, 'bounds' ):
        bnds_name = ax.bounds
        return f(bnds_name)
    else:
        boundsax = f.getBoundsAxis(2,boundid='bounds')
        bnds_name = ax.id+'_bounds'
        ax.bounds = bnds_name
        # The following getGenericBounds call will issue ax.getData() which will lead to a message
        # ncvarget: ncid 65536; varid 3: NetCDF: Operation not allowed in define mode
        # So far as I can tell, this is harmless, it's just a warning that the NetCDF
        # library has switched to data mode.
        ax.genGenericBounds()
        ax_bnds = cdms2.createVariable( ax.genGenericBounds(), id=bnds_name, axes=[ax,boundsax] )
        if units!=None:  ax_bnds.units = units
        f.write(ax_bnds)

f = cdms2.open(filen,'r+')
ax = f[axn]
getBounds( ax, f )
f.close()

