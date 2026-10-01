"""Two formatter boundaries plus exact literal/import; no native/CRT execution."""
import hashlib,importlib.util,json
from pathlib import Path
import struct,sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;out=W/'filecache-format-boundary-source-01.json'
if out.exists():raise ValueError('immutable capture exists')
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('cache_format_capture',W/'capture-index-path.py');C.RANGES=[(0x17d2e0,0x17d33b),(0x16d670,0x16d678)]
sys.argv=[sys.argv[0],str(out)];C.main();v=json.loads(out.read_text())
data=C.EXE.read_bytes()
if hashlib.sha256(data).hexdigest()!=C.SHA:raise ValueError('reference moved')
pe=struct.unpack_from('<I',data,60)[0];opt=pe+24;sz=struct.unpack_from('<H',data,pe+20)[0]
secs=[struct.unpack_from('<IIII',data,pe+24+sz+40*k+8) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
def read(r,n):
 for vs,va,size,off in secs:
  if va<=r and r+n<=va+size:return data[off+r-va:off+r-va+n]
 raise ValueError('unbacked original format bytes')
def cstr(r):
 b=bytearray()
 for k in range(512):
  x=read(r+k,1)
  if x==b'\0':return b.decode('ascii')
  b.extend(x)
 raise ValueError('unbounded format/import name')
literal=read(0x8f4438-C.BASE,3)
if literal!=b'%s\0':raise ValueError('original literal is not exact %s')
idir,isize=struct.unpack_from('<II',data,opt+112+8);found=[]
for k in range(isize//20):
 oft,ts,fwd,name,iat=struct.unpack('<IIIII',read(idir+k*20,20))
 if not any([oft,ts,fwd,name,iat]):break
 for n in range(65536):
  q=struct.unpack('<Q',read((oft or iat)+8*n,8))[0]
  if q==0:break
  va=C.BASE+iat+8*n
  if va==0x8c2f08:
   if q>>63:raise ValueError('unexpected ordinal import')
   found.append(dict(iat_va=hex(va),dll=cstr(name),name=cstr(q+2),lookup_raw=q.to_bytes(8,'little').hex()))
 else:raise ValueError('unbounded import table')
if len(found)!=1:raise ValueError('missing formatter import')
v.update(invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 wrapper_complete=True,annotation_prerequisite=load('format_roles',W/'validate-title-source-annotations.py').validate(v),
 exact_literal=dict(va='0x8f4438',bytes=literal.hex(),sha256=hashlib.sha256(literal).hexdigest()),
 static_format_import=found[0],limits='Local argument/literal/import identity; not loaded CRT/options/formatting effects or live path reachability')
out.write_text(json.dumps(v,indent=2)+'\n')
print('STATIC FORMAT',json.dumps(found[0]))
for q in v['ranges']:print(q['start'],q['sha256'])
