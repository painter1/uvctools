#!/env python

# Apply an offset to times in files, the output files of the MSU tool.

import cdms2

offset = 1.0
# file = 'tls_both___IPSL-CM5A-LR.r1i1p1.piControl.mon.nc'
file = 'test.nc'
f = cdms2.open(file,'r+')
eqmsu_tlt = f['eqmsu_tls']   # this is the MSU temperatures
t = eqmsu_tlt.getTime()
bndnom = t.bounds
time_bnds = f[bndnom]
assert( t == time_bnds.getTime() )

print t[0:4], time_bnds[0:4], tb[0:4]

t[0:len(t)] += offset      # strangely, t[:] causes file to grow without bounds
time_bnds[0:len(t),0:2] += offset

print t[0:4], time_bnds[0:4], tb[0:4]

