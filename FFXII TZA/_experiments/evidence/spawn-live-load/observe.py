"""Bounded read-only save and persistence snapshots, using runtime_probe and EXP031 identity controls."""
import ctypes, hashlib, json, struct, sys, time
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root.parents[4]
kit=repo/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0,str(kit))
import runtime_probe as rp
import ffxii_runtime as rt
import team
label=sys.argv[1]
assert label in ('fresh-title','old-complete','old-field','current-complete','current-field','old-after-current-complete','old-after-current-field')
out=root/(label+'-memory.json')
assert not out.exists(), 'Preserve the previous observation'
owner=json.loads((root/'process.json').read_text())
pid=owner['pid']
record=dict(start_unix=time.time(),pid=pid,label=label,status='INVALID',samples=[],
            method='ReadProcessMemory only; no debug attach, writes, injected calls or suspended threads.',
            tool_hashes={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in [Path(__file__),kit/'runtime_probe.py',kit/'ffxii_runtime.py']})
h=None
try:
    board=json.loads(team.BOARD.read_text())
    assert any(t['id']=='FABLE-REQ-ASTRA-OLD-SAVE-LOAD' and t['agent']=='ASTRA' and t['status']=='ACTIVE' for t in board['tasks'])
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
    for _ in range(2):
        s=dict(start_unix=time.time(),reads=[])
        def read(name,address,size):
            b=reader.read(address,size)
            assert b is not None and len(b)==size,(name,hex(address),size)
            s['reads'].append(dict(name=name,address=address,size=size,bytes=b.hex(),sha256=hashlib.sha256(b).hexdigest()))
            return b
        binding=read('battle_binding_before',0x2EBF190,8)
        keep=read('keep_bindings_before',0x208E690,16)
        read('history_window_stamp_before',0x208936C,12)
        read('clock_parity_before',0x208D450,16)
        read('active_save_image',0x2164280,0x56690)
        b=struct.unpack('<Q',binding)[0]
        s['battle_binding']=b
        s['binding_matches_active_image']=b==0x21B290C
        if b:read('bound_battle_block',b,0x7410)
        s['keep_bindings']=list(struct.unpack('<QQ',keep))
        for index,pointer in enumerate(s['keep_bindings']):
            if pointer:read('keep_bank_'+str(index+1),pointer,0x9400)
        read('unit_definition_handle',0x2EBF130,8)
        read('gambit_preset_handle',0x2EBF0E0,8)
        s['binding_stable']=read('battle_binding_after',0x2EBF190,8)==binding
        s['keep_bindings_stable']=read('keep_bindings_after',0x208E690,16)==keep
        read('history_window_stamp_after',0x208936C,12)
        read('clock_parity_after',0x208D450,16)
        s['end_unix']=time.time()
        record['samples'].append(s)
        assert s['binding_stable'] and s['keep_bindings_stable'],'Pointer changed during sequential capture'
        time.sleep(.25)
    assert len(record['samples'])==2
    record['status']='OBSERVED'
except BaseException as e:
    record['error']=repr(e)
finally:
    if h:record['read_handle_closed']=bool(rp.k32.CloseHandle(h))
    record['end_unix']=time.time()
    out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k not in ('modules','samples')},indent=2))
for s in record['samples']:
    print('sample',s['start_unix'],'bound',hex(s['battle_binding']),'image_binding',s['binding_matches_active_image'],'keep',[hex(x) for x in s['keep_bindings']],'reads',len(s['reads']))
sys.exit(0 if record['status']=='OBSERVED' and record.get('read_handle_closed') else 1)
