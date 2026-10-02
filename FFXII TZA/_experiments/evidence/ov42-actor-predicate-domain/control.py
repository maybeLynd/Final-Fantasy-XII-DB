"""Concrete producer prerequisites and claim-connected decoded-record controls."""
import ast,copy,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;F=P/'controls-01';F.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if not json.loads((P/'proof-02.status.json').read_text()).get('terminal'):raise RuntimeError('missing positive invocation')
positive=json.loads((P/'result-01.json').read_text())
if positive.get('producer_complete') is not True:raise RuntimeError('missing positive result')
cases=[]
for label in ['missing-CFG','wrong-CFG-interface','missing-class-contract']:
 d=F/label;shutil.copytree(P,d,ignore=shutil.ignore_patterns('controls-01','control-*.status.json','control-*.stdout','control-*.stderr'))
 if label=='missing-CFG':(d/'prove_owner_reload_order.py').unlink()
 elif label=='missing-class-contract':(d/'retained/ov42-class20-action-admission/class20-admission-result-01.json').unlink()
 else:
  shutil.copyfile(d/'prove-title-queue-consumption.py',d/'prove_owner_reload_order.py')
  p=d/'input-identities-02.json';v=json.loads(p.read_text())
  for x in v['inputs']:
   if x['path']=='prove_owner_reload_order.py':x['sha256']=sha(d/'prove_owner_reload_order.py')
  p.write_text(json.dumps(v))
 out=d/'fresh-result.json';argv=[sys.executable,'-B',str(d/'prove.py'),str(out)]
 r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=30)
 (d/'stdout').write_bytes(r.stdout);(d/'stderr').write_bytes(r.stderr)
 need=(r.returncode!=0 and not out.exists())
 if label=='wrong-CFG-interface':need=need and b'required actual CFG prerequisite unavailable' in r.stderr
 row=dict(case=label,argv=argv,terminal=True,exit=r.returncode,exception=None,result_exists=out.exists(),expected_refusal=need,
          driver_sha256=sha(d/'prove.py'))
 (d/'status.json').write_text(json.dumps(row,indent=2)+'\n');cases.append(row)

# Compile the unchanged actual derive function only. The producer's checked CLI
# above remains separate; these records are synthetic inputs, not patched EXE.
source=(P/'prove.py').read_text();tree=ast.parse(source)
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='derive')
namespace={'RuntimeError':RuntimeError}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(P/'prove.py'),'exec'),namespace)
s=importlib.util.spec_from_file_location('tested_original_cfg',P/'prove_owner_reload_order.py');G=importlib.util.module_from_spec(s);s.loader.exec_module(G)
raw=json.loads((P/'retained/action-selector-local-exclusions/action-availability-gates-raw-01.json').read_text())
ix={int(i['pc'],16):i for q in raw['ranges'] if int(q['start'],16)==0x2ffcf0 for i in q['instructions']}
if namespace['derive'](ix,G)!=positive['facts']:raise RuntimeError('positive exact derive/result disagree')
synthetic=[]
for label,pc,args,code in [('action-carrier',0x2ffe9a,'ecx, ax','0fb7c8'),
                           ('parsed-record-carrier',0x2ffe97,'rdx, rsi','488bd6'),
                           ('class-failure-return',0x2ffd94,'eax, 0','b800000000')]:
 alt=copy.deepcopy(ix);alt[pc]['args']=args;alt[pc]['bytes']=code
 try:namespace['derive'](alt,G)
 except RuntimeError as e:synthetic.append(dict(case=label,pc=hex(pc),bytes=code,args=args,refused=True,diagnostic=str(e)))
 else:raise RuntimeError('named claim mutation admitted: '+label)
complete=len(cases)==3 and all(x['expected_refusal'] for x in cases) and len(synthetic)==3
(P/'control-result-01.json').write_text(json.dumps(dict(complete=complete,CLI_cases=cases,synthetic_derive_cases=synthetic,
 limits='Three actual CLI prerequisites and three synthetic decoded-record controls; no new shipping capture, table census or original-code execution'),indent=2)+'\n')
print(json.dumps(dict(complete=complete,CLI_cases=3,synthetic_derive_cases=3)))
raise SystemExit(0 if complete else 1)
