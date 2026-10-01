"""Named F4 prerequisite for the already selected CD14/NULL-cleanup question.

Method A: constructor, root getter and F4 recomputation distinguish the normal
registered descriptor from an arbitrary/rebound one. Capture compiler physical
spans only; normal coverage/callee effects must still be established in reduction.
No game, new fixture platform, class census or repeat of earlier captures.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'softedges-array-descriptor-offset-code-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];o=struct.unpack_from('<H',d,p+20)[0]
targets={0x6373d0,0x632d80,0x63e410};rows=[]
for i in range(n):
 q=p+24+o+40*i
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000 in targets:rows.append((a+0x120000,b+0x120000,u+0x120000))
if len(rows)!=3 or {r[0] for r in rows}!=targets or sum(b-a for a,b,u in rows)>4096:
 raise ValueError('exact prerequisite physical identity/budget; revise method before retry')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[r[:2] for r in rows];sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=[list(x) for x in rows],
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 question='Which normal root/constructor/F4 conditions justify CD14 clearing the same array+8 slot60EFE0 reads?',
 limits='Physical original prerequisite spans, not live registration state, arbitrary descriptor invariance, caller reachability or lazy-init side effects.')
out.write_text(json.dumps(r,indent=2)+'\n')
print('Captured named original descriptor-offset prerequisites; arrayF4/null-cleanup composition not yet accepted')
