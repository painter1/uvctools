import cdms2
import debug
f=cdms2.open('~/metrics_data/b1850_ANN_climo.nc')  # this comes from ACME output
vars=f.variables.keys()
vars.sort()
from metrics.packages.amwg.derivations.massweighting import weighting_choice
g=open('weighting_choice','w')
for vn in vars:
  var = f(vn)
  choice = weighting_choice(var)
  units = getattr(var,'units',None)
  if units=="":  units='""'
  try:
      levdim = var.getLevel() is not None
  except:
      levdim = None  # happens for nbdate
  g.write('variable %-20s weighting %s\tlevel? %s \tunits %s\n' % (vn,choice,levdim,units) )
g.close()
