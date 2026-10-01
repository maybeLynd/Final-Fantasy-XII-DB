"""Actual category checker failures on disposable input-only adapted copies."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable control directory exists')
source=W/'prove-action-category-seven.py';text=source.read_text()
line='W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]'
if text.count(line)!=1:raise ValueError('one input-root literal expected')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['capture-index-path.py','capture-action-availability-gates.py','action-availability-gates-raw-01.json',
 'capture-spattack-leaves-and-guard.py','spattack-leaves-and-guard-raw-01.json']
out.mkdir();shutil.copyfile(source,out/'original-checker.py');cases=[]
for case in ['positive','failed_capture_role','missing_required_raw','changed_table_bytes']:
 f=out/case;f.mkdir()
 for name in names:shutil.copyfile(W/name,f/name)
 shutil.copytree(W/'special-action-frozen-ready',f/'special-action-frozen-ready')
 if case=='failed_capture_role':
  p=f/'action-availability-gates-raw-01.json';r=json.loads(p.read_text());r['controls'][0]['observed']='r';p.write_text(json.dumps(r))
 elif case=='missing_required_raw':(f/'action-availability-gates-raw-01.json').unlink()
 elif case=='changed_table_bytes':
  p=f/'special-action-frozen-ready/action-selectors-01/tables/action_data_ch.st2e';b=bytearray(p.read_bytes());b[-1]^=1;p.write_bytes(b)
 adapted=text.replace(line,'W=pathlib.Path('+repr(str(f.resolve()))+');ROOT=pathlib.Path('+repr(str(ROOT))+')')
 script=f/'checker-input-adapted.py';script.write_text(adapted)
 argv=[sys.executable,'-B',str(script),str(f/'result.json')]
 run=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=20)
 (f/'stdout.txt').write_text(run.stdout);(f/'stderr.txt').write_text(run.stderr)
 if case=='positive':
  valid=run.returncode==0 and (f/'result.json').exists()
  if valid:
   r=json.loads((f/'result.json').read_text());valid=len(r['rows'])==9 and all(r['controls'].values()) and r['raw5_domain'][0]['category_result']==5
 else:
  marker={'failed_capture_role':'capture role prerequisite','missing_required_raw':'FileNotFoundError','changed_table_bytes':'immutable table prerequisite'}[case]
  valid=run.returncode!=0 and marker in run.stderr and not (f/'result.json').exists()
 cases.append(dict(case=case,argv=argv,terminal=True,exit_code=run.returncode,result_exists=(f/'result.json').exists(),
  control_passed=valid,adapted_checker_sha256=sha(script)))
 if not valid:raise ValueError('actual category prerequisite control failed: '+case)
if sha(source)!=sha(out/'original-checker.py'):raise ValueError('source changed during controls')
(out/'receipt.json').write_text(json.dumps(dict(driver_sha256=sha(pathlib.Path(__file__)),original_checker_sha256=sha(source),
 adaptation='W/ROOT input literals only; no checker logic changes',cases=cases,
 scope='producer path controls, not original-code executions or independent acceptance'),indent=2)+'\n')
print('Category checker actual controls: positive0; failed role, missing raw, changed table all nonzero/no-result')
