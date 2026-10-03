"""Concrete CLI prerequisite controls for this query qualification path."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out=P/sys.argv[1]
    if out.exists():raise ValueError('fresh controls required')
    out.mkdir();cases=[]
    for label,filename,key,value,error in [
      ('failed-upstream-proof','proof-02.status.json','exit',1,'base invariant result/status failed'),
      ('incomplete-current-metadata','singleton-extents-01.json','complete',False,'required complete current extent artifact'),
      ('incomplete-current-wrapper','singleton-source-01.json','wrapper_complete',False,'required complete current capture wrapper')]:
        f=out/label;f.mkdir()
        for q in P.iterdir():
            if q.is_file():shutil.copy2(q,f/q.name)
        target=f/filename;prior=target.read_bytes();x=json.loads(prior);x[key]=value
        target.write_text(json.dumps(x,indent=2));(f/'mutation.json').write_text(json.dumps(dict(file=filename,key=key,value=value,preimage_sha256=hashlib.sha256(prior).hexdigest()),indent=2))
        result=f/'fresh-result.json'
        argv=[sys.executable,'-B',str(f/'qualify-singleton.py'),result.name]
        r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=45)
        (f/'stdout').write_bytes(r.stdout);(f/'stderr').write_bytes(r.stderr)
        row=dict(label=label,argv=argv,exit=r.returncode,expected_error=error,expected_error_seen=error.encode() in r.stderr,result_absent=not result.exists(),driver_sha256=sha(f/'qualify-singleton.py'))
        (f/'status.json').write_text(json.dumps(row,indent=2));cases.append(row)
        if not row['exit'] or not row['expected_error_seen'] or not row['result_absent']:
            raise ValueError('concrete prerequisite refusal failed '+label)
    result=dict(status='PASS_ACTUAL_PREREQUISITE_CONTROLS_INDEPENDENT_PENDING',driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'qualify-singleton.py'),cases=cases,limits='Three actual Python CLI artifact refusals, not game/native execution, semantic acceptance or extra original instruction coverage.')
    (out/'result.json').write_text(json.dumps(result,indent=2));print('Three exact upstream/artifact failures refused without downstream result')

if __name__=='__main__':main()
