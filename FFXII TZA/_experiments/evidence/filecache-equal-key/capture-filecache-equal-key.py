"""Five bounded original boundaries, no native/live state or caller census."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
sys.dont_write_bytecode = True
W=Path(__file__).resolve().parent
out=W/'filecache-equal-key-source-01.json'
if out.exists(): raise ValueError('immutable source exists')
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('equal_capture',W/'capture-index-path.py')
C.RANGES=[(0x1d6a20,0x1d6a6d),(0x20b680,0x20b83b),
          (0x20b5f0,0x20b675),(0x20b0f0,0x20b126),(0x20c300,0x20c438)]
sys.argv=[sys.argv[0],str(out)]
C.main()
v=json.loads(out.read_text())
v.update(invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    wrapper_complete=True, annotation_prerequisite=load('equal_annotations',W/'validate-title-source-annotations.py').validate(v),
    limits='Local conditional insertion/hit boundaries only; no natural collision, insertion-domain census, CRT effects or lifetime proof')
# Selected static import declarations, from the same checked shipping image.
data=C.EXE.read_bytes()
if hashlib.sha256(data).hexdigest()!=C.SHA: raise ValueError('image moved')
pe=struct.unpack_from('<I',data,60)[0];opt=pe+24
ns=struct.unpack_from('<H',data,pe+6)[0];opsize=struct.unpack_from('<H',data,pe+20)[0]
secs=[struct.unpack_from('<IIII',data,pe+24+opsize+40*k+8) for k in range(ns)]
def read_rva(r,n):
    for vs,va,size,off in secs:
        if va<=r and r+n<=va+size:return data[off+r-va:off+r-va+n]
    raise ValueError('unbacked static import')
def cstr(r):
    out=bytearray()
    for k in range(512):
        b=read_rva(r+k,1)
        if b==b'\0':return out.decode('ascii')
        out.extend(b)
    raise ValueError('unbounded import name')
idir,isize=struct.unpack_from('<II',data,opt+112+8)
found=[]
for k in range(isize//20):
    oft,ts,fwd,name,iat=struct.unpack('<IIIII',read_rva(idir+k*20,20))
    if not any([oft,ts,fwd,name,iat]):break
    for n in range(65536):
        q=struct.unpack('<Q',read_rva((oft or iat)+8*n,8))[0]
        if q==0:break
        va=C.BASE+iat+8*n
        if va in [0x8c2b48,0x8c2b50]:
            if q>>63:raise ValueError('unexpected ordinal import')
            found.append(dict(iat_va=hex(va),dll=cstr(name),name=cstr(q+2),import_lookup_raw=q.to_bytes(8,'little').hex()))
    else:raise ValueError('unbounded import table')
if len(found)!=2:raise ValueError('missing release import declarations')
v['static_release_imports']=sorted(found,key=lambda x:x['iat_va'])
out.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
for q in v['ranges']:print('RANGE',q['start'],q['end_exclusive'],q['sha256'])
print('STATIC IMPORTS',json.dumps(v['static_release_imports']))
