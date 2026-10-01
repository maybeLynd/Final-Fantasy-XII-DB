import json,struct
from pathlib import Path
W=Path(__file__).resolve().parent;r=json.loads((W/'raw.json').read_text());g={'struct':struct};exec((W/'retained/selected-sbn-functions.py').read_text(),g)
for m in ['btlctrl','mapctrl']:
 s=(W/'retained'/(m+'.sbn')).read_bytes();b=(W/'retained'/(m+'.dbg')).read_bytes();e=(W/'retained'/(m+'.ebp')).read_bytes();bl=[]
 for o,end in g['sbn_blocks'](s):
  L,bases,starts,t=g['sbn_group_read'](s,o);bl.append([s[a:s.index(b'\0',a,end)].decode('cp932') for a in starts])
 x=next(x for x in r['rows'] if x['module']==m and x['name']=='DEBUG_MENU');bind=next(x for x in r['bindings'] if x['module']==m and x['scope']==1)
 print('MODULE',m)
 for j in range(x['jump_pc'],x['jump_pc']+18):
  line,block,flag=struct.unpack_from('<HBB',b,bind['q0']+4*j)
  if flag:print(j,e[bind['code_start']+j:bind['code_start']+j+3].hex(),line,block,'one',bl[block][line-1],'zero',bl[block][line])
 print('labels neighborhood',bl[0][x['occurrences'][0]['index']:x['occurrences'][0]['index']+8])
 print('macro',[(bi,j,t) for bi,ts in enumerate(bl) for j,t in enumerate(ts) if 'MJPAGE_MAX' in t and ('#define' in t or '#macro' in t)])
