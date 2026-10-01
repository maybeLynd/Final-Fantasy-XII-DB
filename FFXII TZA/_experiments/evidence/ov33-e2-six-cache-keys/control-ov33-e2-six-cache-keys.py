"""Actual key-domain reducer refuses changed code or incomplete input."""
import hashlib,importlib.util,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'ov33-e2-six-key-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
positive=W/'ov33-e2-six-cache-keys-result-01.json';r=json.loads(positive.read_text());checker=W/'prove-ov33-e2-six-cache-keys.py'
if r.get('producer_complete') is not True or r['checker_sha256']!=sha(checker) or not r['detection_positive']['matching_archive_names']:raise ValueError('required positive/detection control absent')
s=importlib.util.spec_from_file_location('key_control_annotation',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
def changed_multiplier(src):
 p=src/'filecache-hash-loop-source-01.json';z=json.loads(p.read_text());q=z['ranges'][0];i=next(i for i in q['instructions'] if i['pc']=='0x674a10')
 if i['bytes']!='6bc021':raise ValueError('original multiplier preimage changed')
 i['bytes']='6bc020';i['args']='eax, eax, 0x20';q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest();S.validate(z);p.write_text(json.dumps(z,indent=2)+'\n')
def zero_input(src):
 p=src/'ov33-e2-key-inputs-01/inputs.json';z=json.loads(p.read_text());z['archive']['file_count']=0;p.write_text(json.dumps(z,indent=2)+'\n')
def missing_prefix(src):(src/'ov33-e2-key-inputs-01/archive-name-index-prefix.bin.zlib').unlink()
cases=[('consistent-wrong-multiplier',changed_multiplier,'original complete hash-loop identity changed'),('zero-input-population',zero_input,'required index input missing/zero/incomplete'),('missing-index-prefix',missing_prefix,'FileNotFoundError')]
out.mkdir();records=[]
for label,mut,error in cases:
 case=out/label;src=case/'source';src.mkdir(parents=True)
 shutil.copyfile(W/'filecache-hash-loop-source-01.json',src/'filecache-hash-loop-source-01.json');shutil.copytree(W/'ov33-e2-key-inputs-01',src/'ov33-e2-key-inputs-01');mut(src)
 target=case/'result.json';run=subprocess.run([sys.executable,'-B',str(checker),str(target),str(src)],capture_output=True,timeout=60)
 (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr)
 record=dict(case=label,exit=run.returncode,result_absent=not target.exists(),expected_error_seen=error in run.stderr.decode(errors='replace'))
 (case/'status.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
 if run.returncode==0 or not record['result_absent'] or not record['expected_error_seen']:raise ValueError('invalid key-domain refusal '+label)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_SIX_KEY_REFUSALS_INDEPENDENT_PENDING',checker_sha256=sha(checker),positive_reused=dict(path=positive.name,sha256=sha(positive)),refusals=records,limits='Three actual producer CLI controls; complete positive reused. No native/game run or external-test credit.'),indent=2)+'\n');print('Three actual key-domain refusals; positive and nonempty collision detector reused')
