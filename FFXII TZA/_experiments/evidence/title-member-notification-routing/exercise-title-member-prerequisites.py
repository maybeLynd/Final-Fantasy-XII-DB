"""Actual checker invocation controls for OV29 routing; private input copies only.
No shipping instructions are executed by these controls. No result can be accepted
after an unchecked subprocess/exception or failed capture prerequisite.
Usage: python exercise-title-member-prerequisites.py FRESH_CASE_DIR
"""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable case directory exists')
out.mkdir()
driver=W/'prove-title-member-notification.py';source=driver.read_text()
old='W=pathlib.Path(__file__).resolve().parent; ROOT=W.parents[4]'
if source.count(old)!=1:raise ValueError('input-root adaptation unavailable')
adapted=source.replace(old,'W=pathlib.Path(__file__).resolve().parent; ROOT=pathlib.Path('+repr(str(ROOT))+')')
names=['capture-index-path.py','capture-title-watcher-lifetime.py','capture-title-member-routing.py',
       'capture-title-watcher-attachment.py','title-watcher-lifetime-raw-02.json',
       'title-member-routing-raw-01.json','title-watcher-attachment-raw-01.json']
cases=['positive','incomplete_wrapper','failed_role','missing_source','changed_instruction_bytes']
receipts=[]
for case in cases:
    c=out/case;c.mkdir()
    for name in names:shutil.copyfile(W/name,c/name)
    shutil.copytree(W/'section04-title-member-source',c/'section04-title-member-source')
    (c/driver.name).write_text(adapted)
    p=c/'title-member-routing-raw-01.json'
    if case=='missing_source':p.unlink()
    elif case!='positive':
        r=json.loads(p.read_text())
        if case=='incomplete_wrapper':r['wrapper_complete']=False
        elif case=='failed_role':r['controls'][0]['observed']='r'
        elif case=='changed_instruction_bytes':r['ranges'][0]['instructions'][0]['bytes']='90'
        p.write_text(json.dumps(r,indent=2)+'\n')
    result=c/'result.json'
    run=subprocess.run([sys.executable,str(c/driver.name),str(result)],cwd=ROOT,capture_output=True,text=True)
    (c/'stdout.txt').write_text(run.stdout);(c/'stderr.txt').write_text(run.stderr)
    valid=(run.returncode==0 and result.exists()) if case=='positive' else (run.returncode!=0 and not result.exists())
    if case=='positive' and valid:
        rr=json.loads(result.read_text());valid=bool(rr.get('established')) and all(rr['controls'].values())
    receipt=dict(case=case,exit=run.returncode,result_exists=result.exists(),expected_accepted=case=='positive',control_pass=valid,
        invocation=[sys.executable,c.name+'/'+driver.name,c.name+'/result.json'],
        stdout_sha256=hashlib.sha256(run.stdout.encode()).hexdigest(),stderr_sha256=hashlib.sha256(run.stderr.encode()).hexdigest())
    (c/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');receipts.append(receipt)
    if not valid:raise ValueError('actual checker invocation control failed:'+case)
(out/'result.json').write_text(json.dumps(dict(status='COMPLETE',driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest(),
    method='producer prerequisite controls, not native or live execution',adaptation='private local input root only; canonical EXE and retained SECTION04 sources unchanged',
    cases=receipts),indent=2)+'\n')
print('COMPLETE five actual invocation cases; positive accepted, four prerequisite defects refused/no-result.')
