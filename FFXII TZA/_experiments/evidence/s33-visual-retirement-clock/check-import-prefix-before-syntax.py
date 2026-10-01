"""Actual retained import stage with labelled host fixtures; no native/game simulation."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;F=P/'import-controls-01'
R=Path('Database/FFXII TZA/_index/candidates/s33-opus-replay-op1-real')
U=R.parent/'s21-opus-replay-applier-stub-free'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'s33-producer.py':(R/'check.py','927b20cbaca9ac820dc8525dcd1e49ff39f76337f75867189675e720f8fb9373'),'s33-result.json':(R/'result.json','fc9e621bcb40c61defb0f8a511e8c52e7fa558ba5365f197a6b0da6cb1531146'),'s33.stdout':(R/'run_output.txt','77ed89b20910898d5d9f61beaef83e8d6032abbf5856533a4dcc52997b62efc4'),'s33-README.md':(R/'README.md','798ed34da0285cbd6ea92a896d419e2c7385996f87531bddb1ec335bfc1e3eec'),'upstream-producer.py':(U/'check.py','8e678e8979da5c8fa221778aa52f6b9275b87931858cad72bb01dcce373d73ec'),'upstream-result.json':(U/'result.json','192b1a2c921ff43ba99a81f4e1b588e4fc1de90014bd6ed43c75f874c70f59e6')}
retained=P/'retained';retained.mkdir(exist_ok=False)
for name,(source,pin) in expected.items():
    if sha(source)!=pin:raise RuntimeError('retained peer preimage moved')
    shutil.copyfile(source,retained/name)
source=(retained/'s33-producer.py').read_text();tree=ast.parse(source)
start=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='cwd' for t in n.targets))
nodes=tree.body[start:start+4]
if len(nodes)!=4 or not isinstance(nodes[2],ast.With) or ast.unparse(nodes[2])!='with contextlib.redirect_stdout(io.StringIO()):\n    import check as C' or ast.unparse(nodes[-1])!='os.chdir(cwd)':raise RuntimeError('actual import path changed')
if any(isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='C' and n.attr in ['allok','results'] for n in ast.walk(tree)):raise RuntimeError('producer now checks upstream; reconcile')
fragment='\n'.join(ast.get_source_segment(source,n) for n in nodes)+'\n'
F.mkdir(exist_ok=False);(F/'original-prefix.py').write_text(fragment,encoding='utf-8')
runner='''import contextlib,io,json,os,sys\nBASE=sys.argv[1]\nsys.path.insert(0,BASE)\ntry:\n    exec(compile(open(sys.argv[2]).read(),sys.argv[2],'exec'))\nexcept Exception as e:\n    print(json.dumps({'prefix_returned':False,'exception':repr(e)}));raise SystemExit(2)\nprint(json.dumps({'prefix_returned':True,'upstream_allok':C.allok,'upstream_rows':C.results,'exception':None}))\n'''
(F/'runner.py').write_text(runner,encoding='utf-8')
fixtures={'positive':"allok=True\nresults={'qualified':{'pass_':True}}\nprint('qualified PASS')\n",'reported-fail':"allok=False\nresults={'qualified':{'pass_':False}}\nprint('qualified FAIL; NOT ok')\n",'raised-failure':"raise RuntimeError('qualified upstream failure')\n"}
cases=[]
for label,text in fixtures.items():
    d=F/label;d.mkdir();(d/'check.py').write_text(text,encoding='utf-8')
    argv=[sys.executable,'-B',str(F/'runner.py'),str(d),str(F/'original-prefix.py')]
    run=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=15)
    (d/'stdout').write_bytes(run.stdout);(d/'stderr').write_bytes(run.stderr)
    observed=json.loads(run.stdout)
    expected_result=(run.returncode==2 and observed['prefix_returned'] is False and 'qualified upstream failure' in observed['exception']) if label=='raised-failure' else(run.returncode==0 and observed['prefix_returned'] is True and observed['upstream_allok']==(label=='positive'))
    row={'case':label,'argv':argv,'exit':run.returncode,'terminal':True,'exception':None,'fixture_sha256':sha(d/'check.py'),'observed':observed,'expected_behavior_observed':expected_result and not run.stderr,'method':'Labelled host module fixture through the exact retained import-prefix statements; no native/whole-S33/game execution'}
    (d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');cases.append(row)
historical=json.loads((retained/'upstream-result.json').read_text())
complete=len(cases)==3 and all(c['expected_behavior_observed'] for c in cases)
result={'complete':complete,'verdict':'REJECT_IMPORT_STAGE_UPSTREAM_VERDICT_PROPAGATION' if complete else'INVALID_CONTROL','driver_sha256':sha(Path(__file__)),'source_sha256':expected['s33-producer.py'][1],'prefix_sha256':sha(F/'original-prefix.py'),'cases':cases,'historical_upstream_report':{'ok':historical['ok'],'rows':len(historical['results']),'limits':'Current retained upstream record is positive; this latent guard defect does not prove it failed in the historical R7 run.'},'finding':'The exact import prefix returns normally and hides printed failure when upstreammodule reports allok=False. The full producer has no C.allok/C.results check. A raisedexception does stop this stage. Require checked nonempty upstreamverdict before accessingW/uc/S; preserve false/missing/exception diagnostics.','limits':'This runs only the actual import stage with labelled host modules. It does not claim that all eight downstream native cases passed under an injected failure, nor that historical outcomes are refuted. No full campaigns repeated.'}
(F/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'complete':complete,'verdict':result['verdict'],'cases':[{'case':c['case'],'exit':c['exit'],'prefix_returned':c['observed']['prefix_returned']} for c in cases],'native_runs':0,'game_runs':0}))
raise SystemExit(0 if complete else1)
