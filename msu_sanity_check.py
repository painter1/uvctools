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
if True:  # <<<< take this out when Qt works again <<<<
    v=vcs.init()

tlt=f['eqmsu_tlt']
print tlt.shape
len0 = tlt.shape[0]
v.plot(tlt[0:len0:12,0,0])
raw_input("Press Return to finish...")

fl = open(os.path.expanduser('~/msu/msu.log'))
for line in fl:
  if line.find('WARNING')>-1:
      print 120*'=','\n'
      print line
      print 120*'='
