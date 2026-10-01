"""One prepared EO3 capture using the existing recorder, reader and abort.

Importing this module performs no native calls. The CLI requires --execute,
an existing prepared directory and ASTRA's live @runtime claim. It does not
launch FF12, send input, set up saves, certify health, or restore user files.
"""
import argparse
import ast
import ctypes as C
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
EVIDENCE=ROOT/'Database/FFXII TZA/_experiments/evidence'
FIX=EVIDENCE/'exp127-instrument-control'
KIT=ROOT/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0,str(FIX))
from capture_scoped_v2 import capture
from eo3_callback import EO3Callback
from observe import Recorder
from match import PRODUCER,BUILDER,ISSUER
from owned_game_abort import make_abort,validate_expected,EXE_SHA,SOURCE_SHA

SITES=[PRODUCER,BUILDER,ISSUER]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sources():
    names=['run_eo3.py','capture_scoped_v2.py','eo3_callback.py','observe.py',
           'match.py','project.py','owned_game_abort.py','native_stop_control.py']
    paths=[*(HERE/n for n in names),FIX/'ownership.py',FIX/'cleanup_candidate.py',
           FIX/'original/capture.py',FIX/'original/hwbp-source.py',FIX/'original/api_receipts.py',
           KIT/'runtime_probe.py',KIT/'ffxii_runtime.py',
           EVIDENCE/'eo3-pointer-observation-preflight/observation.json']
    return {p.relative_to(ROOT).as_posix():sha(p) for p in paths}


class GuardedAPI:
    """Validate the capture's opened handle before DebugActiveProcess.

    A stop flag is sampled between debug events. Once latched, the capture
    unwinds into its existing cleanup; the same flag does not block cleanup.
    No input automation occurs here. This is cooperative, not an atomic stop.
    """
    def __init__(self,audit,expected,identity,qualify,begin,stop,ready,clock):
        self.audit=audit;self.expected=expected;self.identity=identity
        self.qualify=qualify;self.begin=begin;self.stop=stop
        self.handle=None;self.stop_latched=False;self.cleanup_started=False
        self.arming=[];self.ready=ready;self.clock=clock
        self.ready_receipt=None;self.readiness_error=None
    def __getattr__(self,name):return getattr(self.audit,name)
    def OpenProcess(self,access,inherit,pid):
        assert pid==self.expected['pid'],'different process requested'
        self.handle=self.audit.OpenProcess(access,inherit,pid)
        self.audit.mark('eo3_capture_handle',pid=pid,access=access,handle=self.handle)
        return self.handle
    def DebugActiveProcess(self,pid):
        assert pid==self.expected['pid'] and self.handle
        assert not self.stop(),'stop requested before attachment'
        observed=self.identity(self,self.handle)
        self.audit.mark('eo3_pre_attach_identity',observed=observed)
        assert observed==self.expected,'opened process lifetime/image differs'
        qualification=self.qualify(self.handle)
        self.audit.mark('eo3_pre_attach_qualification',qualification=qualification)
        assert qualification['status']=='REFERENCE_CONTROLS_PASS'
        assert not self.stop(),'stop requested during qualification'
        self.begin()  # after qualification; no manual setup time enters Recorder
        return self.audit.DebugActiveProcess(pid)
    def ContinueDebugEvent(self,pid,tid,status):
        event=dict(self.audit.event) if self.audit.event else None
        result=self.audit.ContinueDebugEvent(pid,tid,status)
        if (result and self.ready_receipt is None and event and event['code']==1
                and event.get('exception')==0x80000003 and event.get('first_chance')==1
                and self.arming and all(ok for thread,ok in self.arming)):
            self.ready_receipt=dict(pid=pid,tid=tid,sites=SITES,arming=list(self.arming),
                                    monotonic=self.clock.monotonic(),basis='Initial stopped arming succeeded and its event was continued.')
            self.audit.mark('eo3_armed_after_continue',**self.ready_receipt)
            try:self.ready(dict(self.ready_receipt))
            except Exception as failure:
                self.readiness_error=type(failure).__name__+': '+str(failure)
                self.audit.mark('eo3_readiness_delivery_failed',error=self.readiness_error)
                # Return the actual successful Continue result. The caller must
                # set pending=False before a later exception unwinds to cleanup.
        return result
    def WaitForDebugEvent(self,event,timeout):
        self.cleanup_started=self.cleanup_started or any(
            row.get('operation')=='timeout_cleanup_begin' for row in self.audit.rows)
        if not self.cleanup_started and not self.stop_latched and (self.readiness_error or self.stop()):
            self.stop_latched=True
            self.audit.mark('eo3_stop_requested_between_events',readiness_error=self.readiness_error)
            raise RuntimeError('stop/readiness failure; end capture and perform cleanup only')
        return self.audit.WaitForDebugEvent(event,timeout)


