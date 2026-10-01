"""Original pump caller and exact5B queue-consumer tail; Method A only.

17D6E0 entry fragment is pinned; use a reducer to verify normal CFG/caller dataflow.
185C20 lacks pdata here: only its original5B unconditional tail is claimed.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'title-queue-pump-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0];rows=[];leaf=None
for k in range(n):
 q=p+24+o+40*k;vs,va,rs,ro=struct.unpack_from('<IIII',d,q+8)
 if 0x120000+va<=0x185c20 and 0x185c25<=0x120000+va+rs:leaf=d[ro+0x185c20-0x120000-va:ro+0x185c25-0x120000-va]
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  for j in range(ro,ro+rs-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000==0x17d6e0:rows.append([a+0x120000,b+0x120000,u+0x120000])
if rows!=[[0x17d6e0,0x17d874,0x1d537c8]] or leaf!=bytes.fromhex('e90b060000'):raise ValueError('pump/tail original identities changed')
s=importlib.util.spec_from_file_location('capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[rows[0][:2],(0x185c20,0x185c25)];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=rows,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Exact pump original span plus5B unconditional tail only. No larger tail function boundary, complete caller CFG, context initialization, actual call/thread/frame/lifetime proof without reduction.')
out.write_text(json.dumps(r,indent=2)+'\n');print('Original pump/tail source available for specific dataflow reduction')
