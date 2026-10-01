"""Check retained native receipts only. Never launches, attaches or writes context."""
import copy
import hashlib
import json
from pathlib import Path

E = Path(__file__).resolve().parent
FIX = E.parent / 'exp127-instrument-control'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())


def reduce_arm(mode, data):
    ready, capture, result, api, exit_info = [data[k] for k in ('ready','capture','result','api','exit')]
    assert ready['pid'] == result['owned_child_pid']
    assert len(ready['baseline_handler']) == 1
    assert ready['baseline_handler'][0]['code'] == 0x80000004
    assert result['baseline']['debugger'] is False and result['baseline']['exit'] is None
    assert capture['hits'] and all(h['rip']==ready['address'] for h in capture['hits'])
    assert capture['detach'] and capture['cleanup']['status']=='PASS'
    assert capture['arming'] and all(x[1] for x in capture['arming'])
    for key in ('clears','verified'):
        assert capture['cleanup'][key] and all(x[1] for x in capture['cleanup'][key])
    assert result['forced_termination']==[] and result['final_exits']=={'debugger':0,'target':0}
    assert exit_info['normal_exit'] and exit_info['handler_removed'] and exit_info['allocation_freed']
    assert not exit_info['debugger_present']
    post=result['post']
    assert len(post)==4 and all(not r['debugger'] and r['exit'] is None for r in post)
    assert all(b['beats']>a['beats'] for a,b in zip(post,post[1:]))
    groups, group = [], None
    for row in api:
        if row['operation']=='WaitForDebugEvent' and row['result']:
            assert group is None
            group=[row]
        elif row['operation']=='ContinueDebugEvent':
            assert group and row['result']
            assert row['pid']==group[0]['pid']==ready['pid'] and row['tid']==group[0]['tid']
            group.append(row);groups.append(group);group=None
        elif group is not None:group.append(row)
    assert group is None and groups
    steps=[g for g in groups if g[0].get('exception')==0x80000004]
    own=[g for g in steps if g[0]['address']==ready['address']]
    foreign=[g for g in steps if g[0]['address']!=ready['address']]
    assert own and len(own)>=len(capture['hits'])
    out=dict(pid=ready['pid'],own_main_hits=len(capture['hits']),own_api_steps=len(own),
             foreign_events=len(foreign),handler_total=len(exit_info['handler_events']),
             post_heartbeat_sizes=[r['beats'] for r in post],normal_exit=True,
             capture_status=capture['status'])
    if mode=='positive':
        assert not foreign and capture['status']=='PASS' and not capture['errors']
        assert not capture['trigger_issued'] and len(exit_info['handler_events'])==1
    else:
        assert len(foreign)==1 and capture['status']=='INVALID' and capture['trigger_issued']
        expected_error=('unrecognized or unreadable single step' if mode=='original'
                        else 'unowned or unreadable single step; no resume write')
        assert capture['errors']==[expected_error]
        g=foreign[0]
        chances=[r for r in g if r['operation']=='exception_chance']
        writes=[r for r in g if r['operation']=='SetThreadContext']
        assert len(chances)==1 and chances[0]['first_chance']==1
        expected_status=0x10002 if mode=='original' else 0x80010001
        assert g[-1]['status']==expected_status
        assert len(writes)==(1 if mode=='original' else 0)
        if writes:
            assert writes[0]['result'] and writes[0]['context']['Dr6']==0
            assert writes[0]['context']['EFlags'] & 0x10000
        delivery=data['delivery']
        assert delivery['before']==1 and delivery['returned_from_raise']
        assert delivery['after']==len(exit_info['handler_events'])==(1 if mode=='original' else 2)
        if mode=='candidate':
            actual=exit_info['handler_events'][-1]
            assert actual['code']==g[0]['exception'] and actual['address']==g[0]['address']
            assert actual['tid']==g[0]['tid']
        out.update(foreign_continue_status_hex=hex(expected_status),foreign_context_writes=len(writes),
                   handler_delta=delivery['after']-delivery['before'])
    return out


def check():
    summary,inputs,loaded={}, {}, {}
    for mode in ('positive','original','candidate'):
        p=E/mode
        data={k:read(p/name) for k,name in [('ready','target-ready.json'),('capture','capture.json'),
             ('result','result.json'),('api','api.json'),('exit','target-exit.json')]}
        if mode!='positive':data['delivery']=read(p/'delivery.json')
        plan=read(p/'plan.json')
        assert data['result']['sources']==plan['sources']
        assert data['ready']['source_sha256']==plan['sources']['run.py']
        for name,h in plan['sources'].items():
            assert sha(E/name if name=='run.py' else FIX/name)==h,name
        summary[mode]=reduce_arm(mode,data)
        loaded[mode]=data
        for f in p.iterdir():
            if f.is_file(): inputs[f.relative_to(E).as_posix()]=sha(f)
    # Deliberately malformed copies: a label or cleanup success cannot mask
    # missing positive observations, swallowed delivery or a context write.
    controls=[]
    for defect in ('zero_positive','wrong_reply','missing_handler','empty_api','unexpected_write'):
        mode='positive' if defect=='zero_positive' else 'candidate'
        data=copy.deepcopy(loaded[mode])
        if defect=='zero_positive':data['capture']['hits']=[]
        elif defect=='missing_handler':data['delivery']['after']=1
        elif defect=='empty_api':data['api']=[]
        else:
            start=next(i for i,r in enumerate(data['api']) if r['operation']=='WaitForDebugEvent'
                       and r.get('exception')==0x80000004 and r['address']!=data['ready']['address'])
            end=next(i for i in range(start,len(data['api'])) if data['api'][i]['operation']=='ContinueDebugEvent')
            if defect=='wrong_reply':data['api'][end]['status']=0x10002
            else:data['api'].insert(end,{'operation':'SetThreadContext','result':1})
        try:reduce_arm(mode,data)
        except (AssertionError,KeyError):controls.append(defect)
        else:raise AssertionError('undetected malformed receipt: '+defect)
    return dict(method='Offline reduction of native disposable-target receipts; no new execution',
                arms=summary,malformed_receipts_rejected=controls,input_sha256=inputs)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    result=check()
    if args.write:
        with (E/'normalized.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'arms':result['arms'],'malformed_receipts_rejected':result['malformed_receipts_rejected']},indent=2))
