#!/usr/local/cdat/bin/python

# one-off tool to replace "missing" data with 0.0 in a sftlf file (the bad guy came from FIO)
# Also, this needs to multiply by 100.
# >>> TO DO: check what the MSU computation did with this.  Did Charles
# >>> put in something to treat a 0...1 sftlf correctly???  "missing" values????
# Note that fio's sftlf file has basically no attributes.

import cdms2, numpy

f = cdms2.open('sftlf.nc','r+')
lat = f['lat']
sftlf = f['sftlf']
# sftlf.setMissing(0) will set the "missing value" to 0, which is almost right,
# but it's better to remove the mask and set all the data.
# Actually setlf.setMissing(0.0)  has no effect.  But doing what the code (in avariable.py)
# does will work:
#sftlf.missing_value = numpy.array([0.0],dtype=numpy.float32)
#sftlf._FillValue = numpy.array([0.0],dtype=numpy.float32)
# Still, those don't change the existing values of masked-out elements, and we need that.

ss = sftlf.getValue()
# ss.shrink_mask() will eliminate the mask, but we still need it...
mask = numpy.ma.getmaskarray(ss)

# shape of sftlf is 64x128
for i in range(64):
    for j in range(128):
        if mask[i,j]:
            # Note that setting sftlf[i,j] implicitly un-masks sftlf at i,j.
            sftlf[i,j] = 0.0
        else:
            sftlf[i,j] *= 100.

f.close()

