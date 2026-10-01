import copy,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;D=W/'reducer-controls';assert not D.exists();D.mkdir();receipts=[]
for name in ('incomplete-good-cases','nonzero-good-results'):
    p=D/name;shutil.copytree(W/'activity-02',p)
    if name=='incomplete-good-cases':
        r=json.loads((p/'raw.json').read_text());r['finished']=False;r['fatal']={'type':'LABELLED_SETUP_FAILURE','detail':'control before semantic acceptance'}
        (p/'raw.json').write_text(json.dumps(r,indent=2)+'\n');marker='INCOMPLETE_CAPTURE'
    else:
        r=json.loads((p/'invocation.json').read_text());r['returncode']=1
        (p/'invocation.json').write_text(json.dumps(r,indent=2)+'\n');marker='UPSTREAM_FAILED'
    args=[sys.executable,'-B',str(W/'check.py'),'--activity',str(p)]
    q=subprocess.run(args,capture_output=True,text=True,timeout=10)
    assert q.returncode!=0 and marker in q.stderr and 'REJECT_ACTIVITY_WRITER_ATTRIBUTION' not in q.stdout
    c={'name':name,'args':args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'expected':marker,'terminal':True}
    (D/(name+'-receipt.json')).write_text(json.dumps(c,indent=2)+'\n');receipts.append(c)
(W/'reducer-controls.json').write_text(json.dumps({'finished':True,'controls':receipts,'credit':'two producer reducer controls, not new activity executions or independent acceptance'},indent=2)+'\n')
print('ACTIVITY_REDUCER_REFUSALS',len(receipts))
