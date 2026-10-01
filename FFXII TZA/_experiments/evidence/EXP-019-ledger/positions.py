import sys,json,struct,time,hashlib
from pathlib import Path
kit=Path(__file__).resolve().parents[4]/'Tools/analysis-kit/gfz-scripts'
sys.path.insert(0,str(kit));import runtime_probe as rp
assert len(sys.argv)==2
out=Path(sys.argv[1]);assert not out.exists()
found=rp.find_process('FFXII_TZA.exe');assert len(found)==1 and found[0][0]==12200
assert hashlib.sha256(Path(found[0][1]).read_bytes()).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
h=rp.k32.OpenProcess(rp.PROCESS_VM_READ|rp.PROCESS_QUERY_INFORMATION,False,12200);assert h
try:
 p=rp.Probe(h)
 def read(a,n):
  b=p.read(a,n);assert b is not None and len(b)==n;return b
 def num(a,f):return struct.unpack(f,read(a,struct.calcsize(f)))[0]
 assert read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES))==rp.CONTROL_BYTES
 pool=num(0x208e688,'<Q');assert num(0x208e6a0,'<i')==32
 rows=[]
 for i in range(32):
  u=pool+i*0xf50
  if not num(u,'<B')&1:continue
  a=num(u+0x10,'<Q')
  if not a:continue
  cls=num(a+3,'<B')>>5
  if cls not in (1,3):continue
  m=num(a+0xb8,'<Q')
  if not m:continue
  raw=read(m,12)
  rows.append(dict(slot=i,unit=u,actor=a,actor_class=cls,movement=m,group=num(u+0xe98,'<B'),position=struct.unpack('<3f',raw),raw=raw.hex()))
 result=dict(pid=12200,unix=time.time(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows)
 out.write_text(json.dumps(result,indent=2));print(json.dumps(rows))
finally:rp.k32.CloseHandle(h)
