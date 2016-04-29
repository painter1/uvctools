# Reads a NetCDF file of land (LMWG) variables, and writes a new file containing
# a subset of these variables.  This should be run from the shell, with one argument:
# the name of the input file.

import sys, cdms2

NecessaryLandVariables = [
    'BTRAN', 'FCEV', 'FCOV', 'FCTR', 'FGEV', 'FGR', 'FIRA', 'FIRE', 'FLDS', 'FSA', 'FSDS', 'FSDSNDLN',
    'FSDSNI', 'FSDSVDLN', 'FSDSVI', 'FSH', 'FSM', 'FSNO', 'FSR', 'FSRDLN', 'FSRNI', 'FSRVDLN', 'FSRVI',
    'H2OSNO', 'H2OSOI', 'LAISHA', 'LAISUN', 'QCHARGE', 'QDRAI', 'QOVER', 'QRGWL', 'QSOIL', 'QVEGE',
    'QVEGT', 'RAIN', 'SNOW', 'SNOWDP', 'SOILICE', 'SOILLIQ', 'SOILPSI', 'TLAI', 'TLAKE', 'TSA', 'TSOI',
    'WA', 'WT', 'ZWT']

def trimLandVars( filen, newfilen ):
    """Reads a NetCDF file, filen, and writes a new file, newfilen, containing a
    subset of its variables.  The subset is determined by the global NecessaryLandVariables
    """
    f = cdms2.open(filen)
    nf = cdms2.open(newfilen,'w')
    for varn in NecessaryLandVariables:
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
trimLandVars( filen, 't_'+filen )
