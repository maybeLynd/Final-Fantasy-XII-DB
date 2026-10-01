"""EO3-only native reader feasibility. Supplied data, no FF12/code execution.

Question: does the existing Probe preserve a >4GiB address and reject partial
reads? Controls: known path ends at a readable page boundary, adjacent PAGE_NOACCESS,
then a second positive. Parent reads only its directly launched bounded child.
"""
import ast
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
SOURCE=ROOT/'Database/Tools/analysis-kit/gfz-scripts/runtime_probe.py'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2);f.write('\n')


def dll():
    k=C.WinDLL('kernel32',use_last_error=True)
    for name,args,ret in [
        ('VirtualAlloc',[C.c_void_p,C.c_size_t,C.c_uint32,C.c_uint32],C.c_void_p),
        ('VirtualProtect',[C.c_void_p,C.c_size_t,C.c_uint32,C.POINTER(C.c_uint32)],C.c_int),
        ('VirtualFree',[C.c_void_p,C.c_size_t,C.c_uint32],C.c_int),
        ('OpenProcess',[C.c_uint32,C.c_int,C.c_uint32],C.c_void_p),
        ('CloseHandle',[C.c_void_p],C.c_int),
        ('ReadProcessMemory',[C.c_void_p,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)],C.c_int),
        ('QueryFullProcessImageNameW',[C.c_void_p,C.c_uint32,C.c_wchar_p,C.POINTER(C.c_uint32)],C.c_int),
        ('GetModuleFileNameW',[C.c_void_p,C.c_wchar_p,C.c_uint32],C.c_uint32),
        ('IsDebuggerPresent',[],C.c_int)]:
        f=getattr(k,name);f.argtypes=args;f.restype=ret
    return k


def module(k,handle):
    text=C.create_unicode_buffer(32768);n=k.GetModuleFileNameW(handle,text,len(text))
    assert 0<n<len(text)
    return dict(path=text.value,sha256=sha(text.value))


def child(folder):
    k=dll();address=None;normal=False
    try:
        address=k.VirtualAlloc(None,8192,0x3000,4);assert address and address>0xffffffff,'no above4GiB feasibility allocation'
        path=b'PS2Data\\efb\\synthetic_reader.efb\0'
        start=address+4096-len(path)
        C.memset(address,0xa5,8192);C.memmove(start,path,len(path))
        old=C.c_uint32();assert k.VirtualProtect(address+4096,4096,1,C.byref(old))
        write(folder/'ready.json',dict(pid=os.getpid(),parent_pid=os.getppid(),source_sha256=sha(__file__),
              python=module(k,None),kernel32=module(k,k._handle),allocation=address,allocation_bytes=8192,
              path_address=start,path_hex=path.hex(),page_boundary=address+4096,second_page_protection=1,
              method='native synthetic instrument control; no original FF12 instructions'))
        deadline=time.monotonic()+15
        while not (folder/'stop.flag').exists():
            assert time.monotonic()<deadline,'owned child deadline'
            time.sleep(.02)
        normal=True
    finally:
        freed=bool(k.VirtualFree(address,0,0x8000)) if address else None
        write(folder/'exit.json',dict(pid=os.getpid(),normal=normal,allocation_freed=freed,
                                     debugger_present=bool(k.IsDebuggerPresent())))


