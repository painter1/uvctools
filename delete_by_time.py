"""This deletes data from a time-dependent variable in a NetCDF file.  It writes the result
 into a new, uniquely named, file.  This script should be called with the file and variable names.
 This was written for specific CCSM4 ts,ps files, but if there's a need it could be generalized later.
 Thus the usage
is like:
  python delete_by_time.py filename varname
Presently data for the first year will be deleted, from variables named 'ps' and 'ts'."""

ntdel = 12  # number of time values to be deleted from the beginning
# varnames = ['ps','ts']

import sys, os
if len(sys.argv)<3:
    print "Please provide filename and varname arguments."
    filename = 'ts2.nc'  # for testing convenience
    varname  = 'ts'      # for testing convenience
else:
    filename = sys.argv[1]
    varname  = sys.argv[2]

import cdms2, cdtime, numpy
from cdms2.error import CDMSError
import time, datetime

# When compression is turned off as follows, CDAT will write a NetCDF3 file:
cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)

# Use time to make the output filename unique.
timt=time.localtime().__reduce__()[1][0]
tims = '_'+'.'.join(str(i) for i in timt)

f = cdms2.open( filename, 'r' )
# fvar = f[varname]
# ft = f['time']
# ftb = f['time_bnds']

# The new file should be the same as the original file except for the time dimension,
# the time,time_bnds, and ta variables, and most attributes.  This history attribute
# should be changed, at a minimum..
fne = os.path.splitext(filename)
gname = fne[0]+tims+fne[1]
g = cdms2.open( gname, 'w' )

# This copy omits whatever is needed to make an axis 'unlimited', but we shouldn't need that.
ftime = f.axes['time']  # transient variable
times = ftime[ntdel:].copy()
g.createAxis( 'time', times )
g['time'].units = ftime.units
if hasattr( ftime, 'long_name' ):
    g['time'].long_name = ftime.long_name
if hasattr( ftime, 'standard_name' ):
    g['time'].standard_name = ftime.standard_name
if hasattr( ftime, 'calendar' ):
    g['time'].calendar = ftime.calendar
if hasattr( ftime, 'axis' ):
    g['time'].axis = ftime.axis
gtime = g.axes['time']

flat = f.axes['lat']
lats = flat[:].copy()
g.createAxis( 'lat', lats )
g['lat'].units = flat.units
if hasattr( flat, 'long_name' ):
    g['lat'].long_name = flat.long_name
if hasattr( flat, 'standard_name' ):
    g['lat'].standard_name = flat.standard_name
if hasattr( flat, 'axis' ):
    g['lat'].axis = flat.axis
glat = g['lat']

flon = f.axes['lon']
lons = flon[:].copy()
g.createAxis( 'lon', lons )
g['lon'].units = flon.units
if hasattr( flon, 'long_name' ):
    g['lon'].long_name = flon.long_name
if hasattr( flon, 'standard_name' ):
    g['lon'].standard_name = flon.standard_name
if hasattr( flon, 'axis' ):
    g['lon'].axis = flon.axis
glon = g['lon']

var = f(varname)[ntdel:,:,:]
g.createVariableCopy( var )
gvar = g[varname]
gvar[:,:,:] = var[:,:,:]

time_bnds = f('time_bnds')[ntdel:,:]
g.createVariableCopy( time_bnds )
gtime_bnds = g['time_bnds']
gtime_bnds[:,:] = time_bnds[:,:]
gtime.bounds = 'time_bnds'

lat_bnds = f('lat_bnds')[:,:]
g.createVariableCopy( lat_bnds )
glat_bnds = g['lat_bnds']
glat_bnds[:,:] = lat_bnds[:,:]
glat.bounds = 'lat_bnds'

lon_bnds = f('lon_bnds')[:,:]
g.createVariableCopy( lon_bnds )
glon_bnds = g['lon_bnds']
glon_bnds[:,:] = lon_bnds[:,:]
glon.bounds = 'lon_bnds'

# As I'm not confident that all of f's gobal attributes can be copied, I'll copy attributes
# one-by-one, and only certain named ones.  Some might get missed...
if hasattr( f, 'institution' ): g.institution = f.institution
if hasattr( f, 'institute_id' ): g.institute_id = f.institute_id
if hasattr( f, 'experiment_id' ): g.experiment_id = f.experiment_id
if hasattr( f, 'source' ): g.source = f.source
if hasattr( f, 'model_id' ): g.model_id = f.model_id
if hasattr( f, 'forcing' ): g.forcing = f.forcing
if hasattr( f, 'parent_experiment_id' ): g.parent_experiment_id = f.parent_experiment_id
if hasattr( f, 'parent_experiment_rip' ): g.parent_experiment_rip = f.parent_experiment_rip
if hasattr( f, 'branch_time' ): g.branch_time = f.branch_time
if hasattr( f, 'contact' ): g.contact = f.contact
if hasattr( f, 'references' ): g.references = f.references
if hasattr( f, 'initialization_method' ): g.initialization_method = f.initialization_method
if hasattr( f, 'physics_version' ): g.physics_version = f.physics_version
if hasattr( f, 'product' ): g.product = f.product
if hasattr( f, 'experiment' ): g.experiment = f.experiment
if hasattr( f, 'frequency' ): g.frequency = f.frequency
if hasattr( f, 'Conventions' ): g.Conventions = f.Conventions
if hasattr( f, 'project_id' ): g.project_id = f.project_id
if hasattr( f, 'table_id' ): g.table_id = f.table_id
if hasattr( f, 'title' ): g.title = f.title
if hasattr( f, 'parent_experiment' ): g.parent_experiment = f.parent_experiment
if hasattr( f, 'modeling_realm' ): g.modeling_realm = f.modeling_realm
if hasattr( f, 'realization' ): g.realization = f.realization
if hasattr( f, 'cmor_version' ): g.cmor_version = f.cmor_version
today = str(datetime.date.today())
if hasattr( f, 'history' ):
    g.history = f.history+"; "+today+" removed values for some times."
g.creation_date = today

f.close()
g.close()
