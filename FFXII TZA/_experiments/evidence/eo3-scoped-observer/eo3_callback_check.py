"""Synthetic connector decisions using the original-context type declarations."""
import copy
import ctypes
import json
from pathlib import Path
import sys
from types import SimpleNamespace

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
sys.path.insert(0,str(ROOT/'Database/FFXII TZA/_experiments/evidence/exp127-instrument-control'))
from native_stop_check import Context
from eo3_callback import EO3Callback
from observe import Recorder
from observe_control import context,memory
from control import fixture
from match import PRODUCER,BUILDER,ISSUER


def sequence(mutate=None,pointer=0x6abcd000):
    f=fixture(pointer);blobs,read=memory(f);recorder=Recorder(100);audit=SimpleNamespace(event=None,last_get=None)
    handles=[]
    class Probe:
        def __init__(self,handle):handles.append(handle);assert handle==11
        def read(self,address,n):return read(address,n)
    callback=EO3Callback(recorder,Probe,clock=lambda:100)
    outputs=[]
    for index,values in enumerate((f[0],f[3],f[6])):
        if recorder.decision!='CONTINUE':break
        if index==2:blobs[-1]=(f[6]['rbx'],bytes(f[7]))
        ctx=Context.from_buffer_copy(bytes.fromhex(context(values)['context_hex']))
        ctx.ContextFlags=0x10001b;ctx.EFlags=0x202
        ctx.Dr0=PRODUCER;ctx.Dr1=BUILDER;ctx.Dr2=ISSUER;ctx.Dr3=0;ctx.Dr7=0x415;ctx.Dr6=0xffff0ff0|(1<<index)
        event=dict(id=index+1,pid=99,tid=values['tid'],code=1,exception=0x80000004,first_chance=1,address=ctx.Rip)
        row=dict(operation='full_context',api='GetThreadContext',result=1,requested_flags=0x10001b,
                 event=dict(event),thread_binding=dict(tid=values['tid']),address=ctypes.addressof(ctx),
                 context_hex=bytes(ctx).hex(),size=ctypes.sizeof(ctx),api_index=index,
                 source='synthetic caller/context fixture; not a native API receipt')
        audit.event=event;audit.last_get=row
        if mutate and index==0:mutate(audit,ctx)
        outputs.append(callback(None,99,11,values['tid'],ctx,audit))
    return recorder,outputs,handles


def main():
    r,outputs,handles=sequence();assert r.finish()['results'][0]['pointer_preserved']
    assert [x['decision'] for x in outputs]==['CONTINUE','CONTINUE','STOP_MATCHED_PENDING_HEALTH'] and handles==[11,11,11]
    r,high,_=sequence(pointer=0x18bc13000);assert len(high)==1 and high[0]['decision']=='HOLD_FOR_OWNED_ABORT' and not r.match.results
    rejected=[]
    def reject(label,fn):
        try:sequence(fn)
        except (AssertionError,KeyError):rejected.append(label)
        else:raise AssertionError('invalid connector accepted: '+label)
    reject('wrong event thread',lambda a,c:a.event.update(tid=998))
    reject('stale context from previous event',lambda a,c:a.last_get['event'].update(id=0))
    reject('different thread handle binding',lambda a,c:a.last_get['thread_binding'].update(tid=998))
    reject('modified context buffer',lambda a,c:setattr(c,'Rdi',c.Rdi+1))
    reject('write proposal instead of observed context',lambda a,c:a.last_get.update(api='SetThreadContext'))
    reject('second-chance event',lambda a,c:(a.event.update(first_chance=0),a.last_get['event'].update(first_chance=0)))
    out=dict(method='Synthetic EO3 connector control, no native calls',decisions=[x['decision'] for x in outputs],
             selected_original_pointer=r.events[0]['context']['rdi'],high_pointer_decision=high[0]['decision'],rejected=rejected,
             limits=['Not live FF12 or native execution of the semantic three-site recorder.',
                     'The separate native stopped-event/read/abort controls support the connector shape; reference/game health still required.'])
    if '--write' in sys.argv:
        with (W/'eo3-callback-control.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((W/'eo3-callback-control.json').read_text())==out
    print('EO3 connector joins the three synthetic sites, holds changed-pointer producer, and rejects stale/foreign/proposed contexts.')


if __name__=='__main__':main()
