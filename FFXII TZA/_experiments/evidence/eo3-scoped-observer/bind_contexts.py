"""Next EO3 adapter component: bind retained context reads to owned events.

Method A, existing receipts only. Native CloseHandle was not logged; this does
not assert an independent handle-lifetime census or qualify pending-event abort.
"""
import ast
import copy
import ctypes
import ctypes.wintypes as w
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from project import project

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
OLD=ROOT/'Database/FFXII TZA/_experiments/evidence/native-fp-context-control'
FIX=ROOT/'Database/FFXII TZA/_experiments/evidence/exp127-instrument-control'
namespace={'ctypes':ctypes,'w':w}
tree=ast.parse((FIX/'original/hwbp-source.py').read_text())
defs=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name in ('M128A','CONTEXT')]
assert len(defs)==2
exec(compile(ast.Module(body=defs,type_ignores=[]),'frozen CONTEXT declarations','exec'),namespace)
predicate={}
exec(compile((FIX/'ownership.py').read_text(),str(FIX/'ownership.py'),'exec'),predicate)
owned_step=predicate['owned_step'];Context=namespace['CONTEXT']


def bind(rows,pid,gate):
    groups=[];current=None;phase='capture'
    for index,row in enumerate(rows):
        op=row['operation']
        if op=='timeout_cleanup_begin':
            assert current is None,'cleanup begins with an unresolved event'
            phase='cleanup'
        if op=='WaitForDebugEvent' and row['result']:
            assert current is None,'new event before old continuation'
            current=dict(event=row,event_index=index,rows=[],phase=phase)
        elif op=='ContinueDebugEvent':
            assert current is not None,'continuation without event'
            event=current['event']
            assert (row['pid'],row['tid'])==(event['pid'],event['tid']) and row['result']==1
            current['continued']=row;groups.append(current);current=None
        elif current is not None:
            current['rows'].append((index,row))
    assert current is None,'unterminated event'
    results=[]
    for group in groups:
        event=group['event']
        if group['phase']!='capture' or event.get('exception')!=0x80000004:continue
        assert event['pid']==pid and event['address']==gate
        assert group['continued']['status']==0x10002
        chances=[r for _,r in group['rows'] if r['operation']=='exception_chance']
        assert len(chances)==1 and chances[0]['tid']==event['tid'] and chances[0]['address']==gate and chances[0]['first_chance']==1
        last_open=None;pending_get=None;contexts=[]
        for index,row in group['rows']:
            op=row['operation']
            if op=='OpenThread':
                assert row['result'] and row['tid']==event['tid'],'context thread differs from event thread'
                last_open=row
            elif op=='GetThreadContext':
                assert last_open and row['handle']==last_open['result'] and row['result']==1
                pending_get=row
            elif op=='full_context' and row['api']=='GetThreadContext':
                assert pending_get and row['handle']==pending_get['handle'] and row['requested_flags']==pending_get['requested_flags']
                values=project(row);ctx=Context.from_buffer_copy(bytes.fromhex(row['context_hex']))
                assert owned_step(ctx,event['address'],[gate]),'context not this owned execute breakpoint'
                assert values['rip']==gate
                contexts.append(dict(api_index=index,context_read=row,values=values))
                pending_get=None;last_open=None
        assert len(contexts)==2,'frozen read_regs and resume reread are not the expected pair'
        # The frozen capture's first read_regs supplies the observer; the second
        # is resume_past_breakpoint's distinct reread. Do not count it as a new hit.
        results.append(dict(event_index=group['event_index'],pid=pid,tid=event['tid'],
                            observer=contexts[0],resume_reread=contexts[1]))
    assert results,'no owned observer events'
    return results


def main():
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    manifest=json.loads((OLD/'manifest.json').read_text())
    names=['full-observer/api.json','full-observer/target-ready.json','full-observer/capture.json']
    for name in names:assert sha(OLD/name)==manifest[name]
    rows=json.loads((OLD/names[0]).read_text());ready=json.loads((OLD/names[1]).read_text())
    capture=json.loads((OLD/names[2]).read_text())
    linked=bind(rows,ready['pid'],ready['gate_address'])
    assert len(linked)==len(capture['hits'])==21
    assert [(r['tid'],r['observer']['values']['rip'],r['observer']['values']['rsp']) for r in linked]==[(r['tid'],r['rip'],r['rsp']) for r in capture['hits']]
    assert all(r['observer']['values']['rcx']==r['observer']['values']['rbx']==ready['buffer_address'] for r in linked)
    rejected=[]
    def reject(label,bad):
        try:bind(bad,ready['pid'],ready['gate_address'])
        except (AssertionError,KeyError):rejected.append(label)
        else:raise AssertionError('bad event binding accepted: '+label)
    start=linked[0]['event_index'];end=linked[0]['observer']['api_index']
    j=next(i for i in range(start,end) if rows[i]['operation']=='OpenThread')
    bad=copy.deepcopy(rows);bad[j]['tid']+=1;reject('different thread context',bad)
    bad=copy.deepcopy(rows);bad[end]['handle']+=1;reject('unmatched context handle',bad)
    bad=copy.deepcopy(rows);bad[end]['api']='SetThreadContext';reject('write proposal substituted for observer read',bad)
    bad=copy.deepcopy(rows);raw=bytearray.fromhex(bad[end]['context_hex']);raw[Context.Dr6.offset]^=1;bad[end]['context_hex']=raw.hex();reject('address-only context without owned DR6 cause',bad)
    bad=copy.deepcopy(rows);bad[start]['pid']+=1;reject('foreign process event',bad)
    bad=copy.deepcopy(rows);bad.pop(next(i for i in range(end,len(bad)) if bad[i]['operation']=='ContinueDebugEvent'));reject('event never continued',bad)
    reject('empty journal',[])
    out=dict(method='A - retained native event/API evidence',new_native_execution=False,live_game=False,
             source_sha256={n:sha(OLD/n) for n in names},
             helper_sha256={n:sha(FIX/n) for n in ['ownership.py','capture_candidate.py','original/hwbp-source.py']},
             events=linked,rejected=rejected,
             limits=['21 existing capture events;42 context reads include21 resume rereads, not new samples.',
                     'OpenThread/GetThreadContext ordering in the frozen single debugger loop supplies binding; CloseHandle was not logged.',
                     'No fresh native adapter, stopped memory reads, abort/cleanup or FF12 health qualification.'])
    if '--write' in __import__('sys').argv:
        with (W/'binding-control.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((W/'binding-control.json').read_text())==out
    print('Bound21 retained observer events to matching thread handles and separate21 resume reads;',len(rejected),'binding controls reject.')


if __name__=='__main__':main()
