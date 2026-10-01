"""Synthetic ownership/abort connection; no game process or native API calls."""
import copy
import ctypes as C
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace
from owned_game_abort import make_abort,validate_expected,EXE,EXE_SHA,SOURCE_SHA,ABORT_AST_SHA

W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


class Event(C.Structure):
    _fields_=[('dwProcessId',C.c_uint32),('dwThreadId',C.c_uint32),('dwDebugEventCode',C.c_uint32)]


class Fixture:
    DBG_CONTINUE=0x10002;DEBUG_EVENT=Event
    def __init__(self,identity,terminate=True,exit_code=0xea03):
        self.k32=self;self.identity=dict(identity);self.calls=[];self.now=0
        self.terminate=terminate;self.exit_code=exit_code
        self.event=dict(pid=identity['pid'],tid=77)
        self.events=[(4,88),(5,77)]
    def monotonic(self):self.now+=.01;return self.now
    def identity_read(self,k,handle):
        assert handle==91;self.calls.append(['identity',handle]);return dict(self.identity)
    def TerminateProcess(self,handle,code):
        self.calls.append(['terminate',handle,code]);return int(self.terminate)
    def ContinueDebugEvent(self,pid,tid,status):
        self.calls.append(['continue',pid,tid,status]);return 1
    def WaitForDebugEvent(self,ptr,timeout):
        code,tid=self.events.pop(0);ev=ptr._obj
        ev.dwProcessId=self.identity['pid'];ev.dwThreadId=tid;ev.dwDebugEventCode=code
        self.calls.append(['wait_event',code,tid]);return 1
    def WaitForSingleObject(self,handle,timeout):
        self.calls.append(['wait_terminal',handle,timeout]);return 0
    def GetExitCodeProcess(self,handle,ptr):
        self.calls.append(['exit_code',handle]);ptr._obj.value=self.exit_code;return 1
    def mark(self,name,**values):self.calls.append([name,values])


def main():
    # The two retained raw receipts demonstrate why a PID alone is inadequate.
    # They are native Python subjects, NOT observed FF12 identities.
    reader=json.loads((W/'native-reader-1/owned-child.json').read_text())
    later=json.loads((W/'native-instruction-read-failure-1/owned-child.json').read_text())
    old_identity=reader['identity'];new_identity=later['identity']
    assert old_identity['pid']==new_identity['pid']==38728
    assert old_identity['creation']!=new_identity['creation']
    expected=dict(new_identity,image=EXE,image_sha256=EXE_SHA)
    label='Supplied FF12 identity shape using retained native PID/time values; not an observed FF12 process.'
    baseline=Fixture(expected)
    result=make_abort(expected,identity_reader=baseline.identity_read,clock=baseline)(baseline,expected['pid'],91,77,baseline)
    assert result['terminal'] and result['exit_code']==0xea03
    ops=[x[0] for x in baseline.calls]
    assert ops[:3]==['identity','terminate','continue']
    assert ops.count('terminate')==1 and ops.count('continue')==3
    controls={}
    for key,value in [('creation',old_identity['creation']),('pid',expected['pid']+1),
                      ('image',r'D:\unrelated\FFXII_TZA.exe'),('image_sha256','0'*64)]:
        actual=dict(expected);actual[key]=value;fixture=Fixture(actual)
        fixture.event=dict(pid=expected['pid'],tid=77)
        try:make_abort(expected,identity_reader=fixture.identity_read,clock=fixture)(fixture,expected['pid'],91,77,fixture)
        except AssertionError:pass
        else:raise AssertionError('mismatched lifetime permitted: '+key)
        assert fixture.calls==[['identity',91]],key
        controls['observed_'+key]=fixture.calls
    for key,value in [('pid',expected['pid']+1),('tid',78)]:
        f=Fixture(expected);f.event[key]=value
        try:make_abort(expected,identity_reader=f.identity_read,clock=f)(f,expected['pid'],91,77,f)
        except AssertionError:pass
        else:raise AssertionError('foreign pending event permitted')
        assert f.calls==[['identity',91]];controls['event_'+key]=f.calls
    rejected=[]
    for key,value in [('creation',0),('pid',True),('image',r'D:\mod-client\FFXII_TZA.exe'),('image_sha256','0'*64)]:
        bad=dict(expected);bad[key]=value
        try:validate_expected(bad)
        except AssertionError:rejected.append(key)
        else:raise AssertionError('invalid prepared identity: '+key)
    f=Fixture(expected,terminate=False)
    try:make_abort(expected,identity_reader=f.identity_read,clock=f)(f,expected['pid'],91,77,f)
    except AssertionError:pass
    else:raise AssertionError('failed terminate permitted continuation')
    assert [x[0] for x in f.calls]==['identity','terminate'];controls['terminate_failure']=f.calls
    f=Fixture(expected,exit_code=0)
    r=make_abort(expected,identity_reader=f.identity_read,clock=f)(f,expected['pid'],91,77,f)
    assert not r['terminal'];controls['unexpected_exit_code']=dict(result=r,calls=f.calls)
    out=dict(method='Synthetic adapter control only; native_calls=0; no original/game execution',
             supplied_identity_label=label,source_sha256=SOURCE_SHA,abort_ast_sha256=ABORT_AST_SHA,
             retained_pid_reuse=dict(earlier=old_identity,later=new_identity),
             positive=dict(result=result,calls=baseline.calls),rejected_expected=rejected,controls=controls,
             tool_sha256={p.name:sha(p) for p in (W/'owned_game_abort.py',Path(__file__))},
             limits=['Exact abort body reused from native controls, not a fresh native game abort.',
                     'Expected lifetime must originate in a fresh authorized setup; shape validation cannot prove that.',
                     'Runner must still bind its attach, reference code/module state, backup and health checks.',
                     'No semantic healthy-game result from intentional termination.'])
    if '--write' in sys.argv:
        with (W/'owned-game-abort-observation.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((W/'owned-game-abort-observation.json').read_text())==out
    print('Exact retained abort connected to supplied game identity; reused PID/foreign event/image and failed termination reject. Synthetic only.')


if __name__=='__main__':main()
