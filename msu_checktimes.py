#!/env python

# Check times, branches, etc. for MSU data.

import cdms2, os, glob, cdtime

inputroot = '/Users/painter1/data/MSU_Data/'

#models = ['CCSM4', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'GISS-E2-R',\
#    'HadGEM2-CC', 'IPSL-CM5A-LR', 'MIROC-ESM', 'MIROC5', 'MRI-CGCM3', 'inmcm4' ]
models = ['GISS-E2-H','GISS-E2-R']
ensembles_piControl = { 'ACCESS1-0':['r1i1p1'], 'bcc-csm1-1-m':['r1i1p1'], 'CCSM4':['r1i1p1'],\
                            'CESM1-BGC':['r1i1p1'], 'CESM1-WACCM':['r2i1p1'],\
                            'CMCC-CESM':['r1i1p1'], 'CMCC-CMS':['r1i1p1'], 'CNRM-CM5':['r2i1p1'],\
                            'CSIRO-Mk3-6-0':['r1i1p1'], 'CanESM2':['r1i1p1'], \
                            'GFDL-CM3':['r1i1p1'], 'GFDL-ESM2G':['r1i1p1'], 'GFDL-ESM2M':['r1i1p1'],\
                            'GISS-E2-R':['r1i1p1','r1i1p2','r1i1p3'],\
                            'HadGEM2-AO':['r1i1p1'], 'HadGEM2-CC':['r1i1p1'], 'HadGEM2-ES':['r1i1p1'],\
                            'IPSL-CM5A-LR':['r1i1p1'], 'IPSL-CM5A-MR':['r1i1p1'], 'IPSL-CM5B-LR':['r1i1p1'],\
                            'MIROC-ESM':['r1i1p1'], 'MIROC-ESM-CHEM':['r1i1p1'], 'MIROC5':['r1i1p1'],\
                            'MPI-ESM-MR':['r1i1p1'], 'MRI-CGCM3':['r2i1p1'], 'NorESM1-ME':['r1i1p1'],\
                            'inmcm4':['r1i1p1']  }
ensembles_historical = { 'ACCESS1-0':['r1i1p1'], 'bcc-csm1-1-m':['r1i1p1'], 'CCSM4':['r1i1p1','r2i1p1','r3i1p1'],\
                             'CESM1-BGC':['r1i1p1'],\
                             'CESM1-WACCM':['r2i1p1'], 'CMCC-CESM':['r1i1p1'], 'CMCC-CMS':['r1i1p1'],\
                             'CNRM-CM5':['r1i1p1','r2i1p1','r4i1p1'], 'CSIRO-Mk3-6-0':['r1i1p1','r10i1p1'],\
                             'CanESM2':['r1i1p1','r2i1p1','r3i1p1','r4i1p1','r5i1p1'],\
                             'GFDL-CM3':['r1i1p1'], 'GFDL-ESM2G':['r1i1p1'], 'GFDL-ESM2M':['r1i1p1'],\
                             'GISS-E2-H':['r1i1p3','r6i1p1'],\
                             'GISS-E2-R':['r1i1p1','r1i1p2','r1i1p3','r4i1p3'],\
                             'HadGEM2-AO':['r1i1p1'], \
                             'HadGEM2-CC':['r1i1p1','r2i1p1','r3i1p1'], 'HadGEM2-ES':['r1i1p1','r2i1p1'],\
                             'IPSL-CM5A-LR':['r1i1p1','r2i1p1'], 'IPSL-CM5A-MR':['r1i1p1'], 'IPSL-CM5B-LR':['r1i1p1'],\
                             'MIROC-ESM':['r1i1p1'], 'MIROC-ESM-CHEM':['r1i1p1'], 'MIROC5':['r1i1p1'],\
                             'MPI-ESM-MR':['r1i1p1'], 'MRI-CGCM3':['r1i1p1'], 'NorESM1-ME':['r1i1p1'],\
                             'inmcm4':['r1i1p1']  }
ensembles_historicalExt = { 'GISS-E2-H':['r1i1p3','r6i1p1'],\
                                'GISS-E2-R':['r1i1p1','r1i1p2','r1i1p3','r4i1p3'] }

