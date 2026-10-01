"""Missing named parent prerequisite, Method A only.

The retained registrar sends6372A0 through arg6 to descriptor+78.6373D0
goes through arg2 to+70, so it must not be called the parent/root getter.
Capture only the original pdata span for6372A0; no lazy-init effects claim.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'softedges-array-parent-getter-code-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0];rows=[]
for i in range(n):
 q=p+24+o+40*i
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000==0x6372a0:rows.append((a+0x120000,b+0x120000,u+0x120000))
if rows:raise ValueError('unexpected pdata for verified two-instruction parent leaf')
leaf=None
for i in range(n):
 q=p+24+o+40*i;vs,va,rs,ro=struct.unpack_from('<IIII',d,q+8)
 if 0x120000+va<=0x6372a0 and 0x6372a8<=0x120000+va+rs:
  leaf=d[ro+0x6372a0-0x120000-va:ro+0x6372a8-0x120000-va]
if leaf!=bytes.fromhex('488d05c90f6c02c3'):raise ValueError('complete LEA/RET original parent identity changed')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x6372a0,0x6372a8)];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=[list(x) for x in rows],
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 limits='Complete two-instruction original parent-return leaf; no constructor execution, live registration or lifetime established.')
out.write_text(json.dumps(r,indent=2)+'\n');print('Captured missing exact parent-getter source, no parent conclusion yet')