def run(m,expected,audit,probe_factory,identity,qualify,*,clock=time,stop=lambda:False,ready=lambda receipt:None):
    """Execute one connected capture; never issue a final live semantic PASS."""
    expected=validate_expected(expected)
    assert not stop(),'stop was already requested; no automatic restart'
    original_api=m.k32;original_slots=m.set_slots;state={}
    def begin():
        state['started']=clock.monotonic();state['recorder']=Recorder(state['started'])
        state['callback']=EO3Callback(state['recorder'],probe_factory,clock=clock.monotonic)
        audit.mark('eo3_recorder_started',monotonic=state['started'],
                   basis='Before attachment, after qualification; conservatively includes attach latency.')
    guarded=GuardedAPI(audit,expected,identity,qualify,begin,stop,ready,clock)
    def set_slots(tid,slots):
        assert not slots or list(slots)==SITES
        ok=original_slots(tid,slots)
        if slots:guarded.arming.append((tid,bool(ok)))
        return ok
    def observe(*args):return state['callback'](*args)
    abort=make_abort(expected,identity_reader=identity,clock=clock)
    result=dict(status='INVALID',method='Connected EO3 recorder; execution substrate and live health require enclosing evidence.',
                capture=None,recorder=None,normalized=None,reference_identity=expected,
                input_sent=False,health_observed=False,restoration_verified=False)
    try:
        m.k32=guarded;m.set_slots=set_slots
        result['capture']=capture(m,expected['pid'],SITES,10,audit,observe,abort)
        if 'recorder' in state:
            r=state['recorder']
            result['recorder']=dict(started=r.started,decision=r.decision,reason=r.reason,
                                    events=r.events,reads=r.reads,semantic_payload_bytes=r.bytes)
        if guarded.readiness_error:
            result['status']='INVALID'
        elif result['capture']['status']=='MATCHED_PENDING_HEALTH':
            result['normalized']=state['recorder'].finish()
            result['status']='OBSERVATION_PENDING_SESSION_HEALTH'
        else:result['status']=result['capture']['status']
    finally:
        m.k32=original_api;m.set_slots=original_slots
        result['stop_latched']=guarded.stop_latched
        result['armed']=guarded.ready_receipt
        result['readiness_error']=guarded.readiness_error
    return result


def definitions(path,names,namespace):
    tree=ast.parse(path.read_text())
    nodes=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
    assert {n.name for n in nodes}==set(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace)


