import copy,hashlib,json
from pathlib import Path
r=json.loads(Path('Database/Tools/work/ASTRA/arena-init-result.json').read_text())
base=r['cases'][0]
def compact(c):
    for k,v in c.items():
        if k=='visited':print(k,json.dumps(v))
        elif k=='writes':
            print(k)
            for row in v:print(json.dumps(row))
        else:print(k,json.dumps(v))
print('BASE: every field, event and raw final byte')
compact(base)
def differences(a,b,path=''):
    if type(a)!=type(b):return [(path,b)]
    if isinstance(a,dict):
        if a.keys()!=b.keys():return [(path,b)]
        return [d for k in a for d in differences(a[k],b[k],path+'/'+str(k))]
    if isinstance(a,list):
        if len(a)!=len(b):return [(path,b)]
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in differences(x,y,path+'/'+str(i))]
    return [] if a==b else [(path,b)]
print('ALL OTHER CASES: complete differing leaves from BASE; changed-length arrays emitted whole')
for c in r['cases'][1:]+[r['mutant']]:
    print('CASE',c['name'])
    for p,v in differences(base,c):print(p,json.dumps(v))
print('TOP LEVEL METADATA',json.dumps({k:v for k,v in r.items() if k not in ('cases','mutant')}))
