#!/usr/bin/env python

# Plots some MSU temperature data, for use as a sanity check.
# Run this under CDAT, not Python.

import vcs, sys, cdms2, os
if len(sys.argv)<2 :
    sys.stderr.write("Usage: %s file1\n" % sys.argv[0] )
    raise SystemExit(1)
file = sys.argv[1]
# print "plotting from",file
f=cdms2.open(file)
v=vcs.init()

varn = os.path.basename(file).split('_')[0]
# ... tlt for file=~/MSU_out/tlt_both___CanESM2.r10i1p1.historical-r5.mon.195001-202012.nc
var=f['eqmsu_'+varn]  # E.g. f['eqmsu_tlt']
print var.shape
len0 = var.shape[0]
if len0>=24:
    v.plot(var[0:len0:12,0,0])
else:
    v.plot(var[:,int(0.7*var.shape[1]),0])
    #v.plot(var[:,0,0])
raw_input("Press Return to finish...")

fl = open(os.path.expanduser('~/msu/msu.log'))
for line in fl:
  if line.find('WARNING')>-1:
      print 120*'=','\n'
      print line
      print 120*'='