def frozen_loader():
    """Import frozen Python declarations only; load_source is not called here."""
    sys.path.insert(0,str(FIX/'original'))
    spec=importlib.util.spec_from_file_location('eo3_frozen_loader',FIX/'original/capture.py')
    original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
    assert Path(sys.modules[original.Audit.__module__].__file__).resolve()==(FIX/'original/api_receipts.py').resolve()
    return original


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--prepared',type=Path,required=True)
    args=parser.parse_args()
    if not args.execute:parser.error('No action taken: this runner requires explicit --execute')
    folder=args.prepared.resolve();plan=json.loads((folder/'plan.json').read_text())
    assert plan['sources']==sources(),'prepared tool/source identity changed'
    expected=validate_expected(plan['identity'])
    sys.path.insert(0,str(KIT));import team
    board=json.loads(team.BOARD.read_text())
    assert any(t['id']==plan['runtime_task'] and t['agent']=='ASTRA' and t['status']=='ACTIVE'
               and any(r['key']=='@runtime' for r in t.get('claimed_resources',t['resources']))
               for t in board['tasks']),'active ASTRA runtime claim required'
    # These are source pins to separately reviewed preparation, not substitutes
    # for reading that evidence. A setup receipt must identify this same lifetime.
    assert plan['setup_identity']==expected
    assert plan['setup_receipts'] and all(sha(folder/n)==h for n,h in plan['setup_receipts'].items())
    assert not (folder/'STOP').exists(),'explicit stop persists; no automatic restart'
    assert not (folder/'capture.json').exists() and not (folder/'api.json').exists()
    import runtime_probe as rp
    import ffxii_runtime as rt
    original=frozen_loader();Audit=original.Audit
    m=original.load_source()
    source=HERE/'native_stop_control.py';assert sha(source)==SOURCE_SHA
    ns=dict(C=C,Audit=Audit,sha=sha)
    definitions(source,['configure','identity','ScopedAudit'],ns)
    ns['configure'](m.k32)
    m.k32.CheckRemoteDebuggerPresent.argtypes=[C.c_void_p,C.POINTER(C.c_int)]
    m.k32.CheckRemoteDebuggerPresent.restype=C.c_int
    audit=ns['ScopedAudit'](m.k32,folder/'api.json')
    # Same reader class as the native controls, with an explicit API binding.
    read_ns=dict(ctypes=C,k32=audit);definitions(KIT/'runtime_probe.py',['Probe'],read_ns)
    plain_ns=dict(ctypes=C,k32=m.k32);definitions(KIT/'runtime_probe.py',['Probe'],plain_ns)
    rp.psapi.EnumProcessModules.argtypes=[C.c_void_p,C.c_void_p,C.c_ulong,C.POINTER(C.c_ulong)]
    raw=Path(expected['image']).read_bytes();assert hashlib.sha256(raw).hexdigest()==EXE_SHA
    qualification={}
    def qualify(handle):
        q=qualification;q.update(status='INVALID',code=[],started_unix=time.time())
        verdict,hits,modules=rt.classify(expected['pid'])
        q.update(module_verdict=verdict,watched_modules=hits,modules=modules)
        assert verdict=='clean' and modules
        q['module_file_sha256']={p:sha(p) for p in modules}
        q['image_base']=rp.module_base(handle);assert q['image_base']==rp.IMAGE_BASE==0x120000
        present=C.c_int()
        q['debugger_query_succeeded']=bool(m.k32.CheckRemoteDebuggerPresent(handle,C.byref(present)))
        q['debugger_present']=bool(present.value)
        assert q['debugger_query_succeeded'] and not q['debugger_present']
        reader=plain_ns['Probe'](handle)
        control=reader.read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES))
        q['read_control']=control.hex() if control is not None else None
        assert control==rp.CONTROL_BYTES
        q['null_read_rejected']=reader.read(0,16) is None;assert q['null_read_rejected']
        pe=struct.unpack_from('<I',raw,0x3c)[0];table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
        for i in range(struct.unpack_from('<H',raw,pe+6)[0]):
            off=table+i*40
            if raw[off:off+8].rstrip(b'\0')!=b'.text':continue
            vs,rva,size,ro=struct.unpack_from('<IIII',raw,off+8);wanted=raw[ro:ro+min(vs,size)]
            observed=reader.read(rp.IMAGE_BASE+rva,len(wanted));assert observed is not None
            q['code'].append(dict(address=rp.IMAGE_BASE+rva,size=len(wanted),
                                  expected_sha256=hashlib.sha256(wanted).hexdigest(),
                                  observed_sha256=hashlib.sha256(observed).hexdigest(),matches=observed==wanted))
        assert len(q['code'])==1 and q['code'][0]['matches']
        prior=json.loads((EVIDENCE/'eo3-pointer-observation-preflight/observation.json').read_text())
        q['selected_bodies']=[]
        for body in prior['bodies']:
            observed=reader.read(int(body['address'],16),body['bytes'])
            q['selected_bodies'].append(dict(address=body['address'],raw=observed.hex() if observed is not None else None,
                                            expected_sha256=body['sha256']))
            assert observed is not None and observed.hex()==body['raw']
        q.update(status='REFERENCE_CONTROLS_PASS',ended_unix=time.time(),
                 limits='Sequential pre-attach reads, not an atomic process snapshot or proof of all module state.')
        return q
    def ready(receipt):
        with (folder/'armed.json').open('x') as out:json.dump(receipt,out,indent=2);out.write('\n')
    result=dict(status='INVALID',qualification=qualification,sources=plan['sources'])
    try:
        result['run']=run(m,expected,audit,read_ns['Probe'],ns['identity'],qualify,
                          stop=lambda:(folder/'STOP').exists(),ready=ready)
        result['status']=result['run']['status']
    except Exception as failure:result['error']=type(failure).__name__+': '+str(failure)
    finally:
        result['sources_unchanged']=plan['sources']==sources()
        if not result['sources_unchanged']:result['status']='INVALID'
        audit.save();(folder/'capture.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],'— separate live health/restoration acceptance still required.')


if __name__=='__main__':main()
