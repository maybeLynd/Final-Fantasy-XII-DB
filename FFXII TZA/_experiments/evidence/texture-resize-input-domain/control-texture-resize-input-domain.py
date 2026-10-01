"""Three actual selected-count producer refusals; reuse positive, no game tests."""
import hashlib,importlib.util,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-resize-input-domain-controls-01'
if out.exists():raise ValueError('immutable controls exist')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
positive=W/'texture-resize-input-domain-result-01.json';r=json.loads(positive.read_text());checker=W/'prove-texture-resize-input-domain.py'
if not r.get('producer_complete') or r['checker_sha256']!=sha(checker):raise ValueError('missing valid positive')
names=[q['path'] for q in r['source_pins']];out.mkdir()
s=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
def floor(z):
 q=next(q for q in z['ranges'] if q['start']=='0x17e8e0');i=next(i for i in q['instructions'] if i['pc']=='0x17e9ec')
 if not i['bytes'].startswith('0f47'):raise ValueError('CMOVA preimage changed')
 i['bytes']='0f46'+i['bytes'][4:];i['mnemonic']='cmovbe'
 q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest();S.validate(z)
def metadata(z):z['pdata_entries'].pop()
cases=[('consistent-wrong-floor',names[0],floor,'selected original body identity changed'),('missing-normal-tail',names[2],None,'FileNotFoundError'),('missing-tail-metadata',names[2],metadata,'missing complete chained root metadata')];records=[]
for label,file,mut,error in cases:
 case=out/label;src=case/'source';src.mkdir(parents=True)
 for n in names:shutil.copyfile(W/n,src/n)
 p=src/file
 if mut is None:p.unlink()
 else:z=json.loads(p.read_text());mut(z);p.write_text(json.dumps(z,indent=2)+'\n')
 target=case/'result.json';run=subprocess.run([sys.executable,'-B',str(checker),str(target),str(src)],capture_output=True,timeout=60)
 (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr)
 q=dict(case=label,exit=run.returncode,result_absent=not target.exists(),expected_error_seen=error in run.stderr.decode(errors='replace'))
 (case/'status.json').write_text(json.dumps(q,indent=2)+'\n');records.append(q)
 if run.returncode==0 or not q['result_absent'] or not q['expected_error_seen']:raise ValueError('invalid refusal '+label)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_SELECTED_COUNT_REFUSALS_INDEPENDENT_PENDING',positive_reused=dict(path=positive.name,sha256=sha(positive)),checker_sha256=sha(checker),refusals=records,limits='Three synthetic producer CLI controls, no live/native runs or independent acceptance'),indent=2)+'\n');print('Three actual count-domain refusals; positive reused')
