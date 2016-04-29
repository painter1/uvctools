# Reads a NetCDF file of variables, and regrids lat-lon to a 12x24 (15 degree) grid.
# Levels are left alone.  To get a different grid size, change nlat,nlon below.
# This should be run from the shell, with one argument: the name of the input file.
# The result will be written to a new file, name generated from the input filename.

import sys, cdms2, numpy
nlat = 13 # 15 degree
nlon = 25 # 15 degree
#nlat = 10 # 20 degree
#nlon = 19 # 20 degree

def coarsenVars( filen, newfilen ):
    """Reads a NetCDF file, filen, and writes a new file, newfilen, containing all its variables,
    but regridded in its horizontal axeseb to a 12x14 (15 degree) lat-lon grid.
    """
    latbnds = numpy.linspace(-90,90,nlat)
    lat = 0.5*( latbnds[1:]+latbnds[:-1] )
    lataxis=cdms2.createAxis( lat, id='lat' )
    lonbnds = numpy.linspace(0,360,nlon)
    lon = 0.5*( lonbnds[1:]+lonbnds[:-1] )
    lonaxis=cdms2.createAxis( lon, id='lon' )
    newgrid=cdms2.createRectGrid(lataxis, lonaxis)

    f = cdms2.open(filen)
    nf = cdms2.open(newfilen,'w')
    for varn in f.variables.keys():
        print "working on",varn
        var = f(varn)
        if var.getGrid() is None:
            print varn,"has no grid!"
            continue
        newvar = var.regrid(newgrid)   # works even if var has levels
        newvar.id = var.id         # before, id was var.id+'_CdmaRegrid'
        nf.write(newvar)
    for attr in f.attributes.keys():
        setattr(nf,attr,getattr(f,attr))
    if hasattr(nf,'history'):
        nf.history = nf.history + '; some variables deleted'
    f.close()
    nf.close()

filen = sys.argv[1]
coarsenVars( filen, 'c_'+filen )
