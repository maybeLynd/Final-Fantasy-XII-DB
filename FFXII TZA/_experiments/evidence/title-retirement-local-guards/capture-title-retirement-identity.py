"""Two missing named dependencies of retained24A680/181610/1B1960.

Method A. Do not recapture the retained title/retirement body or invent cancellation
from a function name. The manager getter is a verified8B MOV/RET leaf; its
key producer has a checked normal pdata span. No pending-state/game observation.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'title-retirement-identity-source-01.json'
if out.exists():raise ValueError('immutable output exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0];rows=[];getter=None
for i in range(n):
 q=p+24+o+40*i;vs,va,rs,ro=struct.unpack_from('<IIII',d,q+8)
 if 0x120000+va<=0x1b1c00 and 0x1b1c08<=0x120000+va+rs:getter=d[ro+0x1b1c00-0x120000-va:ro+0x1b1c08-0x120000-va]
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000==0x1b1440:rows.append((a+0x120000,b+0x120000,u+0x120000))
if len(rows)!=1 or rows[0][:2]!=(0x1b1440,0x1b14df) or getter!=bytes.fromhex('488b05e1f5dc01c3'):raise ValueError('named dependency boundary/identity failed')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x1b1c00,0x1b1c08),rows[0][:2]];sys.argv=[sys.argv[0],str(out)];C.main();r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=[list(x) for x in rows],
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 limits='Missing manager/key producer source only. No full transitive cancellation/drain, resource lifetime, initialized manager/ticket state or natural teardown reachability claim.')
out.write_text(json.dumps(r,indent=2)+'\n');print('Captured missing retirement manager/key identities only')
