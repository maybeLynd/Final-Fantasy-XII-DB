import hashlib,importlib.util,json,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((HERE/'source.json').read_text())
p=Path(s['reader_path']);rb=p.read_bytes();assert sha(rb)==s['reader_sha256']
(HERE/'retained'/'02-existing-image-reader.py').write_bytes(rb)
sp=importlib.util.spec_from_file_location('verified_reader',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();assert sha(raw)==s['exe_sha256']
pe=struct.unpack_from('<I',raw,60)[0];er,es=struct.unpack_from('<II',raw,pe+24+112+3*8)
data=m.img_rd(raw,secs,m.IMG_LO+er,es)
all_entries=[struct.unpack_from('<III',data,i) for i in range(0,len(data),12)]
groups=[]
for b in s['bodies']:
 start=int(b['entry'],16);end=start+b['size'];assert m.img_rd(raw,secs,start,b['size']).hex()==b['raw_hex']
 entries=[x for x in all_entries if start<=m.IMG_LO+x[0]<end]
 assert len(entries)==3
 cursor=start;members=[]
 for a,z,u in entries:
  assert a+m.IMG_LO==cursor;cursor=z+m.IMG_LO
  h=m.img_rd(raw,secs,u+m.IMG_LO,4);flags=h[0]>>3;count=h[2]
  size=(4+2*count+3)&~3
  if flags&4:size+=12
  blob=m.img_rd(raw,secs,u+m.IMG_LO,size)
  parent=None
  if flags&4:
   parent=struct.unpack_from('<III',blob,size-12);assert parent==entries[0]
  members.append({'begin':hex(a+m.IMG_LO),'end':hex(z+m.IMG_LO),'unwind':hex(u+m.IMG_LO),'unwind_hex':blob.hex(),'flags':flags,'chain_parent':list(parent) if parent else None})
 assert cursor==end
 groups.append({'entry':b['entry'],'end':hex(end),'contiguous_entries':members})
import unicorn,capstone
s['pe_runtime_function_groups']=groups
s['retained_reader']='retained/02-existing-image-reader.py'
s['tool_modules']=[{'path':str(Path(mod.__file__).resolve()),'sha256':sha(Path(mod.__file__).read_bytes())} for mod in [unicorn,capstone]]
(HERE/'source.json').write_text(json.dumps(s,indent=2)+'\n')
print('PASS exact shipping bytes and two complete three-fragment chained RuntimeFunction groups; no code execution repeated.')
