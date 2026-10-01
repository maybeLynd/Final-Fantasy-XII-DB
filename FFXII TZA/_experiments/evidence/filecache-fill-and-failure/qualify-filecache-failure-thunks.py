"""Qualify retained inline-captured bytes; no recapture or native execution."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 out=W/'filecache-release-allocator-thunks-qualified-01.json'
 if out.exists():raise ValueError('immutable qualifier output exists')
 old=W/'filecache-release-allocator-thunks-source-01.json';v=json.loads(old.read_text())
 C=load('failure_thunk_reference',W/'capture-index-path.py')
 data=C.EXE.read_bytes()
 if hashlib.sha256(data).hexdigest()!=C.SHA or v.get('exe_sha256')!=C.SHA or v.get('driver_sha256')!=sha(W/'capture-index-path.py'):raise ValueError('retained reference/driver changed')
 pe=struct.unpack_from('<I',data,60)[0];opt=pe+24;sz=struct.unpack_from('<H',data,pe+20)[0]
 secs=[struct.unpack_from('<IIII',data,pe+24+sz+40*k+8) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
 def read(r,n):
  for vs,va,size,off in secs:
   if va<=r and r+n<=va+size:return data[off+r-va:off+r-va+n]
  raise ValueError('unbacked original bytes')
 for q in v['ranges']:
  blob=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']));a=int(q['start'],16)
  if blob!=read(a-C.BASE,len(blob)):raise ValueError('retained thunk differs from original')
 V=load('failure_thunk_roles',W/'validate-title-source-annotations.py')
 check=V.validate(v)
 def cstr(r):
  b=bytearray()
  for k in range(512):
   x=read(r+k,1)
   if x==b'\0':return b.decode('ascii')
   b.extend(x)
  raise ValueError('unbounded import name')
 idir,isize=struct.unpack_from('<II',data,opt+112+8);found=[]
 for k in range(isize//20):
  oft,ts,fwd,name,iat=struct.unpack('<IIIII',read(idir+k*20,20))
  if not any([oft,ts,fwd,name,iat]):break
  for n in range(65536):
   q=struct.unpack('<Q',read((oft or iat)+8*n,8))[0]
   if q==0:break
   va=C.BASE+iat+8*n
   if va==0x8c2b40:
    if q>>63:raise ValueError('unexpected ordinal')
    found.append(dict(iat_va=hex(va),dll=cstr(name),name=cstr(q+2),lookup_raw=q.to_bytes(8,'little').hex()))
  else:raise ValueError('unbounded import table')
 if len(found)!=1 or found[0]['name']!='malloc':raise ValueError('original malloc declaration missing')
 v.update(producer_complete=True,qualification_driver_sha256=sha(Path(__file__)),
     retained_source=dict(path=old.name,sha256=sha(old)),annotation_check=check,
     malloc_import_declaration=found[0],
     limits='Raw01 was executed as an inline bounded capture with tool exit0 but no prehashed named wrapper/outer receipt. This qualifier verifies exact retained bytes against shipping image and re-decodes roles, without recapturing or claiming that prior invocation had stronger receipts. Static malloc declaration, not loaded target/effect or natural failure proof.')
 out.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
 print('QUALIFIED RETAINED ORIGINAL THUNKS',len(v['ranges']),check['instruction_records'],json.dumps(found[0]))
if __name__=='__main__':main()