def print_times_branch( inputroot, model, experiment, ensemble, piControl_units=None, historical_units=None ):
    pspath = inputroot+experiment+'/'+model+'/'+ensemble+'/atmos/mon/ps/'
    tspath = inputroot+experiment+'/'+model+'/'+ensemble+'/atmos/mon/ts/'
    tapath = inputroot+experiment+'/'+model+'/'+ensemble+'/atmos/mon/ta/'
    lsps = glob.glob(pspath+'ps_*')
    lsps.sort()
    lsts = glob.glob(tspath+'ts_*')
    lsts.sort()
    lsta = glob.glob(tapath+'ta_*')
    lsta.sort()

    if len(lsts)==0:
        print 'files',tspath+'ts_*','not found'
        return
        
    f=cdms2.open(lsts[0])
    ts0=f['ts']
    t0=ts0.getTime()
    g=cdms2.open(lsts[-1])
    ts1=g['ts']
    t1=ts1.getTime()

    calstr = t0.calendar
    cal=cdtime.StandardCalendar
    # For calendar attribute meanings, cf CF Conventions 4.4.1.
    #  For cdtime calendars, c.f. http://esg.llnl.gov/cdat/cdms_html/cdms-3.htm
    # I assume that an experiment and its parent have the same calendar, as do all data of the same experiment.
    if calstr=="365_day": cal=cdtime.NoLeapCalendar
    elif calstr=="noleap": cal=cdtime.NoLeapCalendar
    elif calstr=="gregorian": cal=cdtime.MixedCalendar  # not cdtime.Gregorian calendar!
    elif calstr=="standard": cal=cdtime.StandardCalendar
    elif calstr=="proleptic_gregorian": cal=cdtime.GregorianCalendar
    elif calstr=="360_day": cal=cdtime.Calendar360
    elif calstr=="julian": cal=cdtime.JulianCalendar
    else: print "don't understand calendar",calstr

    tmin=t0[:].min()
    tmax=t1[:].max()
    tb0 = f[ t0.bounds ]
    tb1 = g[ t1.bounds ]
    tbmin = tb0[0,0]
    tbmax = tb1[-1,1]
    units = t0.units

    # Convert final time and time bound to same units as initial times
    tmax  = cdtime.reltime( tmax,  t1.units ).tocomp(cal).torel(units,cal).value
    tbmax = cdtime.reltime( tbmax, t1.units ).tocomp(cal).torel(units,cal).value

    if f.parent_experiment_id=='piControl' and piControl_units:
        parent_units = piControl_units
    elif f.parent_experiment_id=='historical' and historical_units:
        parent_units = historical_units
    else:
        parent_units = ''

    if len(lsts)==1:
        print "In",tspath,',\n   ',lsts[0],\
            "\nhas time centers running from",tmin,"to",tmax,\
            "and time bounds from",tbmin,"to",tbmax,units,'(',calstr,')'
    else:
        print "In",tspath,',\n   ',lsts[0],"...\n...",lsts[-1],\
            "\nhave time running from",tmin,"to",tmax,\
            "and time bounds from",tbmin,"to",tbmax,units,'(',calstr,')'
    tminrel  = cdtime.reltime( tmin, units )
    tmincomp = tminrel.tocomp(cal)
    tbminrel  = cdtime.reltime( tbmin, units )
    tbmincomp = tbminrel.tocomp(cal)
    print "i.e.,",tmincomp, 'to', cdtime.reltime(tmax,units).tocomp(cal)," and ",\
        tbmincomp,"to",cdtime.reltime(tbmax,units).tocomp(cal)
    if f.parent_experiment_id==None or f.parent_experiment_id=='N/A':
        print "and there is no parent."
    else:
        print "and branch(es) from ",f.parent_experiment_id,\
            getattr(f,'parent_experiment_rip','(rip not available)')," at parent time",f.branch_time,\
            parent_units
        if len(parent_units)>0:
            tprel  = cdtime.reltime(float(f.branch_time),parent_units)
            tpcomp = tprel.tocomp(cal)
            # The branch time is in the parent's units and should be the same moment of time as the
            # initial time for this experiment.  If it isn't, the difference is the "offset" which
            # needs to be applied to times (of this experiment or its parent) to make their data
            # strictly comparable.
            tmrp = tbmincomp.torel(parent_units,cal)
            u = parent_units.split(' ')[0]  # usually 'days'
            print "i.e.,",tpcomp," so the offset is", tmrp.value-tprel.value,u
    print '\n'
    f.close()
    g.close()
    return units

def print_ts_centering( inputroot, model, experiment, ensemble, piControl_units=None, historical_units=None ):
    tspath = inputroot+experiment+'/'+model+'/'+ensemble+'/atmos/mon/ts/'
    lsts = glob.glob(tspath+'ts_*')
    lsts.sort()
    if len(lsts)==0:
        print 'files',tspath+'ts_*','not found'
        return
    f=cdms2.open(lsts[0])
    ts = f['ts']
    t  = ts.getTime()
    time_bnds = f['time_bnds']
    print "cell_methods=",ts.cell_methods," t[0]=",t[0]," in bounds",time_bnds[0,:]
    # Note we see that cell_methods contains "time: mean" and bounds is [0. 31.] for January (The
    # first month for Hadley is November so bounds is [0. 30.]).  Many models also provide the
    # sampling interval used in computing this mean.  CF CF Conventions section 7.3 and 7.3.2.

# To print information on time range and branch times:
for model in models:
    print '\n',model,'----------------\n'
    if model in ensembles_piControl.keys():
        for ensemble in ensembles_piControl[model]:
            piControl_units = print_times_branch( inputroot, model, 'piControl', ensemble )
            if model.find("IPSL")==0 or model=="GISS-E2-R" or model=="GISS-E2-H" or model=="CCSM4":
                # IPSL, GISS, and CCSM4 follow special standards  :-)
                piControl_units = "years since 0"          # used for branch time, not internally in piControl
    else:
        piControl_units = None
    if model in ensembles_historical.keys():
        for ensemble in ensembles_historical[model]:
            historical_units = print_times_branch( inputroot, model, 'historical', ensemble, piControl_units )
            if model.find("IPSL")==0 or model=="GISS-E2-R" or model=="GISS-E2-H" or model=="CCSM4":
                # IPSL, GISS, and CCSM4 follow special standards  :-)
                historical_units = "years since 0"          # used for branch time, not internally in piControl
            #print_times_branch( inputroot, model, 'rcp85', ensemble, piControl_units, historical_units )
            print_times_branch( inputroot, model, 'historicalExt', ensemble, piControl_units, historical_units )

# To print information on time centering and averaging:
for model in models:
    print '\n',model,'----------------\n'
    for ensemble in ensembles_historical[model]:
        print_ts_centering( inputroot, model, 'historical', ensemble )

