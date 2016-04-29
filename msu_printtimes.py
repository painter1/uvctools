#!/usr/local/cdat/bin/python
"just checks the time and time_bnds variables for consistency"

import cdms2,glob

for file in glob.glob("*.nc"):
    f = cdms2.open(file)
    t = f['time']
    tb = f['time_bnds']
    print file,  max([ abs(t[i]- 0.5*(tb[i,0]+tb[i,1])) for i in range(len(t)) ])
