import cdms2

import optparse
parser=optparse.OptionParser(usage="%prog [options]\nComputes linearegression of variable 1 of file 1 on variable 2 in file 2")
g1= optparse.OptionGroup(parser,"Input Options")
g2= optparse.OptionGroup(parser,"Processing Options")
g3= optparse.OptionGroup(parser,"Output Options")
g1.add_option("--file1",help="File 1",action="store",dest="filename_1")
g1.add_option("--file2",help="File 2",action="store",dest="filename_2")
g1.add_option("-v","--var1",help="Variable Name in File 1",action="store",dest="var1")
g1.add_option("--var2",help="Variable Name in File 2, set to VAR1 if not passed",action="store",dest="var2")
parser.add_option_group(g1)
g2.add_option("-n","--nlices",help="how many slices are read/written at once",type='int',dest="nslices",default=50)
parser.add_option_group(g2)
g3.add_option("-o","--out",help="Output File",action="store",dest="filename_out",default="concatenated.nc")
parser.add_option_group(g3)

(options,args) = parser.parse_args()
cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(0)

f1=cdms2.open(options.filename_1)
f2=cdms2.open(options.filename_2)

v1=f1[options.var1]
print 'Variable 1:',v1.shape
var2 = options.var2
if var2 is None:
   var2=options.var1

v2=f2[var2]
print 'Variable 2:',v2.shape

t1 = v1.getTime()
t2 = v2.getTime()
if t1.units!=t2.units:
   t2 = cdms2.createAxis(t2,copy=True)
   t2.toRelativeTime(t1.units)
if t1[-1]>=t2[0]:
   print "CAUTION: Variables overlap in time from",t2[0],"to",t1[-1],t1.units

f=cdms2.open(options.filename_out,"w")

n = v1.shape[0]
for i in range(0,n,options.nslices):
    print '%s: slices %i to %i (out of %i)' % (options.filename_1,i,i+options.nslices,n)
    s=v1(time=slice(i,i+options.nslices))
    f.write(s)
u=s.getTime().units
    
n = v2.shape[0]
for i in range(0,n,options.nslices):
    print '%s: slices %i to %i (out of %i)' % (options.filename_2,i,i+options.nslices,n)
    s=v2(time=slice(i,i+options.nslices))
    t=s.getTime()
    if u!=t.units:
       t.toRelativeTime(u)
    f.write(s)

f.close()

print 'Done: concatenated %s and %s into %s\n' % (options.filename_1,options.filename_2,options.filename_out)

