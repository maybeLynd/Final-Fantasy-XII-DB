import json,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-named-entry-line-convention');u=lambda b,o:struct.unpack_from('<I',b,o)[0]
rows=[]
for m,idx,want in [('evctrl',0x61,'test_load_flg'),('btlctrl',0x0d,'loop_flg'),('btlctrl',0x0e,'mapjump_menu_flg'),('mapctrl',0x52,'test'),('mapctrl',0x20,'curmenu')]:
 b=(P/'retained'/(m+'.dbg')).read_bytes();e=(P/'retained'/(m+'.ebp')).read_bytes();pool=u(b,8);T0=u(b,4);N=u(b,T0)
 names=[b[pool+u(b,T0+4+4*i):b.index(b'\0',pool+u(b,T0+4+4*i))].decode('cp932') for i in range(N)]
 base=u(e,0x10);vt=base+u(e,base+0x28);nv=u(e,vt);ds=[struct.unpack_from('<II',e,vt+4+8*i) for i in range(nv)]
 r=dict(module=m,index=idx,t0_count=N,descriptor_count=nv,t0_at_operand=names[idx] if idx<N else None,wanted=want,wanted_ordinals=[i for i,n in enumerate(names) if n==want],descriptor_hex=e[vt+4+8*idx:vt+12+8*idx].hex(),descriptor=ds[idx],nearby_names=[dict(i=i,n=n) for i,n in enumerate(names) if abs(i-idx)<=3])
 rows.append(r)
(W/'feasibility.json').write_text(json.dumps(dict(status='UNVALIDATED_PREPARATION_ONLY',rows=rows),indent=2)+'\n');print(json.dumps(rows,indent=2),flush=True)
