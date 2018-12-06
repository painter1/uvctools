import debug
import sys, argparse
import cdms2, cdutil
from genutil import udunits

if True:
    # normal:
    levels_std = [ 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150,
                   100, 70, 50, 30, 20, 10]
    print "standard 17 levels"
else:
    # special for 72-level E3SM data:
    levels_std = [ 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10., 11.,
                   12., 15., 20., 25., 30., 40., 45., 50., 60., 70., 75., 80.,
                   90., 100., 110., 120., 130., 140., 150., 160., 170., 185., 200., 215.,
                   235., 250., 275., 300., 320., 350., 375., 400., 440., 480., 500., 550.,
                   600., 625., 660., 700., 720., 750., 770., 790., 800., 820., 830., 850.,
                   860., 870., 880., 890., 900., 915., 925., 935., 945., 950., 960., 1000.]
    levels_std.reverse()  # so it will be [ 1000., 960., ... 2.0, 1.0, 0.0 ]
    print ">>>>"
    print ">>>> WARNING, NON-STANDARD LEVELS <<<<"
    print "<<<<"

 #   ... mbar, converted from the default (in Pa) of logLinearInterpolation
 # Use this because logLinearInterpolation doesn't detect the units of its inputs.

def verticalize( T, hyam, hybm, ps ):
    """
    For data T with CAM's hybrid level coordinates, converts to pressure levels and may (depending
    on how the final if clause is set) interpolate to more standard (cdutil default) pressure level
    coordinates.  This function returns a temperature variable with pressure levels.
    The input arguments hyam, hybm, ps are the usual CAM veriables by that
    name.  Order of dimensions must be (lev,lat,lon).
    """
    if hyam is None or hybm is None or ps is None:
        raise Exception("In verticalize, missing one of hyam,hybm,ps: %s,%s,%s"%
                        ( getattr(hyam,'id',None), getattr(hybm,'id',None), getattr(ps,'id',None) ))

    p0 = 1000.   # mb
    # Convert p0 to match ps.  Later, we'll convert back to mb.  This is faster than
    # converting ps to millibars.
    if ps.units=='mb':
        ps.units = 'mbar' # udunits uses mb for something else
    tmp = udunits(1.0,'mbar')
    s,i = tmp.how(ps.units)
    p0 = s*p0 + i

    axhyam = hyam.getDomain()[0][0]
    axhybm = hybm.getDomain()[0][0]
    if not hasattr(axhyam,'axis'):  axhyam.axis = 'Z'
    if not hasattr(axhybm,'axis'):  axhybm.axis = 'Z'

    levels_orig = cdutil.vertical.reconstructPressureFromHybrid( ps, hyam, hybm, p0 )

    # At this point levels_orig has the same units as ps.  Convert to to mbar
    tmp = udunits(1.0,ps.units)
    s,i = tmp.how('mbar')
    levels_orig = s*levels_orig + i
    levels_orig.units = 'mbar'

    newT = cdutil.vertical.logLinearInterpolation( T, levels_orig, levels_std )
    return newT



if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Convert hybrid levels to pressure levels in T or ta")
    p.add_argument( "--infiles", dest="infiles", help="Names of input files (mandatory)", nargs='+',
                    required=True )
    p.add_argument( "--psfiles", dest="psfiles", help="Names of PS files, corresponding to the T files",
                    nargs='+', required=False )
    args = p.parse_args(sys.argv[1:])
    print "input args=", args
    for i,infn in enumerate(args.infiles):
        f = cdms2.open(infn)
        if args.psfiles is not None and len(args.psfiles)==len(args.infiles):
            g = cdms2.open( args.psfiles[i] )
            gvars = g.variables.keys()
        else:
            gvars = []
        fvars = f.variables.keys()
        print "jfp fvars=",fvars
        print "jfp gvars=",gvars
        if 'T' in fvars:    T = f('T')
        elif 'ta' in fvars: T = f('ta')
        else:               T = None
        if 'hyam' in fvars: hyam = f('hyam')
        else:               hyam = None
        if 'hybm' in fvars: hybm = f('hybm')
        else:               hybm = None
        if 'PS' in fvars:   ps = f('PS')
        elif 'ps' in fvars: ps = f('ps')
        elif 'PS' in gvars: ps = g('PS')
        elif 'ps' in gvars: ps = g('ps')
        else:               ps = None
        if T is None: continue

        newT = verticalize( T, hyam, hybm, ps )

        if newT.getTime() is not None:
            cdutil.times.setTimeBoundsMonthly(newT)
            t=newT.getTime()
            t.toRelativeTime("months since 1800")

        # Write output in NetCDF-3 format for compatibility with Ben Santer's software:
        cdms2.setNetcdf4Flag(0)
        cdms2.useNetcdf3()

        g = cdms2.open( 'ta_'+infn, 'w' )
        g.write( newT, id='ta' )
        g.close()
        f.close()
