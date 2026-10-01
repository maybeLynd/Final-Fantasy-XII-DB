import importlib.util,json,shutil,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('nativewritercheck',W/'check.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
controls=[]
assert not (W/'reducer-controls.json').exists(),'Write-once receipt'
for name in ['missing-second','nonzero-first','changed-second-state']:
 with tempfile.TemporaryDirectory(dir=W) as tmp:
  p=Path(tmp);shutil.copytree(W/'run-01',p/'run-01')
  for f in ['capture.py','capture-terminal.json']:shutil.copyfile(W/f,p/f)
  if name=='missing-second':(p/'run-01/second-terminal.json').unlink()
  elif name=='nonzero-first':
   f=p/'run-01/first-terminal.json';v=json.loads(f.read_bytes());v['returncode']=1;f.write_text(json.dumps(v))
  else:
   f=p/'run-01/after-second-board.json';v=json.loads(f.read_bytes());v['revision']+=1;f.write_text(json.dumps(v))
  try:module.check(p)
  except (AssertionError,FileNotFoundError) as error:controls.append({'case':name,'refused':True,'exception_type':type(error).__name__})
  else:raise AssertionError('Invalid receipt admitted '+name)
(W/'reducer-controls.json').write_text(json.dumps(controls,indent=2)+'\n')
print(json.dumps(controls))
