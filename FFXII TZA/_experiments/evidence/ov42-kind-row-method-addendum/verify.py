"""Additive physical-coverage/method correction; no game-behavior experiment."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
x=json.loads((P/'old-source.json').read_text());y=json.loads((P/'current-source.json').read_text());lookup=json.loads((P/'lookup-01.json').read_text())
a=next(r for r in x['ranges'] if(r['start'],r['end_exclusive'])==('0x306c5b','0x306cec'));b=y['ranges'][0]
blob=lambda r:bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))
if (b['start'],b['end_exclusive'])!=('0x306c5b','0x306cec') or len(blob(a))!=145 or blob(a)!=blob(b) or a['sha256']!=b['sha256']:raise ValueError('nonempty exact original suffix equality required')
s=importlib.util.spec_from_file_location('roles',P/'validate-title-source-annotations.py');V=importlib.util.module_from_spec(s);s.loader.exec_module(V);annotations=[V.validate(z) for z in [x,y]]
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN or x['exe_sha256']!=PIN or y['exe_sha256']!=PIN:raise ValueError('wrong reference identity')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];found=False
for k in range(struct.unpack_from('<H',raw,pe+6)[0]):
 vs,rva,sz,off=struct.unpack_from('<IIII',raw,pe+32+opt+40*k)
 if 0x120000+rva<=0x306c5b and 0x306cec<=0x120000+rva+sz:
  start=off+0x306c5b-0x120000-rva;found=raw[start:start+145]==blob(a)
if not found or lookup.get('complete') is not True or lookup['driver_sha256']!=sha(P/'locate-retained-span.py') or lookup['requested']!=['0x306c5b','0x306cec'] or not any(m['path'].replace('\\','/').endswith('/autoattack-commit-exception/retained/current-row-source-01.json') and m['file_sha256']==sha(P/'old-source.json') for m in lookup['matches']):raise ValueError('actual retained-depth positive prerequisite absent')
with(P/'result-01.json').open('x') as f:json.dump(dict(producer_complete=True,method='A additive method/coverage correction, not a behavior experiment',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=n,sha256=sha(P/n)) for n in ['old-source.json','current-source.json']],annotation_prerequisites=annotations,facts=dict(suffix_bytes=145,suffix_sha256=a['sha256'],redundant_capture=True,new_experiment_coverage=0,new_work='Conditional full32 classifier versus low16 queue invariant analysis remains valid.',cause='Preparation searched only shallow source files, missing earlier retained subfolders.',procedure='Before new instruction capture, run bounded original-byte retained lookup over named W and canonical source-map corpus, including retained subfolders. Reuse a matching source with its original lineage/receipts; a physical match is not semantic acceptance.'),limits='Published d8328725 raw/result/manifest remain immutable. Correct only method/novelty wording; no new native/live sample or global absence/reachability conclusion.',cleanup='Offline only, reference/save/config/process untouched.'),f,indent=2)
print('VERIFIED additive correction: retained145B equals recapture; zero new experimental coverage')
