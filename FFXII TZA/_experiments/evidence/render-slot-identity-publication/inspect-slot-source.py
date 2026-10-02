"""Feasibility/primary-source inspection, not semantic acceptance or FF12 execution."""
import hashlib, importlib.util, json, struct, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if (P/'inspect.py').exists():raise RuntimeError('local inspect.py would shadow required standard library')
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for f,pin in [('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
s=json.loads((P/'capture-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('invocation_driver_sha256')!=sha(P/'capture.py') or x['driver_sha256']!=sha(P/'capture-index-path.py'):raise RuntimeError('actual capture incomplete')
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');roles=V.validate(x)
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=pin or x['exe_sha256']!=pin:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,offset in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
 raise RuntimeError('unbacked range')
required=[('0x41f730','0x41fbe8'),('0x420480','0x420851'),('0x4269a0','0x426c85'),('0x4279b0','0x427af9')]
if [(r['start'],r['end_exclusive']) for r in x['ranges']]!=required:raise RuntimeError('source population changed')
rows=[]
for r in x['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 ix={int(i['pc'],16):i for i in r['instructions']};g=G.graph(ix,a,b)
 if g['visited']!=set(ix):raise RuntimeError('unaccounted original CFG')
 selected=[i for i in ix.values() if any(m['role']!='addr' and m['base'] in ['rbx','rdi','rsi','rcx','r8'] and m['displacement'] in [0,0x284,0x48808,0x4880c] for m in i['memory'])]
 rows.append({'entry':hex(a),'bytes':b-a,'instructions':len(ix),'calls':g['calls'],'selected_accesses':selected})
out=P/(sys.argv[1] if len(sys.argv)>1 else 'inspection-02.json')
if out.exists():raise RuntimeError('immutable output exists')
out.write_bytes((json.dumps({'inspection_complete':True,'driver_sha256':sha(Path(__file__)),'source_sha256':sha(P/'source-01.json'),'annotation_prerequisite':roles,'ranges':rows,'limits':'Feasibility/original-byte/CFG inspection only. No semantic closure, native execution, all-writer/opaque-effect or natural scheduling claim.'},indent=2)+'\n').encode())
print('INSPECTED four original bodies with complete local CFG; semantic proof and controls pending')
