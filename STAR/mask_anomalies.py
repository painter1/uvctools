#!/env/python

from time import ctime
import numpy as np
import cdms2

def avg3x3( tmt, ta, t, j, i ):
    """Input is an array tmt(time,lat,lon) and indices t,j,i for time,lat,lon.
    We average the tmt quantities in the 3x3 lat,lon box around j,i (time is fixed)
    and return the average.  Where forming the 3x3 box runs across the limits if the index range,
    longitude is wrapped around, but latitude uses the appropriate max or min index
    (this average is weighted differently by the poles from anywhere else, but it's good enough
    for current purposes.)
    """
    lat = tmt.getLatitude()
    lon = tmt.getLongitude()
    latmax = len(lat)-1
    latmin = 0
    lonmax = len(lon)-1
    lonmin = 0
    jp1 = min( j+1, latmax )
    jm1 = max( j-1, latmin )
    if i==lonmax:
      ip1=lonmin
    else:
      ip1 = i+1
    if i==lonmin:
      im1=lonmax
    else:
      im1 = i-1
    # the arithmetic average doesn't take missing values into account:
    avg = (1./9.) * ( ta[t,jp1,im1] + ta[t,jp1,i] + ta[t,jp1,ip1] +
                      ta[t,j,im1] + ta[t,j,i] + ta[t,j,ip1] +
                      ta[t,jm1,im1] + ta[t,jm1,i] + ta[t,jm1,ip1] )
    return avg

def avg3x3ranges( tmt, tmtavg, tmtd, td, ta, tr, jr, ir ):
    """Input is an array tmt(time,lat,lon) and index ranges tr=(t1,t2),jr=(j1,j2),ir=(i1,i2)
    for time,lat,lon.  Instead of a range, a set of 3 specific values can be provided, playing
    the role of j-1,j,j+1 or i-1,i,i+1.
    We average the tmt quantities in the 3x3 lat,lon box around j,i (time is fixed)
    and return the average. """
    t1 = tr[0]
    t2 = tr[1]
    if len(jr)==2:
        j1 = jr[0]
        j2 = jr[1]
    else:
        jm = jr[0]
        jc = jr[1]
        jp = jr[2]
    if len(ir)==2:
        i1 = ir[0]
        i2 = ir[1]
    else:
        im = ir[0]
        ic = ir[1]
        ip = ir[2]
    # First compute tmtd, which counts the non-masked cells in the 3x3 box.
    td[ tmt.mask==True ] = 0
    if len(jr)==2 and len(ir)==2:
        tmtd[t1:t2,j1:j2,i1:i2] = ( td[t1:t2,j1+1:j2+1,i1-1:i2-1] + td[t1:t2,j1+1:j2+1,i1:i2] + td[t1:t2,j1+1:j2+1,i1+1:i2+1] +
                                  td[t1:t2,j1:j2,i1-1:i2-1] + td[t1:t2,j1:j2,i1:i2] + td[t1:t2,j1:j2,i1+1:i2+1] +
                                  td[t1:t2,j1-1:j2-1,i1-1:i2-1] + td[t1:t2,j1-1:j2-1,i1:i2] + td[t1:t2,j1-1:j2-1,i1+1:i2+1] )
    elif len(jr)==2 and len(ir)>2:
        tmtd[t1:t2,j1:j2,ic] = ( td[t1:t2,j1+1:j2+1,im] + td[t1:t2,j1+1:j2+1,ic] + td[t1:t2,j1+1:j2+1,ip] +
                                  td[t1:t2,j1:j2,im] + td[t1:t2,j1:j2,ic] + td[t1:t2,j1:j2,ip] +
                                  td[t1:t2,j1-1:j2-1,im] + td[t1:t2,j1-1:j2-1,ic] + td[t1:t2,j1-1:j2-1,ip] )
    elif len(jr)>2 and len(ir)==2:
        tmtd[t1:t2,jc,i1:i2] = ( td[t1:t2,jp,i1-1:i2-1] + td[t1:t2,jp,i1:i2] + td[t1:t2,jp,i1+1:i2+1] +
                                  td[t1:t2,jc,i1-1:i2-1] + td[t1:t2,jc,i1:i2] + td[t1:t2,jc,i1+1:i2+1] +
                                  td[t1:t2,jm,i1-1:i2-1] + td[t1:t2,jm,i1:i2] + td[t1:t2,jm,i1+1:i2+1] )
    elif len(jr)>2 and len(ir)>2:
        tmtd[t1:t2,jc,ic] = ( td[t1:t2,jp,im] + td[t1:t2,jp,ic] + td[t1:t2,jp,ip] +
                              td[t1:t2,jc,im] + td[t1:t2,jc,ic] + td[t1:t2,jc,ip] +
                              td[t1:t2,jm,im] + td[t1:t2,jm,ic] + td[t1:t2,jm,ip] )
    tmtd[ tmtd==0 ] = 1  # avoid divide-by-zero in places which are masked anyway
    # Now tmtavg is the average in the box, excluding masked cells
    ta.data[ta.mask==True] = 0
    ta.mask = False
    if len(jr)==2 and len(ir)==2:
        tmtavg[t1:t2,j1:j2,i1:i2] = (1./tmtd[t1:t2,j1:j2,i1:i2]) *\
            ( ta[t1:t2,j1+1:j2+1,i1-1:i2-1] + ta[t1:t2,j1+1:j2+1,i1:i2] + ta[t1:t2,j1+1:j2+1,i1+1:i2+1] +
              ta[t1:t2,j1:j2,i1-1:i2-1] + ta[t1:t2,j1:j2,i1:i2] + ta[t1:t2,j1:j2,i1+1:i2+1] +
              ta[t1:t2,j1-1:j2-1,i1-1:i2-1] + ta[t1:t2,j1-1:j2-1,i1:i2] + ta[t1:t2,j1-1:j2-1,i1+1:i2+1] )
    elif len(jr)==2 and len(ir)>2:
        tmtavg[t1:t2,j1:j2,ic] = (1./tmtd[t1:t2,j1:j2,ic]) *\
            ( ta[t1:t2,j1+1:j2+1,im] + ta[t1:t2,j1+1:j2+1,ic] + ta[t1:t2,j1+1:j2+1,ip] +
              ta[t1:t2,j1:j2,im] + ta[t1:t2,j1:j2,ic] + ta[t1:t2,j1:j2,ip] +
              ta[t1:t2,j1-1:j2-1,im] + ta[t1:t2,j1-1:j2-1,ic] + ta[t1:t2,j1-1:j2-1,ip] )
    elif len(jr)>2 and len(ir)==2:
        tmtavg[t1:t2,jc,i1:i2] = (1./tmtd[t1:t2,jc,i1:i2]) *\
            ( ta[t1:t2,jp,i1-1:i2-1] + ta[t1:t2,jp,i1:i2] + ta[t1:t2,jp,i1+1:i2+1] +
              ta[t1:t2,jc,i1-1:i2-1] + ta[t1:t2,jc,i1:i2] + ta[t1:t2,jc,i1+1:i2+1] +
              ta[t1:t2,jm,i1-1:i2-1] + ta[t1:t2,jm,i1:i2] + ta[t1:t2,jm,i1+1:i2+1] )
    elif len(jr)>2 and len(ir)>2:
        tmtavg[t1:t2,jc,ic] = (1./tmtd[t1:t2,jc,ic]) *\
            ( ta[t1:t2,jp,im] + ta[t1:t2,jp,ic] + ta[t1:t2,jp,ip] +
              ta[t1:t2,jc,im] + ta[t1:t2,jc,ic] + ta[t1:t2,jc,ip] +
              ta[t1:t2,jm,im] + ta[t1:t2,jm,ic] + ta[t1:t2,jm,ip] )
    print "tmtavg[329,1,92]=",tmtavg[329,1,92]        

