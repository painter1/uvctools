#!/usr/apps/esg/cdat6.0a/bin/python

# This is based on pymd5.  It sums up bytes read from a file, but the real purpose is to
# measure speed of reading the file, so that I can tinker with the chunk size and find
# the best one.

chunksize = 256*256

import sys, struct, timeit, cdms2
global_filename = None

def repeat_sum( filename ):
    global global_filename
    global_filename = filename
    global chunksize
    for chunksize in range(-1,32*1024,2*1024):
        # On gdo2, 16384 is a good chunksize.
        ttime = timeit.timeit( testsum, number=1 )
        fsum,pos = testsum()
        print chunksize, ttime, fsum, pos

def testsum():
    if chunksize>=0:
        return testsum_pyopen()
    else:
        return testsum_cdms()

def testsum_pyopen():
    # For performance on big files, this reads the file one chunk at a time.
    fsum = 0
    with open(global_filename,'rb') as f: 
        for chunk in iter(lambda: f.read(chunksize), ''):
#            for i in range(0,len(chunk),4):
#                if i+4>len(chunk):
#                    continue
#                word = chunk[i:i+4]
#                fsum += struct.unpack( 'i', word )[0]
            pos = f.tell()   # final value will be file size
    return fsum, pos

def testsum_cdms():
    fsum = 0
    f = cdms2.open(global_filename)
#    for varn in f.variables.keys():
#       maxsize = -1
#        var = f[varn]
#        if var.size()>maxsize:
#            maxvarn = varn
#            maxsize = var.size()
#    var = f(maxvarn)   # This reads the entire variable into memory
    sumsize = 0
    for varn in f.variables.keys():
        if varn in ['time_written','date_written']:
            continue    # f(varn) doesn't work because contents is a string.
        var = f(varn)   # This reads the entire variable into memory
        sumsize += var.size
    f.close()
    return 6, sumsize

if __name__ == '__main__':
    if len( sys.argv ) > 1:
        file = sys.argv[1]
        repeat_sum( file )
    else:
        print "please provide a filename"

