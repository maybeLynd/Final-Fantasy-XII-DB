"""Read-only reduction of stopped-event native controls; no native API calls."""
import ast
import copy
import ctypes as C
import ctypes.wintypes as wt
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
FIX=ROOT/'Database/FFXII TZA/_experiments/evidence/exp127-instrument-control'
FP=FIX.parent/'native-fp-context-control'
sys.path.insert(0,str(FIX))
from ownership import owned_step
from project import project

spec=importlib.util.spec_from_file_location('read_only_native_fp_values',FP/'fixture.py')
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
tree=ast.parse((FIX/'original/hwbp-source.py').read_text())
defs=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name in ('M128A','CONTEXT')]
assert len(defs)==2
ns={'ctypes':C,'w':wt};exec(compile(ast.Module(body=defs,type_ignores=[]),'frozen CONTEXT classes','exec'),ns)
Context=ns['CONTEXT']


def validate(d):
    plan,ready,owner,result,cap,obs,api=(d[n] for n in ['plan','target-ready','owned-child','result','capture','stopped-observation','api'])
    arm=plan['arm'];assert arm in ('normal','abort','read-failure')
    assert ready['sources']==plan['sources']
    assert ready['identity']==owner['identity'] and owner['popen_pid']==ready['identity']['pid']
    assert plan['parent_pid']==ready['parent_pid']==owner['parent_pid']
    assert plan['nonce']==ready['nonce'] and len(plan['nonce'])==36
    assert ready['identity']['creation']>0
    assert ready['identity']['image_sha256']==plan['host']['python_sha256']
    assert result['status']=='NATIVE_STOP_CONTROL_OBSERVED' and not result['forced_termination']
    assert result['read_handle_closed'] and result['parent_mapping_closed'] and cap['handle_closed']
    assert result['final_exits']['debugger']==0
    assert cap['arming'] and all(x[1] for x in cap['arming'])
    assert len(cap['hits'])==1,'not the bounded first-event control'
    event=obs['event'];row=obs['context_read'];values=project(row)
    assert values==obs['values'] and row['event']==event
    assert row['thread_binding']['tid']==event['tid']==ready['tid'] and event['pid']==ready['identity']['pid']
    assert event['first_chance']==1 and event['code']==1 and event['exception']==0x80000004
    assert event['address']==values['rip']==ready['gate_address']
    ctx=Context.from_buffer_copy(bytes.fromhex(row['context_hex']))
    assert owned_step(ctx,event['address'],[ready['gate_address']])
    assert values['rax']==0x1122334455667788 and values['rdi']==ready['path_address']
    assert values['r10']==ready['counter_address'] and values['rbx']==values['rcx']==ready['buffer_address']>0xffffffff
    assert ready['path_address']==ready['buffer_address']+0xb00 and ready['counter_address']==ready['buffer_address']+0xa00
    assert obs['path_hex']==ready['path_hex'] and bytes.fromhex(obs['path_hex']).endswith(b'\0')
    assert struct.unpack('<QQQ',bytes.fromhex(obs['counter_hex']))==(obs['before'],obs['after'],obs['saved_rdi'])
    assert obs['before']==obs['after']+1 and result['stopped_counters']==[obs['before'],obs['after']]
    # Independently locate the API context receipt and its native read/handle.
    i=row['api_index'];rawrow=api[i]
    for key,value in row.items():
        if key not in ('api_index',):assert rawrow[key]==value,('context receipt mismatch',key)
    assert api[i-1]['operation']=='GetThreadContext' and api[i-1]['handle']==row['handle'] and api[i-1]['result']==1
    opened=api[row['thread_binding']['open_index']]
    assert opened['operation']=='OpenThread' and opened['tid']==event['tid'] and opened['result']==row['handle']
    assert api[i+1]['operation']=='CloseHandle' and api[i+1]['handle']==row['handle'] and api[i+1]['result']==1
    # Every read must occur inside this event, with no intervening continuation.
    begin=obs['read_begin'];end=obs['read_end'];reads=api[begin:end]
    assert reads and all(r['operation']=='ReadProcessMemory' and r['event']==event for r in reads)
    assert all(r['result']==1 and r['transferred']==r['requested']==len(bytes.fromhex(r['raw_hex'])) for r in reads)
    assert reads[0]['address']==ready['code_address'] and reads[0]['raw_hex']==ready['code_hex']
    assert reads[-1]['address']==ready['counter_address'] and reads[-1]['raw_hex']==obs['counter_hex']
    path=bytes.fromhex(ready['path_hex']);assert len(reads[1:-1])==len(path)
    for off,r in enumerate(reads[1:-1]):
        assert r['address']==ready['path_address']+off and r['requested']==1 and bytes.fromhex(r['raw_hex'])==bytes([path[off]])
    # Pair every successful Wait with its exact continuation, including cleanup.
    active=None;observer_group=None
    for index,r in enumerate(api):
        if r['operation']=='WaitForDebugEvent' and r['result']:
            assert active is None,'event overlapped before continuation';active=(index,r)
        elif r['operation']=='ContinueDebugEvent':
            assert active and r['result']==1
            a,ev=active;assert (r['pid'],r['tid'])==(ev['pid'],ev['tid'])
            if a<i<index:observer_group=(a,index)
            active=None
    assert active is None and observer_group and observer_group[0]<i<begin<end<=observer_group[1]
    decision=next((j,r) for j,r in enumerate(api) if r['operation']=='scoped_decision')
    assert decision[0]>=end and decision[1]['tid']==event['tid']
    terminate=[(j,r) for j,r in enumerate(api) if r['operation']=='TerminateProcess']
    observed_then=api[decision[0]+1:observer_group[1]]
    final=list(struct.unpack_from('<QQ',d['shared-final'],0xa00))
    assert final==result['final_counters']
    samples=d['samples'];assert samples and len(samples)==result['samples']
    for sample in [d['baseline'],*samples]:
        fixture.verify_sample(sample,'preserve',allow_fip_truncation=True)
        assert sample['counters'][0]==sample['counters'][1]
    if arm=='normal':
        assert cap['status']==result['capture_status']=='MATCHED_PENDING_HEALTH' and not cap['errors'] and cap['abort'] is None
        assert cap['cleanup']['status']=='PASS' and cap['detach'] and cap['observations']
        assert cap['cleanup']['clears'] and cap['cleanup']['verified'] and all(x[1] for x in cap['cleanup']['clears']+cap['cleanup']['verified'])
        assert decision[1]['decision']=='STOP_MATCHED_PENDING_HEALTH' and not terminate
        assert any(r['operation']=='SetThreadContext' and r['result']==1 for r in observed_then)
        assert final[0]==final[1]>=obs['before'] and result['final_exits']['target']==0
        ended=d['target-exit'];assert ended['normal'] and ended['code_freed'] and ended['shared_mapping_closed'] and not ended['debugger_present']
        assert samples[-1]['counters']==final
    else:
        assert cap['status']==result['capture_status']=='CONTROL_ABORTED' and cap['abort']['terminal']
        assert cap['abort']['pending_event_serviced'] and cap['abort']['exit_event'] and cap['abort']['wait_result']==0 and cap['abort']['exit_code']==0xea03
        assert decision[1]['decision']=='HOLD_FOR_OWNED_ABORT' and len(terminate)==1
        assert decision[0]<terminate[0][0]<observer_group[1] and terminate[0][1]['result']==1 and terminate[0][1]['exit_code']==0xea03
        assert not any(r['operation'] in ('GetThreadContext','SetThreadContext') for r in observed_then),'resume context operation after hold'
        assert final==[obs['before'],obs['after']] and result['final_exits']['target']==0xea03
        assert d['target-exit'] is None,'no target finally/free claim on termination'
        assert cap['cleanup'] is None
        if arm=='abort':assert not cap['errors'] and cap['observations']
        else:
            assert cap['errors']==['observer failed: OSError: intentional NOACCESS read control; no resume permitted'] and not cap['observations']
            failed=[r for r in api if r['operation']=='ReadProcessMemory' and not r['result']]
            assert len(failed)==1 and failed[0]['address']==ready['guard_address'] and failed[0]['event']==event
            assert failed[0]['transferred']==0 and failed[0]['raw_hex']=='' and failed[0]['error']==299
    semantic_bytes=1232+sum(r['requested'] for r in reads)
    assert semantic_bytes<32768
    return dict(arm=arm,pid=event['pid'],tid=event['tid'],stopped=[obs['before'],obs['after']],final=final,
                path_address=values['rdi'],counter_address=values['r10'],rax=values['rax'],
                selected_context_and_read_bytes=semantic_bytes,capture_status=cap['status'],target_exit=result['final_exits']['target'],
                exact_stopped_event_binding=True,normal_target_finally=arm=='normal')


