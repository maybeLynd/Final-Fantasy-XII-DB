"""Named original PArray<ShaderParameterDefinition>::m_els callback only.

Method A is sufficient for the calling convention and status propagation.
No new execution, resource extraction, class census or binding/reachability proof.
The leaf boundary is the entire two-exit entry CFG, not a first-RET heuristic.
Existing normal60EFE0 source is retained rather than captured again.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent; ROOT=W.parents[4]
out=W/'softedges-elements-callback-source-01'
if out.exists():raise ValueError('immutable source exists')
sha=lambda z:hashlib.sha256(z).hexdigest()
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if sha(d)!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong EXE')
p=struct.unpack_from('<I',d,60)[0];n=struct.unpack_from('<H',d,p+6)[0];op=struct.unpack_from('<H',d,p+20)[0]
sections=[]
for i in range(n):
 q=p+24+op+40*i;sections.append((d[q:q+8].rstrip(b'\0'),*struct.unpack_from('<IIII',d,q+8)))
def read(a,z):
 for name,vs,va,rs,ro in sections:
  if 0x120000+va<=a and a+z<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+z]
 raise ValueError('unbacked exact image read')
registrar=W/'softedges-member-resolution-code-01.json'
r=json.loads(registrar.read_text());ix={int(i['pc'],16):i for q in r['ranges'] for i in q['instructions']}
def rip(pc):
 i=ix[pc];targets=[int(m['rip_target'],16) for m in i['memory'] if m.get('rip_target')]
 if i['mnemonic']!='lea' or len(targets)!=1:raise ValueError('required registration source changed')
 if read(pc,len(bytes.fromhex(i['bytes'])))!=bytes.fromhex(i['bytes']):raise ValueError('registration is not original')
 return targets[0]
name=read(rip(0x5eedaf),6)
vt= rip(0x5eedcc); callback=rip(0x5eedef)
if name!=b'm_els\0' or vt!=0xd4bd30 or callback!=0x60f280:raise ValueError('named member/callback identity')
slot=read(vt+0x40,8)
if struct.unpack('<Q',slot)[0]!=0x60f3d0:raise ValueError('wrong registered assignment')
leaf=read(0x60f3d0,0x21)
if leaf.hex()!='488b41704d8bd04c8bda4885c0740c458bc1498bd2498bcb48ffe0b815000000c3':
 raise ValueError('whole two-exit leaf CFG changed')
entries=[]
for name_s,vs,va,rs,ro in sections:
 if name_s==b'.pdata':
  for q in range(ro,ro+rs-11,12):
   a,b,u=struct.unpack_from('<III',d,q)
   if a+0x120000==callback:entries.append((a+0x120000,b+0x120000,u+0x120000))
if len(entries)!=1 or entries[0][:2]!=(callback,0x60f290):raise ValueError('callback extent identity')
body=read(callback,16)
if body.hex()!='4883ec28e857fdffff33c04883c428c3':raise ValueError('callback call/status sequence changed')
asset=(W/'softedges-resource-source-01/phyretext.fx.phyre').read_bytes()
if sha(asset)!='f67d4492c21fc687f8897c130f66e8cddf5d8d2f0d262589b8597791a767a4cf':raise ValueError('wrong retained asset')
h=struct.unpack_from('<21I',asset);b=asset[h[1]:h[1]+h[2]]
nt,nc,nm,pooln=struct.unpack_from('<4I',b,8);ms=32+4*nt+36*nc;pool=b[ms+24*nm:]
if ms+24*nm+pooln!=len(b):raise ValueError('namespace extent')
def text(a):return pool[a:pool.index(b'\0',a)].decode('ascii')
selected=[];cursor=0
for i in range(nc):
 c=struct.unpack_from('<9I',b,32+4*nt+36*i)
 fields=[struct.unpack_from('<6I',b,ms+24*j) for j in range(cursor,cursor+c[3])];cursor+=c[3]
 if i+1 in (13,17):selected.append(dict(class_id=i+1,name=text(c[2]),raw=list(c),members=[dict(name=text(m[0]),raw=list(m)) for m in fields]))
if cursor!=nm or selected[1]['name']!='PArray<PShaderParameterDefinition>' or selected[1]['members'][1]['name']!='m_els':raise ValueError('exact file member identity')
out.mkdir()
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x60f3d0,0x60f3f1),(0x60f280,0x60f290)];sys.argv=[sys.argv[0],str(out/'original-code.json')];C.main()
raw=json.loads((out/'original-code.json').read_text());raw.update(wrapper_complete=True,invocation_driver_sha256=sha(pathlib.Path(__file__).read_bytes()),
 limits='Entire two-exit leaf dispatcher plus exact normal callback; not complete loader/resource initialization or unknown cleanup effects.')
(out/'original-code.json').write_text(json.dumps(raw,indent=2)+'\n')
facts=dict(method='A STATIC_ONLY',status='PRODUCER_SOURCE_COMPLETE_REVIEW_PENDING',exe_sha256=sha(d),asset_sha256=sha(asset),
 question='What address/count ABI and result propagation does the original named m_els assignment actually use?',
 hypotheses=['A second metadata offset/base adjustment and inner failure propagation','Direct supplied-object callback ABI and explicit inner-status suppression'],
 choice='Exact original branch/register/write sequence distinguishes these hypotheses; no live state or new isolated samples are required.',
 registration_source_sha256=sha(registrar.read_bytes()),member_name=name.hex(),member_name_address=hex(rip(0x5eedaf)),
 vtable=hex(vt),slot_offset='0x40',slot_bytes=slot.hex(),assignment='0x60f3d0',callback=hex(callback),callback_pdata=[list(e) for e in entries],
 file_classes=selected,
 observations=[
  'Native registration5EEDAF names m_els, not m_data. The old working shorthand is corrected; packed class17 independently names m_els at file+4.',
  '60F3D0 reads metadata+70. Nonnull tail-dispatches with RCX=supplied object,RDX=supplied source,R8D=count; it performs no member+48/owner+F4 adjustment. Null returns21 without array writes.',
  'Registered callback60F280 calls original60EFE0 with that ABI, then XOR EAX,EAX and returns0 regardless of a normally returning setter result.',
  'Retained60EFE0 rejects negative signed counts with5 before array writes. Normal nonnegative continuation writes source at array+8 and count|80000000 at array+0; different owned old storage takes unproved5F03A0 cleanup.',
  'Therefore callback return0 is not proof of a write or accepted count. This is original native API behavior, separate from the project requirement that evidence tools propagate failed prerequisites.'
 ],
 limits='Original-source proof only. Mapped-class/member bindings, packed key22/27 resolver child-link terminal behavior, descriptor base adjustments, actual load success, native pointer identity/lifetime, natural reachability and cleanup effects remain OPEN. No static pointer observation is a captured live pointer.',
 next='Resolve actual file-member to mapped-child construction; do not substitute the outer60F590 setter, assume child-null or claim installed arrays from this dispatcher.',
 controls=raw['controls'],native_runs=0,live_runs=0,
 driver_sha256=sha(pathlib.Path(__file__).read_bytes()))
(out/'facts.json').write_text(json.dumps(facts,indent=2)+'\n')
print('CAPTURED original named m_els dispatcher/callback; normal inner-status suppression proved statically; loaded binding OPEN')
