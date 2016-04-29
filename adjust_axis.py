"""This script is for changing the values of an axis to match the same axis in a reference file.
 Normaly you will run this from the shell.  Example:
   python adjust_axis.py time file_to_change.nc reference_file.nc
 The axis in both files is required to have the same length, units, and
 bounds (within a small tolerance).
"""

filen = 'test.nc'
axisname = 'time'
reffilen = 'testref.nc'

import cdms2, numpy, sys

def adjust_axis( filen, axisname, reffilen ):
    print "adjusting axis",axisname,"of file",filen,"from",reffilen
    if filen==reffilen:
        print "WARNING, files are the same"
        return
    f = cdms2.open( filen, 'r+' )
    g = cdms2.open( reffilen, 'r+' )
    axis = f[axisname]
    refaxis = g[axisname]
    if axis is None:
        print "ERROR, axis",axisname,"is not in",filen
        return
    if refaxis is None:
        print "ERROR, axis",axisname,"is not in",reffilen
        return
    if len(axis)!=len(refaxis):
        print "ERROR, axis",axisname,"has different lengths in the two files!"
        print "file",filen,"length",len(axis)
        print "file",reffilen,"length",len(refaxis)
        return
    if getattr(axis,'units',None)!=getattr(refaxis,'units',None):
        print "ERROR, axis",axisname,"has different units in the two files!"
        print "file",filen,"units",getattr(axis,'units',None)
        print "file",reffilen,"units",getattr(refaxis,'units',None)
        return
    bnds = f( getattr(axis,'bounds',None) )
    refbnds = f( getattr(axis,'bounds',None) )
    if not numpy.allclose(bnds,refbnds):
        print "ERROR, axis",axisname,"has different bounds in the two files!"
        print "file",filen,"bounds",bnds
        print "file",reffilen,"bounds",refbnds
        return

    # axis[:] = refaxis[:] grows the file filen without bound, I don't know why.
    for i in range(len(axis)):
        axis[i] = refaxis[i]

    f.close()
    g.close()

if __name__ == '__main__':
    if len( sys.argv )>=4:
        axisname = sys.argv[1]
        filen = sys.argv[2]
        reffilen = sys.argv[3]
    adjust_axis( filen, axisname, reffilen )
