#!/usr/local/cdat/bin/python
""" get the status of datasets and of their files, from the esgcet database.
 The main purpose is to identify those datases which can be completed by
 downloading just a few more files."""
# This is straightforward but really slow...

# Usage:
# 1. export PYTHONPATH=$PYTHONPATH:/export/home/painter/src/esgf-contrib/estani/python/
# 2. Set the hard-coded inputs just below.  Review the code, as it is intended to be
#    changed as needed.
# 3. If you chose to make download lists, concatenate them and edit them as needed.
# Here are the most important inputs.  Change them here:
like = "'%GFDL%'"     # the "LIKE" part of the query to identify datasets to work on
make_dl_lists = True  # Set to True to make download lists, which is useful, but very much slower
                      # and confuses the output.  Otherwise set to False.

# imports copied from harvest_cmip5.py, maybe not all needed...
import sqlalchemy
import os,sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, sql, ForeignKeyConstraint, orm
import time, datetime
# imports added as needed...
from esgcet.config import loadConfig

sql_ds20 = "SELECT name FROM replica.datasets WHERE name LIKE "+like+" AND status=20;"
sql_nfa1 = "SELECT COUNT(*) FROM replica.files WHERE dataset_name='"

config = loadConfig(None)
engine = sqlalchemy.create_engine(config.get('replication', 'esgcet_db'), echo=False, pool_recycle=3600)

datasets = engine.execute( sql.text( sql_ds20 ) ).fetchall()
fmt = "%72s %12s %12s %12s %12s %12s %12s"
print fmt % ("dataset","files","status 0/10","status 20","status 30","status 100","status -1")
print fmt % (" ",      " ",    "no attempt","chose to dl","downloaded","verified","error")
for ds in datasets:
    dstr = ds[0]
    nfiles = engine.execute(sql.text( sql_nfa1+ds[0]+"';" ) ).fetchall()[0][0]
    nfiles010 = engine.execute(sql.text( sql_nfa1+ds[0]+"' AND status>=0 AND status<=10;" ) ).fetchall()[0][0]
    nfiles20 = engine.execute(sql.text( sql_nfa1+ds[0]+"' AND status=20;" ) ).fetchall()[0][0]
    nfiles30 = engine.execute(sql.text( sql_nfa1+ds[0]+"' AND status=30;" ) ).fetchall()[0][0]
    nfiles100 = engine.execute(sql.text( sql_nfa1+ds[0]+"' AND status=100;" ) ).fetchall()[0][0]
    nfiles_m1 = engine.execute(sql.text( sql_nfa1+ds[0]+"' AND status=-1;" ) ).fetchall()[0][0]
    print fmt % (dstr,nfiles,nfiles010,nfiles20,nfiles30,nfiles100,nfiles_m1)
    if make_dl_lists is False:
        continue
    if nfiles100<nfiles and nfiles100>0.5*nfiles:
        if dstr.find("mon.atmos")>0:
            if dstr.find(".historical.")>0 or dstr.find(".rcp85.")>0 or dstr.find(".rcp45.")>0\
               or dstr.find(".piControl.")>0:
                dpri = 10
                print ' '*72,"...urgent download candidate"
            else:
                dpri = 8
                print ' '*72,"...excellent download candidate"
        else:
            dpri = 6
            print ' '*72,"...good download candidate"
    elif nfiles100<nfiles:
        dpri = 2
    else:
        dpri = 0
    if dpri>2:
        # Create a download list for just this dataset.
        import replica_manager
        replica_manager.dataset_match = dstr
        # Use time to make the output filename unique.
        tt=time.localtime().__reduce__()[1][0]
        ts = '.'.join(str(i) for i in tt)
        outfile = "download_"+dstr+'_'+ts
        print "creating download list",outfile
        dataset_type = 'list.repo.pcmdi'  # You have to 'know' this one!  pcmdi is most common
        replica_manager.create_download_lists( outfile, dataset_type )
        # Probably the gsiftp fields of the download list will have to be edited to http-something.
        

