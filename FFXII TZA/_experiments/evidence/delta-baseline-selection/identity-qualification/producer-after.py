import ast,copy,hashlib,json
from pathlib import Path
from types import SimpleNamespace
W=Path(__file__).resolve().parent;output=W/'precondition-controls-next.json';assert not output.exists(),'Preserve existing controls; new execution requires a new identity';r=json.loads((W/'run-03/raw.json').read_text());source=(W/'capture.py').read_text();tree=ast.parse(source);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validate_verifier');ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'actual-default-validate_verifier','exec'),ns)
x=r['cases'][1];g=x['generations'][0];man=json.loads((W/'run-01/aligned-latest/store'/g['generation']/'MANIFEST.json').read_text());real=g['verify'];out=[]
for name,changes,expect in [('actual-retained-positive',{},True),('nonzero-current-looking-output',{'returncode':1},False),('invented-pass-output',{'stdout':'PASS\n'},False)]:
 d=copy.deepcopy(real);d.update(changes);q=SimpleNamespace(args=d['argv'],returncode=d['returncode'],stdout=d['stdout'],stderr=d['stderr']);error=None
 try:ns['validate_verifier'](q,g['generation'],man);accepted=True
 except AssertionError as e:accepted=False;error=str(e)
 assert accepted==expect,(name,accepted);out.append(dict(name=name,input=d,accepted=accepted,error=error))
calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='validate_verifier'];assert len(calls)==2
output.write_text(json.dumps(dict(method='Labelled receipt substitution to exact default predicate, not new Store/selector execution',source_sha256=hashlib.sha256((W/'capture.py').read_bytes()).hexdigest(),normalized_source_sha256=hashlib.sha256(source.encode()).hexdigest(),actual_default_call_lines=[n.lineno for n in calls],cases=out),indent=2)+'\n');print('ACTUAL_DEFAULT_PREDICATE_POSITIVE_AND_FAILURE_CONTROLS')
