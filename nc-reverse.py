#!/usr/local/cdat/bin/python

# one-off tool to reverse order of latitude-dependent arrays in a sftlf file.
# arrays are lat(lat) and sftlf(lat,lon); the only other array is lon(lon).

import cdms2

f = cdms2.open('sftlf.nc','r+')
lat = f['lat']
sftlf = f['sftlf']
# Unfortunately, FileVariable doesn't have a reverse() function...
#lat.reverse()
#sftlf.reverse()

ll=lat[:]
ss=sftlf[:,:]
for i in range(160):
  lat[i] = ll[159-i]
  sftlf[i,:]=ss[159-i]
# still have to fix the bounds...
# and the above didn't affect lat._data_!
#...lat doesn't have bounds; getBounds just returns results of getGenericBounds().
lat._data_ = lat[:]
#...this does it.!

#f.close()