def main():
    outcomes=[];rejected=[];hashes={}
    for arm in ('normal','abort','read-failure'):
        folder=W/('native-stop-'+arm+'-1')
        names=['plan','target-ready','owned-child','result','capture','stopped-observation','api','baseline']
        data={n:json.loads((folder/(n+'.json')).read_text()) for n in names}
        data['target-exit']=json.loads((folder/'target-exit.json').read_text()) if (folder/'target-exit.json').exists() else None
        data['shared-final']=(folder/'shared-final.bin').read_bytes()
        data['samples']=[json.loads(s) for s in (folder/'samples.jsonl').read_text().splitlines()]
        for p,h in data['plan']['sources'].items():assert sha(ROOT/p)==h,p
        code=(folder/'fixture.bin').read_bytes();assert code.hex()==data['target-ready']['code_hex']
        desc=json.loads((folder/'fixture.json').read_text());assert data['target-ready']['gate_address']==data['target-ready']['code_address']+desc['gate']
        original,oldgate=fixture.make('preserve');before=bytes.fromhex(desc['changes']['inserted_before_hex']);after=bytes.fromhex(desc['changes']['inserted_after_hex'])
        assert desc['changes']['original_gate']==oldgate and desc['changes']['original_sha256']==hashlib.sha256(original).hexdigest()
        assert code==original[:oldgate]+before+b'\x90'+after+original[oldgate+1:]
        assert before.hex()=='48ff83000a00004889bb100a0000488dbb000b00004c8d93000a000048b88877665544332211'
        assert after.hex()=='48ff83080a0000488bbb100a0000'
        assert b''.join(bytes.fromhex(r['bytes']) for r in desc['instructions'])==code
        outcomes.append(validate(data))
        hashes[folder.name]={p.name:sha(p) for p in folder.iterdir() if p.is_file()}
        def reject(label,bad):
            try:validate(bad)
            except (AssertionError,KeyError):rejected.append(arm+': '+label)
            else:raise AssertionError('bad native evidence accepted: '+label)
        if arm=='normal':
            bad=copy.deepcopy(data);bad['capture']['hits']=[];reject('empty control',bad)
            bad=copy.deepcopy(data);bad['stopped-observation']['context_read']['thread_binding']['tid']+=1;reject('wrong observer thread',bad)
            bad=copy.deepcopy(data);bad['api'][bad['stopped-observation']['read_begin']]['event']['id']+=1;reject('read from another event',bad)
            bad=copy.deepcopy(data);bad['capture']['cleanup']['verified'][0][1]=False;reject('failed debug-register readback',bad)
            bad=copy.deepcopy(data);bad['target-exit']['code_freed']=False;reject('missing normal allocation cleanup',bad)
            bad=copy.deepcopy(data);bad['owned-child']['identity']['creation']+=1;reject('wrong process creation identity',bad)
        else:
            bad=copy.deepcopy(data);raw=bytearray(bad['shared-final']);struct.pack_into('<Q',raw,0xa08,bad['stopped-observation']['before']);bad['shared-final']=bytes(raw);bad['result']['final_counters'][1]+=1;reject('successor executed despite abort',bad)
            bad=copy.deepcopy(data);bad['capture']['status']='MATCHED_PENDING_HEALTH';reject('abort promoted to healthy capture',bad)
            bad=copy.deepcopy(data);j=next(i for i,r in enumerate(bad['api']) if r['operation']=='TerminateProcess');bad['api'][j]['operation']='SetThreadContext';reject('resume write in place of terminate',bad)
    out=dict(status='NATIVE_STOP_CONTROLS_REVIEWABLE',method='Native instrument controls using supplied shared state; not shipping code or live FF12',
             outcomes=outcomes,rejected=rejected,raw_sha256=hashes,
             limits=['One normal, one intentional abort and one failed-read abort on this host/fixture.',
                     'Counters establish successor execution/nonexecution only in this controlled single-writer fixture.',
                     'Successful API raw last-error values can be stale; result and transfer count govern read acceptance.',
                     'No target-finally/allocation-free observation after intentional termination; subject exit is the boundary.',
                     'No FF12 allocation/caller/queue/crash claim or whole-state/scheduling transparency; FIP counterexample remains.',
                     'Native operating controls do not replace live initial-state, responsiveness and restoration proof.'])
    if '--write' in sys.argv:
        with (W/'native-stop-observation.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((W/'native-stop-observation.json').read_text())==out
    print('Native stopped-read/resume/abort controls verified from raw context/API/shared markers;',len(rejected),'corruptions reject. No FF12 semantic closure.')


if __name__=='__main__':main()
