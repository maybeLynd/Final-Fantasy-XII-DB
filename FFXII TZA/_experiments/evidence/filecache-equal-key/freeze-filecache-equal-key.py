"""Freeze only after actual checked producer/control paths; preserve all failures."""
import hashlib
import json
from pathlib import Path
import shutil
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
BASE=['capture-filecache-equal-key.py','capture-index-path.py','validate-title-source-annotations.py',
      'prove_owner_reload_order.py','filecache-equal-key-source-01.json',
      'filecache-equal-key-capture-01.status.json','filecache-equal-key-capture-01.stdout',
      'filecache-equal-key-capture-01.stderr']
def main():
    out=W/'filecache-equal-key-frozen-ready'
    if out.exists():raise ValueError('immutable packet exists')
    for prefix,driver in [('filecache-equal-key-capture-01','capture-filecache-equal-key.py'),
                          ('filecache-equal-key-positive-02','prove-filecache-equal-key.py'),
                          ('filecache-equal-key-controls-run-01','control-filecache-equal-key.py')]:
        st=json.loads((W/(prefix+'.status.json')).read_text())
        if st.get('exit')!=0 or st.get('terminal') is not True or st.get('driver_sha256')!=sha(W/driver):raise ValueError('required upstream failed/incomplete/stale')
        if not(W/(prefix+'.stdout')).read_bytes().strip() or (W/(prefix+'.stderr')).read_bytes():raise ValueError('required stdout missing/stderr present')
    r=json.loads((W/'filecache-equal-key-result-01.json').read_text())
    if r.get('producer_complete') is not True or len(r['graphs'])!=5 or r['instruction_assertions']!=63 or r['driver_sha256']!=sha(W/'prove-filecache-equal-key.py') or r['annotation_check']['instruction_records']!=283:
        raise ValueError('required nonempty result incomplete')
    for x in r['source_pins']+r['tool_pins']:
        if sha(W/x['path'])!=x['sha256']:raise ValueError('required source/tool moved')
    c=json.loads((W/'filecache-equal-key-controls-01/result.json').read_text())
    if c.get('complete') is not True or c.get('status')!='PASS_FOUR_ACTUAL_REFUSALS' or len(c['cases'])!=4 or not all(x['passed'] and x['terminal'] and x['exit']!=0 and x['result_absent'] for x in c['cases']):raise ValueError('actual controls invalid/incomplete')
    if c['driver_sha256']!=sha(W/'control-filecache-equal-key.py') or c['producer_sha256']!=sha(W/'prove-filecache-equal-key.py'):raise ValueError('controls tool changed')
    files=BASE+['prove-filecache-equal-key.py','control-filecache-equal-key.py','freeze-filecache-equal-key.py',
       'run-filecache-equal-key.py','run-filecache-equal-key-before-forwarded-args-01.py',
       'filecache-equal-key-wrapper-args-failure-01.json','filecache-equal-key-result-01.json',
       'FILECACHE-EQUAL-KEY-METHOD-1001.md','filecache-equal-key-controls-01/result.json']
    for prefix in ['filecache-equal-key-positive-02','filecache-equal-key-controls-run-01']:
        files.extend(prefix+suffix for suffix in ['.status.json','.stdout','.stderr'])
    for case in c['cases']:
        base=Path('filecache-equal-key-controls-01')/case['tag']
        for name,pin in case['inherited_from_baseline'].items():
            if sha(W/base/name)!=pin or sha(W/name)!=pin:raise ValueError('control baseline delta is not lossless')
        if sha(W/base/case['changed_file'])!=case['changed_sha256']:raise ValueError('control delta changed')
        files.extend((base/name).as_posix() for name in [case['changed_file'],'stdout','stderr','receipt.json'])
    out.mkdir()
    for name in sorted(set(files)):
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,p)
    shutil.copy2(W/'FILECACHE-EQUAL-KEY-README-1001.md',out/'README.md')
    (out/'.gitattributes').write_text('* -text\n')
    members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps(dict(kind='conditional original cache numeric-key reuse proof',members=members),indent=2)+'\n')
    print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))
if __name__=='__main__':main()
