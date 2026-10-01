"""Named global getter, callback enqueue and supplied callback boundaries.

Method A.189120 is MOV global/RET, not an object resolver. Keep queue fast stores,
slow helper effects and eventual callback scheduling separate. No live run.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'title-cleanup-callback-queue-source-01.json'
if out.exists():raise ValueError('immutable output exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0];rows=[];leaf=None
for k in range(n):
 q=p+24+o+40*k;vs,va,rs,ro=struct.unpack_from('<IIII',d,q+8)
 if 0x120000+va<=0x189120 and 0x189128<=0x120000+va+rs:leaf=d[ro+0x189120-0x120000-va:ro+0x189128-0x120000-va]
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000 in {0x185a90,0x17ecc0}:rows.append((a+0x120000,b+0x120000,u+0x120000))
if sorted(x[:2] for x in rows)!=[(0x17ecc0,0x17ecdb),(0x185a90,0x185ae6)] or leaf!=bytes.fromhex('488b057164df01c3'):raise ValueError('named callback/getter physical boundaries changed')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x189120,0x189128)]+[x[:2] for x in rows];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=[list(x) for x in rows],
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 limits='Exact original getter/enqueue/callback boundary spans. No initialized context/index/queue capacity, slow insertion effects, actual callback execution or scheduling/cancellation/lifetime proof.')
out.write_text(json.dumps(r,indent=2)+'\n');print('Captured named global/callback queue boundaries; native effects remain distinct')
