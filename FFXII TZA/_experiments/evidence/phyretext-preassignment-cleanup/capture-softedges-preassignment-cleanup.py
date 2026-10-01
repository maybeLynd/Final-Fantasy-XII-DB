"""Next selected question: CD14 zero-write and the called cleanup null boundary.
Reuse the already retained pointer patcher; capture only missing104B dependency.
Do not infer nonnull allocator/destructor effects or redo family classifications.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'softedges-preassignment-cleanup-code-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong reference')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0];rows=[]
for i in range(n):
 q=p+24+o+40*i
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000==0x5f03a0:rows.append((a+0x120000,b+0x120000,u+0x120000))
if len(rows)!=1 or rows[0][:2]!=(0x5f03a0,0x5f0408):raise ValueError('exact physical cleanup source identity')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C);C.RANGES=[rows[0][:2]]
sys.argv=[sys.argv[0],str(out)];C.main();r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entry=list(rows[0]),
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Missing original cleanup dependency only; no native allocator/game effect or complete pointer-patcher effects acceptance.')
out.write_text(json.dumps(r,indent=2)+'\n');print('Retained missing104B cleanup source; null/preassignment result still to reduce')
