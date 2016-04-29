#!/env python

# Get grid information out of a CMIP5 data file and write it to a SCRIP grid file.

import cdms2, numpy

# def cmip5grid2scrip( cmip5datafile, variable=None, scripfile="grid.scrip.nc" ):
"""e.g. cmip5grid2scrip( 'sic_OImon_inmcm4_rcp85_r1i1p1_200601-210012.nc' ).
    This function reads a CMIP5 data file and writes a SCRIP-compatible grid file for a variable in it.
    By default, the variable is the main variable and its name is extracted from the data file name.
    The default output file name is 'grid.scrip.nc'."""
cmip5datafile='sic_OImon_inmcm4_rcp85_r1i1p1_200601-210012.nc'
variable=None
scripfile="grid.scrip.nc"

fd = cdms2.open( cmip5datafile )
if variable==None: variable = cmip5datafile.split('_')[0]  # e.g. 'sic'
var = fd[variable]   # a FileVariable
g = var.getGrid()   # e.g. <FileCurveGrid...>
m = g.getMesh()     # array has lat-lon of all corners of every cell
grid_size = m.shape[0]
grid_rank = m.shape[1]
grid_corners = m.shape[2]
# grid_dims would be [nlat,nlon] where nlat*nlon=grid_size.  Not done yet. <<<<
grid_corner_lat = m[:,0,:]
grid_corner_lon = m[:,1,:]
# Note: g.getMask() will be needed in some cases to generate grid_imask, I have to see one first.  For now... <<<<
if g.getMask()==None:
    grid_imask = numpy.ones( grid_size )
grid_center_lat = 0.25 * sum( grid_corner_lat[:,corner] for corner in range(4) )
grid_center_lon = 0.25 * sum( grid_corner_lon[:,corner] for corner in range(4) )

gsaxis = cdms2.createAxis( range(grid_size) )
gsaxis.id = 'grid_size'
gcaxis = cdms2.createAxis( range(4) )
gcaxis.id = 'grid_corners'
grid_center_lat_v = cdms2.createVariable(grid_center_lat,axes=[gsaxis])
grid_center_lat_v.id='grid_center_lat'
grid_center_lat_v.domain = [ var.domain[1] ]
grid_center_lon_v = cdms2.createVariable(grid_center_lon,axes=[gsaxis])
grid_center_lon_v.id='grid_center_lon'
grid_corner_lat_v = cdms2.createVariable(grid_corner_lat,axes=[gsaxis,gcaxis])
grid_corner_lat_v.id='grid_corner_lat'
grid_corner_lon_v = cdms2.createVariable(grid_corner_lon,axes=[gsaxis,gcaxis])
grid_corner_lon_v.id='grid_corner_lon'

fs = cdms2.open( scripfile, 'w' )
fs.write(grid_center_lat_v)
fs.write(grid_center_lon_v)
fs.write(grid_corner_lat_v)
fs.write(grid_corner_lon_v)

    