f = cdms2.open('TMT_8.nc','r+')
tmt = f('tmt')
(tl,jl,il) = tmt.shape
tmtd = np.zeros( tmt.shape )
tmtavg = np.ma.zeros( tmt.shape )
td = np.ones( tmt.shape )
ta = np.ma.MaskedArray( tmt.data, tmt.mask, copy=True )
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (1,jl-1), (1,il-1) )    # interior
print "tmtavg[329,1,92]=",tmtavg[329,1,92]        
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (1,jl-1), (il-1,0,1) )  # W edge
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (1,jl-1), (il-2,il-1,0) ) # E edge
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (0,0,1), (1,il-1) )       # S edge
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (jl-2,jl-1,jl-1), (1,il-1) )  # N edge
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (0,0,1), (il-1,0,1) )     # SW corner
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (jl-2,jl-1,jl-1), (il-1,0,1) ) # NW corner
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (0,0,1), (il-2,il-1,0) )   # SE corner
avg3x3ranges( tmt, tmtavg, tmtd, td, ta, (0,tl), (jl-2,jl-1,jl-1), (il-2,il-1,0) ) # NE corner

if False:
    for t in range(tl):
        for j in range(jl):
            for i in [0,il-1]:
                #tmtavg[t,j,i] = avg3x3(tmt,ta,t,j,i)  # doesn't handle missing data
                tmtavg[t,j,i] = tmt[t,j,i]  # debugging
        for j in [0,jl-1]:
            for i in range(il):
                #tmtavg[t,j,i] = avg3x3(tmt,ta,t,j,i)  # doesn't handle missing data
                tmtavg[t,j,i] = tmt[t,j,i]  # debugging

tmtdiff = tmtavg - tmt
print "tmtdiff[329,1,92]=",tmtdiff[329,1,92]        
sdm1 = set([])
sdm2 = set([])
for cutoff in [100, 60, 50, 40, 30, 20, 10, 9]:
    inds1 = np.ma.where( tmtdiff>cutoff )
    inds2 = np.ma.where( tmtdiff<-cutoff )
    dm1 = [ (inds1[0][i],inds1[1][i],inds1[2][i]) for i in range(len(inds1[0])) ]
    dm2 = [ (inds2[0][i],inds2[1][i],inds2[2][i]) for i in range(len(inds2[0])) ]
    s1 = set(dm1) - sdm1
    s2 = set(dm2) - sdm2
    d1 = list(s1)
    d2 = list(s2)
    print "for",cutoff,", get",len(dm1),len(dm2),"; new:",len(d1),len(d2),"; samples:",
    if len(d1)>100: print d1[101],
    if len(d2)>100: print d2[101]
    else: print
    sdm1 = set(dm1)
    sdm2 = set(dm2)
# The real anomalies are _below_ the local average, i.e. dm1 etc.  The ones which are above are
# simply points near anomalies.
cutoff = 20
inds1 = np.ma.where( tmtdiff>cutoff )
dm1 = [ (inds1[0][i],inds1[1][i],inds1[2][i]) for i in range(len(inds1[0])) ]

# We just want to set the mask.  This works for TransientVariable, but it's better to do it for
# FileVariable because metadata, etc. are preserved.  The problem is that FileVariable has no
# direct way to set the mask.  So first do it to a TransientVariable, then copy all the data!
for ii in dm1:
    tmt.mask[ii] = True
tmtf = f['tmt']
tmtf[:,:,:] = tmt[:,:,:]

if not hasattr(f,'history'): f.history=""
f.history = f.history+",\n"+ctime()+\
    ": marked anomalous points as missing data"

f.close()

