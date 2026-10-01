"""A one requested source extent, reusing the unchanged existing flow detector."""
import csv,hashlib,json,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';ROOT=Path.cwd().resolve();sha=lambda b:hashlib.sha256(b).hexdigest()
# Resume the retained observation through the reviewed normalizer, without recapture.
if (W/'raw.json').exists():
 import runpy
 runpy.run_path(str(W/'check.py'),run_name='__main__')
 raise SystemExit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='FABLE-REQ-ASTRA-UC1-257-EXTENT');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not (W/'result.json').exists();R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
def table(data):return list(csv.DictReader([l for l in data.decode('utf-8-sig').splitlines() if l and not l.startswith('#')],delimiter='\t'))
DB=ROOT/'Database/FFXII TZA';inputs={'band.tsv':DB/'_index/candidates/uc1-band-257-up/uc1-band-257-up-rows.tsv','admissions.tsv':DB/'99-Unresolved-Residual/Unlisted-Code/unlisted-body-admissions.tsv','functions.tsv':ROOT/'Database/Tools/work/graph/functions.tsv','functions-parent.json':ROOT/'Database/Tools/work/graph/functions.parent.json','errata.tsv':DB/'_index/FUNCTION-EXTENT-ERRATA.tsv','applied1.tsv':DB/'99-Unresolved-Residual/Unlisted-Code/uc1-applied-population-1-64.tsv','applied65.tsv':DB/'99-Unresolved-Residual/Unlisted-Code/uc1-applied-population-65-256.tsv','old-flow.py':W.parent/'uc1-band-ruling/review.py','ruling.md':DB/'_index/candidates/uc1-band-257-up-fable-ruling/README.md'}
payload={n:p.read_bytes() for n,p in inputs.items()};rows=table(payload['band.tsv']);candidate=next(x for x in rows if x['start_va']=='00712180');assert candidate['bytes']=='353' and candidate['outcome']=='clean'
adm=next(x for x in table(payload['admissions.tsv']) if x['start_va']=='00712180');assert adm['verdict']=='body' and adm['bytes']==candidate['bytes'] and adm['prev_entry']==candidate['prev_entry']
src=payload['old-flow.py'].decode();prefix=src[:src.index('adm = table(ADM)')];ns={'__file__':str(inputs['old-flow.py'])};exec(compile(prefix,'unchanged retained ASTRA flow prefix','exec'),ns)
assert sha(ns['raw'])=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
parent=json.loads(payload['functions-parent.json']);listed=table(payload['functions.tsv']);assert parent['executable_sha256']==sha(ns['raw']) and len(listed)==parent['function_count']
sizes={int(x['entry'],16):int(x['body_bytes']) for x in listed if x['body_bytes'].isdigit() and not x['name'].startswith(('Unwind@','Catch_All@'))};assert sizes
applied=[]
for x in table(payload['errata.tsv']):
 if x['verdict']=='merge' and x['corrected_end'].strip():
  a,end=int(x['entry'],16),int(x['corrected_end'],16)
  if a in sizes and a<end<a+sizes[a]:applied.append(dict(source='errata',row=x));sizes[a]=end-a
for name in ['applied1.tsv','applied65.tsv']:
 for x in table(payload[name]):
  if x['kind']=='held':continue
  a,e=int(x['start'],16),int(x['end'],16);assert a<e
  if x['kind']=='remove-listed':assert a in sizes;sizes.pop(a)
  elif x['kind']=='extend-listed':assert a in sizes;sizes[a]=e-a
  elif x['kind'] in ['admit-frontier','split-part']:
   assert a not in sizes or sizes[a]==e-a;sizes[a]=e-a
  else:raise AssertionError(('Unknown canonical applied row kind',x))
  applied.append(dict(source=name,row=x))
refrow=next(x for x in table(payload['applied1.tsv']) if x['start']=='006DAA30');assert refrow['kind']=='admit-frontier' and refrow['end']=='006DAA35'
refbytes=ns['bytes_at'](0x6DAA30,5);refins=list(ns['md'].disasm(refbytes,0x6DAA30));assert len(refins)==1 and refins[0].mnemonic=='jmp' and refins[0].operands[0].imm==0x712180
a,n=0x712180,353;data=ns['bytes_at'](a,n);f=ns['flow'](a,n);short=ns['flow'](a,n-1)
controls={}
for name,length in [('known-truncated-store48',48),('known-complete-store57',57)]:
 b=ns['bytes_at'](0x7EE7C0,length);controls[name]=dict(entry='0x7ee7c0',bytes=length,raw_hex=b.hex(),flow=ns['flow'](0x7EE7C0,length))
obs=dict(candidate=candidate,admission=adm,entry=hex(a),bytes=n,end=hex(a+n),raw_hex=data.hex(),sha256=sha(data),flow=f,short352=dict(raw_hex=data[:-1].hex(),flow=short),listed_entries=[hex(v) for v in sorted(sizes) if a<=v<a+n],numeric_span_overlaps=[dict(entry=hex(v),bytes=z) for v,z in sorted(sizes.items()) if v<a+n and a<v+z],reference_thunk=dict(row=refrow,entry='0x6daa30',bytes=5,raw_hex=refbytes.hex(),op='jmp',target='0x712180',scope='Already-admitted lower-band entry/one original direct jump corroborated; no global reference census or native normal reachability proof'))
for name in ['band.tsv','errata.tsv','applied1.tsv','applied65.tsv','old-flow.py','ruling.md','functions-parent.json']:(R/name).write_bytes(payload[name])
(R/'listed-span-projection.tsv').write_text('entry\tbytes\n'+''.join(f'{v:08X}\t{sizes[v]}\n' for v in sorted(sizes)))
(R/'admission-row.json').write_text(json.dumps(adm,indent=2)+'\n')
tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,providers=[dict(path=str(Path(p).resolve()),bytes=Path(p).stat().st_size,sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name]])
raw=dict(method='A one requested original-byte extent with existing unchanged flow/control; no original/native/emulator/live code execution',driver_sha256=sha(Path(__file__).read_bytes()),reference=dict(exe_sha256=sha(ns['raw']),flow_prefix_sha256=sha(prefix.encode()),full_flow_sha256=sha(payload['old-flow.py'])),inputs=[dict(name=n,path=p.relative_to(ROOT).as_posix(),bytes=len(payload[n]),sha256=sha(payload[n])) for n,p in inputs.items()],tools=tools,projection=dict(filtered_numeric_spans=len(sizes),applied_current_rows=applied,projection_sha256=sha((R/'listed-span-projection.tsv').read_bytes()),limits='Current catalog numeric spans plus documented errata/applied bands. Not every numeric catalog span is native contiguous body proof.'),observation=obs,controls=controls)
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
assert controls['known-truncated-store48']['flow']['problems'] and not controls['known-complete-store57']['flow']['problems']
assert f['full_linear'] and not f['problems'] and f['instructions'] and all(x[4] for x in f['instructions']) and f['exits']==[['0x7122e0','ret']]
assert short['problems'] and not obs['listed_entries'] and not obs['numeric_span_overlaps']
for input_name,input_path in inputs.items():assert input_path.read_bytes()==payload[input_name],('Input changed',input_name)
for x in tools['providers']:assert sha(Path(x['path']).read_bytes())==x['sha256']
from normalize import normalize
result=normalize(raw)
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS_UC1_257_SINGLE_BOUNDARY retained original353B/82reachable/controls; bounded extent only')
