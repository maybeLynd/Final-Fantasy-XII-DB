"""Bounded independent extent review requested by OPUS; A, no native/game run.
Reuse ASTRA's existing reachable-flow detector, not the peer classifier.
"""
import bisect,collections,csv,hashlib,json,struct,sys,datetime
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;ROOT=Path.cwd().resolve();DB=ROOT/'Database/FFXII TZA';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,detail=team.board_status(team.BOARD);assert ok,detail;b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='OPUS-REQ-ASTRA-UC1-BAND-65-256-ORIGINAL-BYTES');assert t['status']=='ACTIVE' and t['agent']=='ASTRA';assert not (W/'result.json').exists()
inputs={'band.tsv':DB/'_index/candidates/uc1-band-65-256/uc1-band-65-256-rows.tsv','admissions.tsv':DB/'99-Unresolved-Residual/Unlisted-Code/unlisted-body-admissions.tsv','functions.tsv':ROOT/'Database/Tools/work/graph/functions.tsv','errata.tsv':DB/'_index/FUNCTION-EXTENT-ERRATA.tsv','old-flow.py':W.parent/'uc1-band-ruling/review.py','peer-producer.py':DB/'_index/candidates/uc1-band-65-256/uc1_band_65_256.py','peer-README.md':DB/'_index/candidates/uc1-band-65-256/README.md'}
payloads={n:p.read_bytes() for n,p in inputs.items()}
def table(data):return list(csv.DictReader([l for l in data.decode('utf-8-sig').splitlines() if l and not l.startswith('#')],delimiter='\t'))
band=table(payloads['band.tsv']);adm=table(payloads['admissions.tsv']);selected=[r for r in band if r['outcome']=='clean'];assert len(band)==120 and len(selected)==100 and len({r['start_va'] for r in selected})==100
ad={r['start_va']:r for r in adm if r['verdict']=='body' and 65<=int(r['bytes'])<=256};assert len(ad)==120 and {r['start_va'] for r in band}==set(ad)
for row in band:assert row['bytes']==ad[row['start_va']]['bytes'] and row['prev_entry']==ad[row['start_va']]['prev_entry']
source=payloads['old-flow.py'].decode();prefix=source[:source.index('adm = table(ADM)')];ns={'__file__':str(inputs['old-flow.py'])};exec(compile(prefix,str(inputs['old-flow.py'])+'[unchanged flow prefix]','exec'),ns)
raw=ns['raw'];read=ns['bytes_at'];flow=ns['flow'];assert sha(raw)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
listed=table(payloads['functions.tsv']);sizes={int(r['entry'],16):int(r['body_bytes']) for r in listed if r['body_bytes'].isdigit() and not r['name'].startswith(('Unwind@','Catch_All@'))};assert sizes and len(listed)>=len(sizes)
applied=[]
for r in table(payloads['errata.tsv']):
 if r['verdict']=='merge' and r['corrected_end'].strip():
  a,end=int(r['entry'],16),int(r['corrected_end'],16)
  if a in sizes and a<end<a+sizes[a]:applied.append(dict(entry=hex(a),old_size=sizes[a],corrected_size=end-a,row=r));sizes[a]=end-a
starts=sorted(sizes)
controls={'known-truncated-store48':dict(start='0x7ee7c0',bytes=48,raw_hex=read(0x7EE7C0,48).hex(),flow=flow(0x7EE7C0,48)),'known-complete-store57':dict(start='0x7ee7c0',bytes=57,raw_hex=read(0x7EE7C0,57).hex(),flow=flow(0x7EE7C0,57))}
assert controls['known-truncated-store48']['flow']['problems'] and not controls['known-complete-store57']['flow']['problems']
rows=[]
for candidate in selected:
 a,n=int(candidate['start_va'],16),int(candidate['bytes']);data=read(a,n);f=flow(a,n);assert f['instructions']
 reach=[i for i in f['instructions'] if i[4]];assert reach
 maxend=max(int(i[0],16)+len(bytes.fromhex(i[1])) for i in reach);assert a<maxend<=a+n
 collisions=[dict(entry=hex(v),size=sizes[v],kind='listed entry inside proposed byte span',reachable_containing_instructions=[i[:4] for i in reach if int(i[0],16)<=v<int(i[0],16)+len(bytes.fromhex(i[1]))]) for v in starts if a<=v<a+n]
 spanoverlap=[dict(entry=hex(v),size=z,kind='catalog numeric span overlap, not proof of contiguous native body') for v,z in sizes.items() if v<a+n and a<v+z]
 external=[]
 for item in f['exits']:
  site,kind=item;inst=next(i for i in f['instructions'] if i[0]==site)
  if kind=='external/direct':
   target=int(inst[3],16);index=bisect.bisect_right(starts,target)-1;owner=starts[index] if index>=0 and target<starts[index]+sizes[starts[index]] else None
   external.append(dict(site=site,target=hex(target),listed_entry_exact=target in sizes,nearest_catalog_containing_span=None if owner is None else dict(entry=hex(owner),size=sizes[owner]),limits='External edge is retained, not traversed or promoted to a native tail call/complete function'))
  elif kind=='indirect':external.append(dict(site=site,target=None,limits='Computed target unresolved, no complete function identity'))
 extension=None
 if f['problems']:
  ext=read(a,n+64);ff=flow(a,n+64);extension=dict(bytes=n+64,raw_hex=ext.hex(),flow=ff,listed_entries=[hex(v) for v in starts if a<=v<a+n+64],limits='One bounded diagnostic extension only, not a proposed repair/automatically accepted extent')
 rows.append(dict(candidate=candidate,raw_hex=data.hex(),sha256=sha(data),flow=f,reachable_instruction_count=len(reach),max_reachable_end=hex(maxend),unreachable_trailing_bytes=data[maxend-a:].hex(),listed_entries=collisions,catalog_numeric_span_overlaps=spanoverlap,external_edges=external,bounded_extension=extension,verdict='HOLD_REACHABLE_BOUNDARY' if f['problems'] else 'HOLD_LISTED_ENTRY' if collisions else 'PASS_BOUNDED_EXTENT',qualifier='This selected span has no reachable missing boundary/listed entry; external and computed exits remain unresolved, not wholefunction/admission proof'))
