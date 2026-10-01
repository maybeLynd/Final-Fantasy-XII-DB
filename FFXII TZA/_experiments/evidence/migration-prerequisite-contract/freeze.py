import copy,hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'run-01';P=Path('Database/FFXII TZA/_experiments/evidence/migration-prerequisite-contract');assert not P.exists()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=json.loads((R/'raw.json').read_text());original=sha(R/'raw.json');d=W/'reducer-controls';d.mkdir(exist_ok=True);receipts=[]
for name in ['incomplete','missing-case','hide-custom-failure']:
 r=copy.deepcopy(raw)
 if name=='incomplete':r['finished']=False
 elif name=='missing-case':r['cases'].pop()
 else:
  c=next(c for c in r['cases'] if c['name']=='custom-tab-fail');c.update(returncode=1,stdout='COMPOSER_FAIL fictitious repair\n',actually_accepted=False,expectation_met=True)
 inp=d/(name+'.json');out=d/(name+'-result.json');inp.write_text(json.dumps(r));assert not out.exists()
 z=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(inp),'--out',str(out)],capture_output=True,text=True)
 receipts.append(dict(name=name,input_sha256=sha(inp),returncode=z.returncode,stdout=z.stdout,stderr=z.stderr,result_exists=out.exists()));assert z.returncode!=0 and not out.exists()
z=subprocess.run([sys.executable,'-B',str(W/'check.py')],capture_output=True,text=True);assert z.returncode==0 and sha(R/'raw.json')==original
(W/'reducer-controls.json').write_text(json.dumps(dict(baseline=dict(returncode=z.returncode,stdout=z.stdout),negative_controls=receipts,original_raw_unchanged=True),indent=2)+'\n')
P.mkdir(parents=True);(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ['PLAN.md','README.md','capture.py','check.py','freeze.py','standalone-format-control.py','standalone-format-control.json','result.json','reducer-controls.json']:shutil.copyfile(W/n,P/n)
shutil.copytree(R,P/'run-01')
members=[dict(path=f.relative_to(P).as_posix(),bytes=f.stat().st_size,sha256=sha(f)) for f in sorted(P.rglob('*')) if f.is_file()]
(P/'manifest.json').write_text(json.dumps(dict(package='migration-prerequisite-contract',members=members),indent=2)+'\n')
for f in P.rglob('*'):
 if f.is_file():
  normal=subprocess.check_output(['git','hash-object','--',f.as_posix()],text=True).strip();unfiltered=subprocess.check_output(['git','hash-object','--no-filters','--',f.as_posix()],text=True).strip();assert normal==unfiltered,f
print('FROZEN_PREREQ',len(members),'byte-preserving Git attributes verified')
