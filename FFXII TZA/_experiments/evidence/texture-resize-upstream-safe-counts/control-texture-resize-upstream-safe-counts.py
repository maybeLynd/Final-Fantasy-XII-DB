"""Focused actual CLI controls for selected upstream counts; positive reused."""
import hashlib,importlib.util,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-resize-upstream-safe-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
positive=W/'texture-resize-upstream-safe-counts-result-01.json';r=json.loads(positive.read_text());checker=W/'prove-texture-resize-upstream-safe-counts.py'
if r.get('producer_complete') is not True or r['checker_sha256']!=sha(checker):raise ValueError('required positive failed/incomplete')
names=[q['path'] for q in r['source_pins']]
for q in r['required_result_pins']:names += [q['path']]+[p['path'] for p in q['source_pins']]
names += [q['path'] for q in r['required_invocation_receipts']];names=list(dict.fromkeys(names))
s=importlib.util.spec_from_file_location('control_annotation',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
def changed_constant(z):
 q=z['ranges'][0];i=next(i for i in q['instructions'] if i['pc']=='0x1babae')
 if i['args']!='r9d, [rcx + 0x20]' or not i['bytes'].endswith('20'):raise ValueError('constant32 preimage changed')
 i['bytes']=i['bytes'][:-2]+'21';i['args']='r9d, [rcx + 0x21]';i['memory'][0]['displacement']=0x21
 q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
 S.validate(z) # Mutation is a valid redecodable LEA, not malformed annotations.
def missing_edge(z):
 z['ranges']=[q for q in z['ranges'] if q['start']!='0x180fd0'];S.validate(z)
def failed_lower(z):z['producer_complete']=False
def failed_exit(z):z['exit']=74
cases=[('consistent-changed32','texture-resize-forwarded-input-caller-source-01.json',changed_constant,'selected upstream shipping identity changed'),('missing-palette-edge','texture-resize-palette-root-edges-source-01.json',missing_edge,'missing/extra selected upstream range'),('failed-lower-result','texture-resize-input-domain-result-01.json',failed_lower,'required lower-floor result failed or incomplete'),('failed-upstream-exit','texture-resize-input-domain-positive-01.status.json',failed_exit,'required lower-floor invocation failed or incomplete')]
out.mkdir();records=[]
for label,file,mut,error in cases:
 case=out/label;src=case/'source';src.mkdir(parents=True)
 for name in names:shutil.copyfile(W/name,src/name)
 p=src/file;z=json.loads(p.read_text());mut(z);p.write_text(json.dumps(z,indent=2)+'\n')
 target=case/'result.json';run=subprocess.run([sys.executable,'-B',str(checker),str(target),str(src)],capture_output=True,timeout=60)
 (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr)
 record=dict(case=label,exit=run.returncode,result_absent=not target.exists(),expected_error_seen=error in run.stderr.decode(errors='replace'))
 (case/'status.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
 if run.returncode==0 or not record['result_absent'] or not record['expected_error_seen']:raise ValueError('invalid concrete refusal '+label)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_UPSTREAM_COUNT_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(checker),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=records,limits='Four concrete producer CLI controls; no new sample, native/game execution or independent acceptance'),indent=2)+'\n')
print('Four actual upstream count refusals, qualified positive reused')
