"""Prepared mapped-member child-link question, exact two original dependencies.
59E070's retained calls59B430/59AC00 prepare the context before59E300.
Capture physical compiler spans, not automatic semantic function acceptance.
No census, fresh resource read, native execution or live initialization.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'softedges-mapping-builders-code-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong reference')
parent=W/'softedges-loader-parent-code-01.json';p=json.loads(parent.read_text())
if p.get('wrapper_complete') is not True:raise ValueError('parent capture incomplete')
ix={i['pc']:i for q in p['ranges'] for i in q['instructions']}
if (ix['0x59e1ea']['mnemonic'],ix['0x59e1ea']['args'])!=('call','0x59b430') or (ix['0x59e227']['mnemonic'],ix['0x59e227']['args'])!=('call','0x59ac00'):raise ValueError('required parent calls changed')
pe=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,pe+6)[0];op=struct.unpack_from('<H',d,pe+20)[0];rows=[]
for i in range(n):
 q=pe+24+op+40*i
 if d[q:q+8].rstrip(b'\0')==b'.pdata':
  size,off=struct.unpack_from('<II',d,q+16)
  for j in range(off,off+size-11,12):
   a,b,u=struct.unpack_from('<III',d,j)
   if a+0x120000 in (0x59b430,0x59ac00):rows.append((a+0x120000,b+0x120000,u+0x120000))
if len(rows)!=2 or sum(b-a for a,b,u in rows)>4096:raise ValueError('dependency identity/bounded extent changed')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C);C.RANGES=[r[:2] for r in rows]
sys.argv=[sys.argv[0],str(out)];C.main();r=json.loads(out.read_text());r.update(wrapper_complete=True,pdata_entries=[list(x) for x in rows],
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),parent_source_sha256=hashlib.sha256(parent.read_bytes()).hexdigest(),
 limits='Physical original dependencies for mapped-member construction; no native/live mapping initialization or normal loader acceptance.')
out.write_text(json.dumps(r,indent=2)+'\n')
print('Captured original context preparation dependencies; mapped-child result not yet accepted')
