import cdms2, sys

# Changes the time axis of the variable ts, so that the time centers equal the time lower bounds.
# This is designed for ts_*.nc files from CMIP5.  Usage:
#      python recenter_time.py ts_foo.nc [ ts_foo2.nc [ ts_foo3.nc .... ] ]

if len(sys.argv)<2 :
    sys.stderr.write("Usage: python %s file1 file2...\n" % sys.argv[0] )
    raise SystemExit(1)
files = sys.argv[1:]
varname='ts'

for file in files:
    f = cdms2.open(file,'r+')
    time_bnds = f['time_bnds']
    assert( time_bnds is not None )
    var = f[varname]
    assert( var is not None )
    t = var.getTime()
    for i in range(len(t)):
        t[i] = time_bnds[i,0]
    f.close()
    print "recentered",file
