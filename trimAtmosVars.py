# Reads a NetCDF file of atmosphere (AMWG) variables, and writes a new file containing
# a subset of these variables.  This should be run from the shell, with one argument:
# the name of the input file.

import sys, cdms2

NecessaryAtmosVariables = [
    'FSNS', 'FLNS', 'FLUT', 'FSNTOA', 'FLNT', 'FSNT', 'SHFLX', 'LHFLX', 'QFLX', 'OCNFRAC', 'T',
    'PS', 'hyam', 'hybm'
]

def trimAtmosVars( filen, newfilen ):
    """Reads a NetCDF file, filen, and writes a new file, newfilen, containing a
    subset of its variables.  The subset is determined by the global NecessaryAtmosVariables
    """
    f = cdms2.open(filen)
    nf = cdms2.open(newfilen,'w')
    for varn in NecessaryAtmosVariables:
        if varn in f.variables.keys():
            var = f(varn)
            nf.write( var )
    for attr in f.attributes.keys():
        setattr(nf,attr,getattr(f,attr))
    if hasattr(nf,'history'):
        nf.history = nf.history + '; some variables deleted'
    f.close()
    nf.close()

filen = sys.argv[1]
trimAtmosVars( filen, 't_'+filen )
