import os, cdms2, pprint

current_dict = {}
for dirpath,dirs,files in os.walk('.'):
    for file in files:
        if file[-3:]=='.nc':
            f=cdms2.open(dirpath+'/'+file)
            if hasattr(f,'tracking_id'):
                if file in current_dict.keys():     # already encountered file
                    if current_dict[file]!=f.tracking_id:
                        if isinstance(current_dict[file],set):
                            current_dict[file].add(f.tracking_id)
                        else:
                            print "warning - file %s has multiple tracking_ids!"%(file)
                            current_dict[file] = set([ f.tracking_id, current_dict[file] ])
                else:   # the normal case, file hasn't been seen before
                    current_dict[file] = f.tracking_id
            f.close()

pp = pprint.PrettyPrinter()
print "current_dict="
pp.pprint( current_dict )

