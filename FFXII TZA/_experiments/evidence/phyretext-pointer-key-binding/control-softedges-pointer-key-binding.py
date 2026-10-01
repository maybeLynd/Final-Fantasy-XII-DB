"""Smallest concrete regression for lost guard source and wrong caller base."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;out=W/'softedges-pointer-key-controls-01'
if out.exists():raise ValueError('immutable control directory exists')
r=json.loads((W/'softedges-pointer-key-binding-result-03.json').read_text());driver=W/'reduce-softedges-pointer-key-binding.py'
if r.get('producer_complete') is not True or r['checker_sha256']!=hashlib.sha256(driver.read_bytes()).hexdigest():raise ValueError('unchecked baseline')
out.mkdir();checks=[]
for name in ['missing-guard-source','wrong-count-base']:
 c=out/name;s=c/'source';s.mkdir(parents=True)
 for item in r['source_pins']:
  p=s/item['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/item['path'],p)
 if name=='missing-guard-source':(s/'softedges-array-terminal-guard-source-01/original-code.json').unlink()
 else:
  p=s/'softedges-header-membership-code-01.json';j=json.loads(p.read_text());x=next(x for q in j['ranges'] for x in q['instructions'] if x['pc']=='0x59cd07')
  x['args']='r9d, dword ptr [r14 + 0x14]';p.write_text(json.dumps(j)+'\n')
  # Disclosed normalization mutation recreates the exact mistaken source-base
  # hypothesis; bytes remain original. The concrete checker must reject it.
 args=[sys.executable,str(driver),str(c/'result.json'),str(s)]
 a=subprocess.run(args,cwd=W.parents[4],capture_output=True,timeout=15)
 (c/'stdout.txt').write_bytes(a.stdout);(c/'stderr.txt').write_bytes(a.stderr)
 rec=dict(case=name,argv=args,exit=a.returncode,result_exists=(c/'result.json').exists(),status='PASS_REFUSED' if a.returncode!=0 and not (c/'result.json').exists() else 'FAIL')
 (c/'invocation.json').write_text(json.dumps(rec,indent=2)+'\n');checks.append(rec)
 if rec['status']!='PASS_REFUSED':raise ValueError('invalid prerequisite reached a semantic result')
(out/'result.json').write_text(json.dumps(dict(status='PASS_PRODUCER_CONTROLS',reducer_sha256=r['checker_sha256'],checks=checks,
 limits='Actual subprocess refusals of disposable source defects, not original-code or live tests. Baseline03 reused; no changed game binary or canonical input.'),indent=2)+'\n')
print('Both affected invocation controls refuse; own children terminal')
