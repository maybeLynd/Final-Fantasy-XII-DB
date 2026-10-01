"""Named queue slow insertion and renderer pumps; Method A only.

Original pdata spans are physical inputs. Completeness of original local CFG and
relevant callees must be established separately before semantic conclusions.
No process state, initialized callback queue, timing or thread observation.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'title-queue-slow-consumer-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong original image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0];rows=[]
for k in range(n):
 q=p+24+o+40*k
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000 in {0x1858a0,0x189570,0x189ce0}:rows.append([a+0x120000,b+0x120000,u+0x120000])
if rows!=[[0x1858a0,0x185a0f,0x1d54518],[0x189570,0x1897b1,0x1d5422c],[0x189ce0,0x18a11b,0x1d54000]]:raise ValueError('named pdata boundaries changed')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[x[:2] for x in rows];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=rows,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Original named physical spans only; no automatic transitive effects, semantic complete CFG, initialized state, timing, thread or lifetime proof.')
out.write_text(json.dumps(r,indent=2)+'\n');print('Named slow insertion/pump source available for bounded reduction')
