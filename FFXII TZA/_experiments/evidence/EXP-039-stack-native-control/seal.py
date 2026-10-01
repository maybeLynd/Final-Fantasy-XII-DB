"""Validate exact EXP038 source and the native cold/positive evidence census."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess

HERE=Path(__file__).resolve().parent
CAPTURE=HERE.parent/'EXP-038-handler-stack'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text())


summary={}
for mode in ('cold','positive'):
    folder=HERE/mode
    assert {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}=={
        'target-ready.json','heartbeat.bin','capture-console.txt','control.json','capture/result.json','capture/api.json'}
    control=read(folder/'control.json');result=read(folder/'capture/result.json')
    info=read(folder/'target-ready.json');audit=read(folder/'capture/api.json')
    assert control['status']==result['status']=='PASS' and control['capture_exit']==0
    assert control['target_source_sha256']==sha(HERE/'target.py')
    assert control['harness_sha256']==sha(HERE/'run_control.py')
    assert control['native_code_before']==control['native_code_after']
    assert control['native_code_before']['sha256']==info['code_sha256']
    assert info['entry']==info['address']+32 and info['cold']==info['address']+33
    assert info['return_address']==info['address']+9
    assert len(control['post'])==4
    assert all(x['exit'] is None and x['debugger'] is False for x in control['post'])
    deltas=[control['post'][i+1]['beats']-control['post'][i]['beats'] for i in range(3)]
    assert all(x>0 for x in deltas) and control['final_exits']==[0,1]
    assert result['detach'] and not result['errors'] and result['cleanup']['status']=='PASS'
    assert result['cleanup']['clears'] and result['cleanup']['verified']
    assert all(ok for _,ok in result['cleanup']['clears']+result['cleanup']['verified'])
    for name,value in result['sources'].items():
        assert sha(CAPTURE/name)==value
        relative=(CAPTURE/name).relative_to(Path.cwd()).as_posix()
        original=subprocess.check_output(['git','show','ea38079:'+relative])
        assert hashlib.sha256(original).hexdigest()==value
    stacks=[(i,x) for i,x in enumerate(audit) if x['operation']=='stopped_stack_read']
    assert len(stacks)==len(result['hits'])==control['hits']
    assert len(stacks)==0 if mode=='cold' else len(stacks)>0
    for index,(position,row) in enumerate(stacks):
        hit=result['hits'][index]
        assert row['status']=='READ' and row['tid']==hit['tid'] and row['rip']==hit['rip']==info['entry']
        assert row['raw']==hit['stack']['raw']
        raw=bytes.fromhex(row['raw']);assert len(raw)==64
        assert row['qwords']==list(struct.unpack('<8Q',raw))
        assert row['top_qword']==row['qwords'][0]==info['return_address']
        previous=next(x for x in reversed(audit[:position]) if x['operation'] in ('WaitForDebugEvent','ContinueDebugEvent'))
        following=next(x for x in audit[position+1:] if x['operation'] in ('WaitForDebugEvent','ContinueDebugEvent'))
        assert previous['operation']=='WaitForDebugEvent' and previous['exception']==0x80000004
        assert following['operation']=='ContinueDebugEvent' and following['result']
        assert previous['tid']==following['tid']==row['tid']
    summary[mode]=dict(hits=len(stacks),known_return=hex(info['return_address']),
                       verified_threads=len(result['cleanup']['verified']),post_heartbeat_deltas=deltas)
(HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
files={p.relative_to(HERE).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p))
       for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(HERE/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n')
print(json.dumps(summary))
