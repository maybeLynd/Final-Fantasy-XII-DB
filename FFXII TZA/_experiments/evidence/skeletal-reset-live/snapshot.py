"""Scoped EXP079/124 query/read identity and base snapshots; no process writes."""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
KIT = REPO / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(KIT))
import runtime_probe as rp
import ffxii_runtime as rt
import team

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pid', type=int, required=True)
    ap.add_argument('--label', required=True)
    a = ap.parse_args()
    assert a.label.replace('-', '').isalnum()
    out = HERE / (a.label + '.json')
    result = dict(status='INVALID', pid=a.pid, start_unix=time.time(), reads=[],
                  method='C: query/read only, sequential identity and base brackets')
    handle = None
    with out.open('x', encoding='utf-8') as output:
        try:
            b = json.loads(team.BOARD.read_text())
            holders = [t for t in b['tasks'] if t['status']=='ACTIVE' and
                       any(r['key']=='@runtime' for r in t['resources'])]
            assert len(holders)==1 and holders[0]['agent']=='ASTRA'
            result['runtime_claim'] = holders[0]['id']
            owner = json.loads((HERE/'process.json').read_text())
            assert owner['pid']==a.pid and rt.list_processes()==[owner]
            result['process'] = owner
            raw = Path(owner['path']).read_bytes()
            assert sha(raw)==rt.AUTHORITY_SHA256
            result['exe_sha256'] = sha(raw)
            result['sources'] = {str(p.relative_to(REPO)):sha(p.read_bytes()) for p in
                                 [Path(__file__), KIT/'runtime_probe.py', KIT/'ffxii_runtime.py']}
            expected = json.loads((HERE/'preflight.json').read_text())['sources']
            assert all(expected[k]==v for k,v in result['sources'].items())
            verdict, watched, modules = rt.classify(a.pid)
            result.update(module_verdict=verdict, watched_modules=watched, modules_before=modules)
            assert verdict=='clean' and modules
            rp.k32.OpenProcess.restype = ctypes.c_void_p
            rp.k32.CloseHandle.argtypes = [ctypes.c_void_p]
            rp.k32.ReadProcessMemory.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,
                                               ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
            rp.psapi.EnumProcessModules.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulong,
                                                  ctypes.POINTER(ctypes.c_ulong)]
            handle = rp.k32.OpenProcess(rp.PROCESS_QUERY_INFORMATION|rp.PROCESS_VM_READ,False,a.pid)
            assert handle
            reader = rp.Probe(handle)
            result['image_base'] = rp.module_base(handle)
            assert result['image_base']==rp.IMAGE_BASE
            def read(address, size, purpose):
                start = time.time()
                data = reader.read(address,size)
                result['reads'].append(dict(address=address,size=size,purpose=purpose,
                    start_unix=start,end_unix=time.time(),hex=None if data is None else data.hex()))
                assert data is not None and len(data)==size
                return data
            assert read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES),'known positive')==rp.CONTROL_BYTES
            result['null_read_rejected'] = reader.read(0,16) is None
            assert result['null_read_rejected']
            rp.k32.CheckRemoteDebuggerPresent.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
            debug = ctypes.c_int()
            assert rp.k32.CheckRemoteDebuggerPresent(handle,ctypes.byref(debug))
            result['debugger_present'] = bool(debug.value)
            assert not debug.value
            pe = struct.unpack_from('<I',raw,0x3c)[0]
            table = pe+24+struct.unpack_from('<H',raw,pe+20)[0]
            sections = []
            for n in range(struct.unpack_from('<H',raw,pe+6)[0]):
                off = table+40*n
                if raw[off:off+8].rstrip(b'\0')==b'.text':
                    vs,rva,size,disk = struct.unpack_from('<IIII',raw,off+8)
                    sections.append((rp.IMAGE_BASE+rva,raw[disk:disk+min(vs,size)]))
            assert len(sections)==1
            address, data = sections[0]
            result['text'] = []
            for phase in ('before','after'):
                current = reader.read(address,len(data))
                result['text'].append(dict(phase=phase,address=address,bytes=len(data),
                    disk_sha256=sha(data),live_sha256=None if current is None else sha(current)))
                assert current==data
                read(0x01F83530,8,'decoder-base-'+phase)
            verdict, watched, modules_after = rt.classify(a.pid)
            result['modules_after'] = modules_after
            assert verdict=='clean' and modules_after==modules
            assert read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES),'known positive after')==rp.CONTROL_BYTES
            result['status'] = 'OBSERVED'
        except BaseException as error:
            result['error'] = repr(error)
        finally:
            if handle:
                result['read_handle_closed'] = bool(rp.k32.CloseHandle(handle))
                if not result['read_handle_closed']:
                    result['status'] = 'INVALID'
            result['end_unix'] = time.time()
            json.dump(result,output,indent=2)
            output.write('\n')
    print(result['status'],result.get('error',''),out)
    return 0 if result['status']=='OBSERVED' else 1

if __name__=='__main__':
    raise SystemExit(main())
