"""Actual fallback checker invocation: corrected extent/completion are prerequisites."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable control directory exists')
source=W/'prove-special-fallback-byte-bound.py';text=source.read_text()
line='W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]'
if text.count(line)!=1:raise ValueError('one input-root literal expected')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['capture-index-path.py','capture-special-selection-dispatch.py','special-selection-dispatch-raw-02.json',
 'capture-spattack-leaves-and-guard.py','spattack-leaves-and-guard-raw-01.json']
out.mkdir();shutil.copyfile(source,out/'original-checker.py');cases=[]
for case in ['positive','missing_wrapper_completion','wrong_dispatch_extent','missing_required_raw']:
 f=out/case;f.mkdir()
 for name in names:shutil.copyfile(W/name,f/name)
 if case in ['missing_wrapper_completion','wrong_dispatch_extent']:
  p=f/'special-selection-dispatch-raw-02.json';r=json.loads(p.read_text())
  if case=='missing_wrapper_completion':r.pop('wrapper_complete')
  else:r['jump_table']['entries']=10
  p.write_text(json.dumps(r))
 elif case=='missing_required_raw':(f/'special-selection-dispatch-raw-02.json').unlink()
 adapted=text.replace(line,'W=pathlib.Path('+repr(str(f.resolve()))+');ROOT=pathlib.Path('+repr(str(ROOT))+')')
 script=f/'checker-input-adapted.py';script.write_text(adapted)
 argv=[sys.executable,'-B',str(script),str(f/'result.json')]
 run=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=20)
 (f/'stdout.txt').write_text(run.stdout);(f/'stderr.txt').write_text(run.stderr)
 if case=='positive':
  valid=run.returncode==0 and (f/'result.json').exists()
  if valid:valid=all(json.loads((f/'result.json').read_text())['controls'].values())
 else:
  marker='FileNotFoundError' if case=='missing_required_raw' else 'dispatch wrapper prerequisite'
  valid=run.returncode!=0 and marker in run.stderr and not (f/'result.json').exists()
 cases.append(dict(case=case,argv=argv,terminal=True,exit_code=run.returncode,result_exists=(f/'result.json').exists(),
  control_passed=valid,adapted_checker_sha256=sha(script)))
 if not valid:raise ValueError('actual fallback prerequisite control failed: '+case)
if sha(source)!=sha(out/'original-checker.py'):raise ValueError('source changed during controls')
(out/'receipt.json').write_text(json.dumps(dict(driver_sha256=sha(pathlib.Path(__file__)),original_checker_sha256=sha(source),
 adaptation='W/ROOT input literals only; checker logic unchanged',cases=cases,
 scope='producer path controls, not original-code executions or independent acceptance'),indent=2)+'\n')
print('Fallback checker actual controls: positive0; missing completion, wrong extent, missing raw all nonzero/no-result')
