#!/usr/local/cdat/bin/python
"special script to change time units of a set of files, to force them to be consistent"

import cdms2,glob

for file in glob.glob("*.nc"):
    f=cdms2.open(file,'r+')
    t=f['time']
    t.toRelativeTime('days since 1850-1-1')
    #...toRelativeTime is supposed to fix the bounds
    # temporary code for when that didn't happen...
    tb = t.getExplicitBounds()
    if t[0]>tb[0,1]:
        toff = t[0]-15.5
        tb += toff
        t.setBounds(tb)
        tb = t.getBounds()
        f['time_bnds'].assignValue(tb)

    f.close()
