"""Returned reviewer counterexamples on the repaired actual default CLI.

No old census/control rerun. Fixtures are labelled; published input untouched.
"""
import hashlib, importlib.util, json, pathlib, shutil, sys
W=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('delivery',W/'prepare-residue-packet-publication.py')
M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
original=M.ROOT/'Database/FFXII TZA/_experiments/evidence/phyretext-member-boundaries'
root=W/'softedges-member-source-qualification-controls-01';root.mkdir()
names=['softedges-elements-callback-source-01/original-code.json','softedges-elements-callback-source-01/facts.json',
       'softedges-member-assignment-code-01.json','softedges-member-resolution-code-01.json','softedges-member-resolution-continuation-code-01.json']
checks=[]
for name in ['width-bytes-only','negative-status-bytes-only','negative-status-consistent','upstream-facts-missing']:
    case=root/name;src=case/'source';src.mkdir(parents=True)
    for f in names:
        p=src/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original/f,p)
    if name=='upstream-facts-missing':
        (src/names[1]).unlink()
    else:
        filename=names[4] if name=='width-bytes-only' else names[2]
        pc='0x59ed42' if name=='width-bytes-only' else '0x60effd'
        p=src/filename;v=json.loads(p.read_text());hits=0
        for q in v['ranges']:
            for i in q['instructions']:
                if i['pc']==pc:
                    i['bytes']='4401e8' if name=='width-bytes-only' else 'b800000000';hits+=1
                    if name=='negative-status-consistent':i['args']='eax, 0'
            q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
        if hits!=1:raise ValueError('ambiguous/missing exact reviewer target')
        p.write_text(json.dumps(v,indent=2),encoding='utf8')
    target=case/'must-not-exist.json';error=None
    try:M.checked_run([sys.executable,str(W/'check-softedges-member-boundaries.py'),str(src),str(target)],timeout=45,receipt_prefix=case/'actual-default-cli')
    except RuntimeError as e:error=str(e)
    if error is None or target.exists():raise ValueError('failed prerequisite accepted '+name)
    if name=='upstream-facts-missing':
        status=json.loads(pathlib.Path(str(target)+'.upstream-status.json').read_text())
        if status['exit']==0:raise ValueError('required legacy failure suppressed')
    checks.append(dict(case=name,status='PASS_REFUSED_NO_FINAL_RESULT',labelled_synthetic=True,error=error))
v=json.loads((W/'softedges-member-boundaries-result-03.json').read_text())
if len(v['source_qualification'])!=4 or len(v['established'])!=3:raise ValueError('positive missing/incomplete')
with (root/'result.json').open('x') as f:json.dump(dict(status='PASS_RETURNED_DEFECT_REPAIR_CONTROLS_INDEPENDENT_PENDING',checks=checks,
    positive_sha256=hashlib.sha256((W/'softedges-member-boundaries-result-03.json').read_bytes()).hexdigest(),
    driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    limits='Four actual default CLI refuses; prior three semantic claims remain accepted at legacy identity, new repair independent pending. No repeated reviewer census or native/live experiments.'),f,indent=2)
print('Both returned byte-only defects, consistent changed bytes and required upstream failure refused; no final result')
