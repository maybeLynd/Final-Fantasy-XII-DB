"""Focused actual producer invocation refusals; reuse the retained positive."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    out=P/'control-result-01.json';D=P/'controls-01'
    if out.exists() or D.exists():raise ValueError('fresh control output required')
    r=json.loads((P/'result-01.json').read_text());s=json.loads((P/'prove-01.status.json').read_text())
    if r.get('producer_complete') is not True or r['driver_sha256']!=sha(P/'prove.py') or s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py'):raise ValueError('current actual positive required')
    files=[p for p in P.iterdir() if p.is_file()];D.mkdir();cases=[]
    for label,name,key,value,marker in [
      ('target-extent-incomplete','target-extents-01.json','complete',False,'required complete current extent artifact'),
      ('target-wrapper-incomplete','target-source-01.json','wrapper_complete',False,'required complete current capture wrapper'),
      ('target-capture-failed','capture-target-01.status.json','exit',1,'required successful capture-target-01')]:
        q=D/label;q.mkdir()
        for f in files:shutil.copyfile(f,q/f.name)
        x=json.loads((q/name).read_text());x[key]=value;(q/name).write_text(json.dumps(x,indent=2))
        inputs=[dict(path=f.name,sha256=sha(f),bytes=f.stat().st_size) for f in sorted(q.iterdir()) if f.is_file()]
        cmd=[sys.executable,'-B',str(q/'prove.py'),'refused.json']
        z=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,timeout=45)
        (q/'producer.stdout').write_bytes(z.stdout);(q/'producer.stderr').write_bytes(z.stderr)
        (q/'producer.status.json').write_text(json.dumps(dict(argv=cmd,terminal=True,exit=z.returncode,exception=None,driver_sha256=sha(q/'prove.py')),indent=2))
        if z.returncode==0 or(q/'refused.json').exists() or marker not in z.stderr.decode(errors='replace'):raise ValueError('actual prerequisite refusal failed '+label)
        cases.append(dict(label=label,inputs=inputs,delta=dict(path=name,key=key,value=value),expected=marker,refused_without_result=True))
        for f in list(q.iterdir()):
            if f.is_file() and(P/f.name).is_file() and f.read_bytes()==(P/f.name).read_bytes():f.unlink()
    out.write_text(json.dumps(dict(complete=True,driver_sha256=sha(Path(__file__)),positive_reused='prove-01 actual current positive, not another semantic run',artifact_cases=cases,source_controls=r['source_controls'],limits='Three actual CLI prerequisite refusals/four synthetic source controls; no native or live execution, no independent acceptance.'),indent=2))
    print('VALIDATED actual target capture status/extent/wrapper prerequisite refusals; retained positive reused')
if __name__=='__main__':main()
