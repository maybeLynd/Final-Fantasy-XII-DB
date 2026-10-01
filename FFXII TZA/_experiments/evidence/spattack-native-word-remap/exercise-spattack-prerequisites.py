"""Actual checker invocations on isolated input-only adapted siblings.
Controls are producer tests, not original FF12 executions or independent acceptance.
"""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('fresh control directory required')
source=W/'prove-spattack-word-roundtrip.py';text=source.read_text()
line='W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]'
if text.count(line)!=1:raise ValueError('one input-root adaptation expected')
inputs=['capture-index-path.py','effective-and-script-id-raw-01.json','capture-effective-and-script-id.py',
 'spattack-output-writers-raw-02.json','capture-spattack-output-writers.py',
 'spattack-queue-reader-raw-01.json','capture-spattack-queue-reader.py',
 'spattack-info-raw-01.json','capture-spattack-info.py',
 'spattack-leaves-and-guard-raw-01.json','capture-spattack-leaves-and-guard.py']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out.mkdir();shutil.copyfile(source,out/'original-checker.py');results=[]
for case in ['positive','missing_wrapper_completion','failed_upstream_role','missing_required_input']:
 f=out/case;f.mkdir()
 for name in inputs:shutil.copyfile(W/name,f/name)
 if case=='missing_wrapper_completion':
  p=f/'spattack-output-writers-raw-02.json';r=json.loads(p.read_text());r.pop('wrapper_complete');p.write_text(json.dumps(r,indent=2)+'\n')
 elif case=='failed_upstream_role':
  p=f/'effective-and-script-id-raw-01.json';r=json.loads(p.read_text());r['controls'][0]['observed']='r';p.write_text(json.dumps(r,indent=2)+'\n')
 elif case=='missing_required_input':(f/'spattack-queue-reader-raw-01.json').unlink()
 # Literal replacement avoids the earlier regex backslash-interpretation failure.
 adapted=text.replace(line,'W=pathlib.Path('+repr(str(f.resolve()))+');ROOT=pathlib.Path('+repr(str(ROOT))+')')
 script=f/'checker-input-adapted.py';script.write_text(adapted)
 argv=[sys.executable,'-B',str(script),str(f/'result.json')]
 run=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=20)
 (f/'stdout.txt').write_text(run.stdout);(f/'stderr.txt').write_text(run.stderr)
 if case=='positive':
  valid=run.returncode==0 and (f/'result.json').exists()
  if valid:
   r=json.loads((f/'result.json').read_text());valid=r['roundtrip_mismatch_words']==[207] and len(r['candidate_results'])==24 and all(r['controls'].values())
 else:
  marker={'missing_wrapper_completion':'wrapper prerequisite incomplete',
          'failed_upstream_role':'upstream controls failed','missing_required_input':'FileNotFoundError'}[case]
  valid=run.returncode!=0 and marker in run.stderr and not (f/'result.json').exists()
 results.append(dict(case=case,argv=argv,terminal=True,exit_code=run.returncode,
   control_passed=valid,adapted_checker_sha256=sha(script),result_exists=(f/'result.json').exists()))
 if not valid:raise ValueError('actual prerequisite control failed: '+case)
if sha(source)!=sha(out/'original-checker.py'):raise ValueError('original checker changed')
(out/'receipt.json').write_text(json.dumps(dict(driver_sha256=sha(pathlib.Path(__file__)),
 original_checker_sha256=sha(source),adaptation='only W/ROOT input literals; checker logic unchanged',
 results=results,scope='actual producer-checker prerequisites; not new FF12 data or independent review'),indent=2)+'\n')
print('Actual invocation controls: positive0; three prerequisite failures nonzero/no-result')