def parent(folder):
    folder.mkdir();k=dll();handle=None;calls=[];outcomes=[];closed=None;ready=None
    frozen=SOURCE.read_bytes();(folder/'reader-source.py').write_bytes(frozen)
    write(folder/'plan.json',dict(question='Does the existing native Probe preserve full address width and reject inaccessible/partial reads?',
          hypotheses=['full pointer and exact requested bytes preserved','address truncated or failed/partial read becomes data'],
          method='native instrument control with supplied child data; not method B shipping-code execution or live FF12',
          reader_sha256=hashlib.sha256(frozen).hexdigest(),runner_sha256=sha(__file__),
          controls='Known NUL-terminated path at readable page end; adjacent NOACCESS; positive repeated after failures',
          stop='one bounded directly owned child,15s maximum; stop flag, normal exit and allocation/handle cleanup receipts'))
    base=Path(sys._base_executable).resolve()
    with (folder/'child.log').open('x') as log:
        process=subprocess.Popen([str(base),str(Path(__file__).resolve()),'--child',str(folder.resolve())],stdout=log,stderr=subprocess.STDOUT)
        try:
            deadline=time.monotonic()+8
            while not (folder/'ready.json').exists():
                assert process.poll() is None,'child exited before ready'
                assert time.monotonic()<deadline,'ready deadline'
                time.sleep(.02)
            ready=json.loads((folder/'ready.json').read_text())
            assert ready['pid']==process.pid and ready['parent_pid']==os.getpid()
            assert ready['source_sha256']==sha(__file__) and Path(ready['python']['path']).resolve()==base
            assert ready['python']['sha256']==sha(base)
            handle=k.OpenProcess(0x410,False,process.pid);assert handle,'owned read/query handle unavailable'
            text=C.create_unicode_buffer(32768);size=C.c_uint32(len(text))
            assert k.QueryFullProcessImageNameW(handle,0,text,C.byref(size)) and Path(text.value).resolve()==base
            write(folder/'ownership.json',dict(parent_pid=os.getpid(),popen_pid=process.pid,child_pid=ready['pid'],
                  child_parent_pid=ready['parent_pid'],opened_image=text.value,python_sha256=sha(base),access=0x410))
            class Audit:
                def ReadProcessMemory(self,h,address,buf,size,got):
                    C.set_last_error(0)
                    ok=k.ReadProcessMemory(h,address,buf,size,got);error=C.get_last_error()
                    n=got._obj.value
                    calls.append(dict(handle=h,address=address.value,requested=size.value,result=int(ok),
                                      transferred=n,error=error,raw_hex=C.string_at(buf,n).hex()))
                    C.set_last_error(error);return ok
            defs=[n for n in ast.parse(frozen).body if isinstance(n,ast.ClassDef) and n.name=='Probe']
            assert len(defs)==1
            ns={'ctypes':C,'k32':Audit()};exec(compile(ast.Module(body=defs,type_ignores=[]),'frozen Probe class','exec'),ns)
            probe=ns['Probe'](handle);path=bytes.fromhex(ready['path_hex']);address=ready['path_address'];boundary=ready['page_boundary']
            assert address+len(path)==boundary and address>0xffffffff
            value=probe.read(address,len(path));assert value==path
            outcomes.append(dict(case='full-width exact positive',bytes_hex=value.hex()))
            value=probe.read(boundary-1,1);assert value==b'\0';outcomes.append(dict(case='last readable byte',bytes_hex=value.hex()))
            value=probe.read(boundary-1,2);assert value is None;outcomes.append(dict(case='cross-page read rejected',returned=None))
            value=probe.read(boundary,1);assert value is None;outcomes.append(dict(case='NOACCESS read rejected',returned=None))
            captured=bytearray()
            for offset in range(128):
                value=probe.read(address+offset,1);assert value is not None
                captured+=value
                if value==b'\0':break
            assert bytes(captured)==path;outcomes.append(dict(case='bounded byte path avoids reading past NUL',bytes_hex=bytes(captured).hex()))
            value=probe.read(address,len(path));assert value==path
            outcomes.append(dict(case='positive after failed reads',bytes_hex=value.hex()))
        finally:
            if handle:closed=bool(k.CloseHandle(handle))
            (folder/'stop.flag').write_text('end owned reader feasibility\n')
            try:exit_code=process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                # Only the directly launched child, never a name/PID rediscovery.
                process.kill();exit_code=process.wait(timeout=5)
                write(folder/'forced-stop.json',dict(popen_pid=process.pid,exit_code=exit_code))
            write(folder/'calls.json',calls)
            write(folder/'parent-cleanup.json',dict(child_exit=exit_code,read_handle_closed=closed,forced_stop=(folder/'forced-stop.json').exists()))
    ended=json.loads((folder/'exit.json').read_text())
    assert outcomes and ready and exit_code==0 and closed and ended['pid']==process.pid and ended['normal'] and ended['allocation_freed'] and not ended['debugger_present']
    assert not (folder/'forced-stop.json').exists()
    write(folder/'result.json',dict(status='NATIVE_READER_CONTROL_ONLY',fresh_live_game=False,original_code_executed=False,
          outcomes=outcomes,limitations=['Supplied stable child memory, not FF12 initialization or memory lifetime.',
              'No debug-event stopped read/abort qualification or game health conclusion.',
              'Actual partial transfer count is retained; failure rejection does not require a particular count.']))
    print('Native reader control: full64-bit path and bounded reads agree; failed/cross-page reads rejected; owned child freed/exited and handle closed.')


if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--child':child(Path(sys.argv[2]))
    elif len(sys.argv)==2:parent(Path(sys.argv[1]))
    else:raise SystemExit('usage: native_read_control.py new-output-folder')
