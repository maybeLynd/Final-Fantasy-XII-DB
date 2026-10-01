"""Specific original queue consumer, Method A; candidate is not proof.

125B original pdata boundary pinned before capture through shared reviewed roles.
Local CFG and same-context queue dataflow must be checked in the reducer.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'title-queue-consumer-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0];rows=[]
for k in range(n):
 q=p+24+o+40*k
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000==0x186230:rows.append([a+0x120000,b+0x120000,u+0x120000])
if rows!=[[0x186230,0x1862ad,0x1d52a90]]:raise ValueError('consumer pdata changed')
s=importlib.util.spec_from_file_location('capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[rows[0][:2]];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=rows,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Original physical source only. Complete normal CFG, pair identity/local meaning requires reduction; natural scheduling, live initialization, callback mutations and lifetime not proved.')
out.write_text(json.dumps(r,indent=2)+'\n');print('Original specific queue consumer source captured')
