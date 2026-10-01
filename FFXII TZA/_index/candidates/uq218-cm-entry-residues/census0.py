import collections, struct
from lib import *
fs = cm_files()
print('files', len(fs))
tags = collections.Counter(); kinds = collections.Counter(); var = collections.Counter()
for p in fs:
    d, es = cm_entries(p)
    var[struct.unpack_from('<I', d, 4)[0]] += 1
    for t, o in es:
        tags[t] += 1
        kinds[(t, struct.unpack_from('<I', d, o+4)[0])] += 1
print(var)
print(sorted(tags.items()))
print(sorted(kinds.items()))
