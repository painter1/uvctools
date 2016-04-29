# One-off code to add 10 months to a file.

from time import ctime
import numpy
import cdms2

# Try to get a NetCDF-3 file, but anything I do produces a "netCDF-4 classic model" file.:
cdms2.useNetcdf3()
#value = 0
#cdms2.setNetcdfShuffleFlag(value) ## where value is either 0 or 1
#cdms2.setNetcdfDeflateFlag(value) ## where value is either 0 or 1
#cdms2.setNetcdfDeflateLevelFlag(value) ## where value is a integer between 0 and 9 included

f=cdms2.open('TMT_5.nc')
tmt = f('tmt')
tmtd = tmt
for i in range(10):
  tmtd = numpy.append( tmtd, tmtd[-1:], axis=0 )
time=tmt.getTime()
lat=tmt.getLatitude()
lon=tmt.getLongitude()
time_bounds = f(time.bounds)
lat_bounds = f(lat.bounds)
lon_bounds = f(lon.bounds)

timed=numpy.append(time,range(2594,2604))
time_boundsd=numpy.append( time_bounds, [[timed[i],timed[i]+1] for i in range(448,458)], axis=0 )
#...Why these numbers?...time shape is (448,), highest value is 2593.
timex = cdms2.createAxis( timed, bounds=time_boundsd, id=time.id )
timex.attributes = time.attributes
bounds=time_bounds.getAxis(1)
atts = time_bounds.attributes
atts['_FillValue'] = 1.0e20
time_boundsx = cdms2.createVariable( time_boundsd, fill_value=1.0e20, axes=[timex,bounds],
                                     attributes=atts, id='time_bounds' )
timex.bounds = 'time_bounds'
atts = tmt.attributes
atts['_FillValue'] = 1.0e20
tmtx = cdms2.createVariable( tmtd, fill_value=1.0e20, axes=[timex,lat,lon],
                             attributes=atts, id=tmt.id )
g=cdms2.open('TMT_6.nc','w')
for att in f.attributes.keys():
    if att not in g.attributes:
        setattr( g, att, getattr(f,att) )
if not hasattr(g,'history'): g.history=""
g.history = g.history+",\n"+ctime()+\
    ": changed to standard variable name, fill value, etc. and filled out the year 2016 by duplicating February"
f.close()
g.write(tmtx)
for att in time.attributes.keys():
    setattr( g['time'], att, getattr(time,att) )
for att in time_bounds.attributes.keys():
    setattr( g['time_bounds'], att, getattr(time_bounds,att) )
for att in lat_bounds.attributes.keys():
    setattr( g['latitude_bounds'], att, getattr(lat_bounds,att) )
for att in lon_bounds.attributes.keys():
    setattr( g['longitude_bounds'], att, getattr(lon_bounds,att) )

g.close()

