"""One actual CLI refusal of labelled failed-upstream status; no native execution."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
proof=P/'prove-mode-query-boundary.py'
if hashlib.sha256(proof.read_bytes()).hexdigest()!='e83a3f7b3e717c41f9a5b8292684d59c04c82e242d01c0df2d978f185cc9f9f0':raise ValueError('Reviewed current producer changed')
positive=json.loads((P/'prove-mode-query-02.status.json').read_text());result=json.loads((P/'result-mode-query-02.json').read_text())
if positive['terminal'] is not True or positive['exit']!=0 or positive['exception'] is not None or result.get('producer_complete') is not True or len(result['controls'])!=5:raise ValueError('Actual positive incomplete')
D=P/'controls-mode-query-status-01';D.mkdir()
s=json.loads((P/'capture-mode-query-01.status.json').read_text());s['exit']=1
status=D/'labelled-failed-upstream.status.json';status.write_text(json.dumps(s,indent=2))
out=D/'must-not-exist.json'
argv=[sys.executable,'-B',str(proof),out.relative_to(P).as_posix(),status.relative_to(P).as_posix()]
r=subprocess.run(argv,cwd=ROOT,stdin=subprocess.DEVNULL,capture_output=True,timeout=15)
(D/'stdout').write_bytes(r.stdout);(D/'stderr').write_bytes(r.stderr)
(D/'receipt.json').write_text(json.dumps(dict(argv=argv,terminal=True,exit=r.returncode,exception=None),indent=2))
if r.returncode!=1 or b'required upstream capture failed/incomplete' not in r.stderr or out.exists():raise ValueError('Failed upstream did not stop actual invocation')
(D/'result.json').write_text(json.dumps(dict(complete=True,status='ACTUAL_CLI_REFUSAL_WITHOUT_RESULT',method='Labelled synthetic upstream-failure receipt through unchanged current producer CLI; not a failed real capture or FF12 execution',positive='Retained actual prove-mode-query-02, no repeat',negative_exit=r.returncode,result_absent=True,producer_sha256=hashlib.sha256(proof.read_bytes()).hexdigest()),indent=2))
print('Actual failed-upstream CLI refused exit1/no result; retained positive complete. No FF12 execution.')
