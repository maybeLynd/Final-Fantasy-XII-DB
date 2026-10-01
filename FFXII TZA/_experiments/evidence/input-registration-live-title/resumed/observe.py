"""Bounded keyboard-registration sampling; no input sender, process writes or debugger."""
import ctypes, hashlib, json, struct, sys, time
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root.parents[5]
kit=repo/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0,str(kit))
import runtime_probe as rp
import ffxii_runtime as rt
import team
label=sys.argv[1]
assert label in ('noinput','positive','pause')
out=root/(label+'-memory.json')
assert not out.exists(), 'Preserve the previous observation'
owner=json.loads((root/'process.json').read_text())
pid=owner['pid']
record=dict(start_unix=time.time(),pid=pid,label=label,status='INVALID',samples=[],
            method='ReadProcessMemory only; no debug attach, writes, injected calls or suspended threads.',
            tool_hashes={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in [Path(__file__),root/'input_sample.py',kit/'runtime_probe.py',kit/'ffxii_runtime.py']})
h=None
try:
    board=json.loads(team.BOARD.read_text())
    assert any(t['agent']=='ASTRA' and t['status']=='ACTIVE' and any(r['key']=='@runtime' for r in t['resources']) for t in board['tasks'])
    assert rt.list_processes()==[owner], 'Process identity changed'
    raw=Path(owner['path']).read_bytes()
    record['exe_sha256']=hashlib.sha256(raw).hexdigest()
    assert record['exe_sha256']==rt.AUTHORITY_SHA256
    verdict,hits,modules=rt.classify(pid)
    record.update(module_verdict=verdict,watched_modules=hits,modules=modules)
    assert verdict=='clean' and modules
    # Win64 HANDLE is pointer-sized, including when Windows returns a high handle value.
    rp.k32.OpenProcess.restype=ctypes.c_void_p
    rp.k32.CloseHandle.argtypes=[ctypes.c_void_p]
    rp.k32.ReadProcessMemory.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
    rp.psapi.EnumProcessModules.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulong,ctypes.POINTER(ctypes.c_ulong)]
    h=rp.k32.OpenProcess(rp.PROCESS_QUERY_INFORMATION|rp.PROCESS_VM_READ,False,pid)
    assert h
    reader=rp.Probe(h)
    record['image_base']=rp.module_base(h)
    assert record['image_base']==rp.IMAGE_BASE
    control=reader.read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES))
    record['known_read_control']=control.hex() if control is not None else None
    assert control==rp.CONTROL_BYTES
    record['null_read_rejected']=reader.read(0,16) is None
    assert record['null_read_rejected']
    pe=struct.unpack_from('<I',raw,0x3c)[0]
    count=struct.unpack_from('<H',raw,pe+6)[0]
    table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
    texts=[]
    for n in range(count):
        off=table+n*40
        if raw[off:off+8].rstrip(b'\0')!=b'.text':continue
        vs,rva,size,ro=struct.unpack_from('<IIII',raw,off+8)
        expected=raw[ro:ro+min(size,vs)]
        actual=reader.read(rp.IMAGE_BASE+rva,len(expected))
        assert actual is not None
        texts.append(dict(address=rp.IMAGE_BASE+rva,bytes=len(expected),
             disk_sha256=hashlib.sha256(expected).hexdigest(),live_sha256=hashlib.sha256(actual).hexdigest(),matches=actual==expected))
    record['code_identity']=texts
    assert len(texts)==1 and texts[0]['matches']
    import input_sample
    record['authored_profiles_before']=reader.read(0x1F80F90,0x150).hex()
    record['live_profiles_before']=reader.read(0x1F80130,0x414).hex()
    start=time.perf_counter()
    print('Keyboard sampling started;20 seconds maximum,4000 samples cap.',flush=True)
    for sample_index in range(4000):
        if time.perf_counter()-start>=20:break
        sample_start=time.perf_counter()
        sample_unix=time.time()
        row=input_sample.snapshot(reader)
        row.update(index=sample_index,start_unix=sample_unix,elapsed_before=sample_start-start,
                   elapsed_after=time.perf_counter()-start)
        record['samples'].append(row)
        assert row['status']=='STABLE_CHAIN','Keyboard chain changed; no registration verdict'
        time.sleep(.005)
    assert record['samples'],'Zero-case observation is invalid'
    record['authored_profiles_after']=reader.read(0x1F80F90,0x150).hex()
    record['live_profiles_after']=reader.read(0x1F80130,0x414).hex()
    assert record['authored_profiles_before']==record['authored_profiles_after']
    assert record['live_profiles_before']==record['live_profiles_after']
    record['known_read_control_after']=reader.read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES)).hex()
    assert record['known_read_control_after']==rp.CONTROL_BYTES.hex()
    record['code_sha256_after']=hashlib.sha256(reader.read(texts[0]['address'],texts[0]['bytes'])).hexdigest()
    assert record['code_sha256_after']==texts[0]['disk_sha256']
    verdict,hits,modules=rt.classify(pid)
    record.update(module_verdict_after=verdict,watched_modules_after=hits,modules_after=modules)
    assert verdict=='clean' and modules
    record['status']='RECORDED_ONLY'
    record['limits']=['No input is sent by this observer.',
        'Finite sample gaps cannot exclude brief transitions between reads.',
        'Zero bytes without a separately established positive keyboard control are inconclusive.',
        'Stable pointer chains and frame brackets are sequential, not atomic or ABA-proof.',
        'A nonzero held byte establishes sampled state, not command acceptance or execution.']
except BaseException as e:
    record['error']=repr(e)
finally:
    if h:
        record['read_handle_closed']=bool(rp.k32.CloseHandle(h))
        if not record['read_handle_closed']:record['status']='INVALID'
    record['end_unix']=time.time()
    with out.open('x',encoding='utf-8') as output:
        output.write(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ('modules','modules_after','samples')},indent=2))
print('samples',len(record['samples']),'nonzero samples',sum(bool(s.get('nonzero_indices')) for s in record['samples']))
sys.exit(0 if record['status']=='RECORDED_ONLY' and record.get('read_handle_closed') else 1)