R=W/'retained';R.mkdir(exist_ok=False)
(R/'initial-failed-review.py').write_bytes((W/'initial-failed-review.py').read_bytes());(R/'initial-failure.json').write_bytes((W/'initial-failure.json').read_bytes())
for name in ('band.tsv','old-flow.py','peer-producer.py','peer-README.md','errata.tsv'):(R/name).write_bytes(payloads[name])
projection='entry\tbytes\n'+''.join(f'{v:08X}\t{sizes[v]}\n' for v in starts);(R/'listed-span-projection.tsv').write_text(projection)
membership='start_va\tbytes\tprev_entry\n'+''.join(f"{r['start_va']}\t{r['bytes']}\t{r['prev_entry']}\n" for r in sorted(ad.values(),key=lambda x:x['start_va']));(R/'admission-membership.tsv').write_text(membership)
dll=Path(capstone._cs._name);tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll=dict(path=str(dll),sha256=sha(dll.read_bytes())))
result=dict(method='A shipping raw bytes/reachable-instruction review, no original-code/native/emulator/live execution',request='OPUS-REQ-ASTRA-UC1-BAND-65-256-ORIGINAL-BYTES',reference=dict(exe_sha256=sha(raw),image_base='0x120000',image_path=str(ns['EXE']),flow_prefix_sha256=sha(prefix.encode()),full_flow_source_sha256=sha(payloads['old-flow.py'])),driver_sha256=sha(Path(__file__).read_bytes()),inputs=[dict(name=n,path=p.relative_to(ROOT).as_posix(),bytes=len(payloads[n]),sha256=sha(payloads[n])) for n,p in inputs.items()],tools=tools,population=dict(band_rows=len(band),selected_clean_rows=len(selected),listed_spans=len(sizes)),controls=controls,applied_existing_errata=applied,observations=rows,summary=dict(verdict_counts=dict(collections.Counter(r['verdict'] for r in rows)),rows_with_external_edges=[r['candidate']['start_va'] for r in rows if r['external_edges']],rows_with_tail_bytes=[r['candidate']['start_va'] for r in rows if r['unreachable_trailing_bytes']],rows_with_numeric_catalog_overlap=[r['candidate']['start_va'] for r in rows if r['catalog_numeric_span_overlaps']]),limits='Independent only of OPUS byte-table instrument, same decoder family/tool is disclosed. Reachable flow starts at proposed entry and follows both conditional direct edges inside span; calls not traversed. External/indirect jumps bounded exits, not complete logical function/normalreachability proof. No computed-pointer recovery, byte-table rerun, semantic/admission/population ruling or PE root extent substitution. Numeric catalog spans can contain gaps and are not automatically native overlap proof.',cleanup='Read-only canonical sources and shipping image; own work/evidence only. PC OFF, no process/game/input/save/config/reference/peerwrites. Owner ruling/reviews remain separate; DB_GOAL NOT_MET')
for name,p in inputs.items():assert p.read_bytes()==payloads[name],('input changed',name)
assert sha(ns['EXE'].read_bytes())==sha(raw) and sha(dll.read_bytes())==tools['capstone_dll']['sha256']
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['summary'],indent=2),flush=True)
