"""Feasibility: one prepared forwarder caller, no whole-caller census."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4];out=W/'texture-resize-forwarded-input-caller-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,p+6)[0];opt=struct.unpack_from('<H',d,p+20)[0]
secs=[struct.unpack_from('<IIII',d,p+24+opt+40*k+8) for k in range(ns)]
def read(a,n):
 for vs,va,rs,ro in secs:
  if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
 raise ValueError('whole reference fragment not backed')
rva,size=struct.unpack_from('<II',d,p+24+112+3*8)
if size%12:raise ValueError('invalid original exception directory')
pd=[tuple(v+0x120000 for v in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
prep=W/'texture-resize-forwarded-input-preparation-07.json';v=json.loads(prep.read_text())
if v['status']!='PREPARATION_ONLY_CONTROLS_VALID' or v['exe_sha256']!=SHA:raise ValueError('invalid preparation')
sites=[q for q in v['references'] if q['target']=='0x183780' and q['kind']=='raw_rel32']
if len(sites)!=1:raise ValueError('selected caller set changed')
entries={};metadata=[]
for q in sites:
 pc=int(q['pc'],16);hits=[e for e in pd if e[0]<=pc<e[1]]
 if len(hits)!=1:raise ValueError('ambiguous/no function fragment for candidate')
 e=hits[0];entries[e]=True;h=read(e[2],4);at=(4+2*h[2]+3)&~3;flags=h[0]>>3
 chain=[v+0x120000 for v in struct.unpack('<III',read(e[2]+at,12))] if flags&4 else None
 metadata.append(dict(site=q['pc'],fragment=list(e),header=h.hex(),flags=flags,chain=chain,expected_call_bytes=q['bytes'],expected_target=q['target']))
s=importlib.util.spec_from_file_location('actual_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[e[:2] for e in sorted(entries)];sys.argv=[sys.argv[0],str(out)];C.main()
z=json.loads(out.read_text());s=importlib.util.spec_from_file_location('actual_annotation',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
agreement=S.validate(z);ix={i['pc']:i for q in z['ranges'] for i in q['instructions']}
for q in metadata:
 i=ix.get(q['site'])
 if i is None or (i['bytes'],i['mnemonic'],i['args'])!=(q['expected_call_bytes'],'call',q['expected_target']):raise ValueError('raw candidate is not a decoded original CALL')
z.update(wrapper_complete=True,callsite_metadata=metadata,annotation_prerequisite=agreement,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),preparation_pin=dict(path=prep.name,sha256=hashlib.sha256(prep.read_bytes()).hexdigest()),limits='One validated upstream directCALL site in containing pdata fragments only; not complete roots/branches/all callers or ordinary positive-count proof. Initial/predecessor/callee/indirect state unresolved; no process/game/native run.')
out.write_text(json.dumps(z,indent=2)+'\n')
print('Verified selected directCALL sites; fragment-only feasibility, incomingR9D semantic closure pending')
for q in z['ranges']:
 ins=q['instructions']
 for k,i in enumerate(ins):
  if i['pc'] in {m['site'] for m in metadata}:print(i['pc'],'FRAGMENT',q['start'],q['end_exclusive'],[(x['pc'],x['mnemonic'],x['args']) for x in ins[max(0,k-9):k+2]])
