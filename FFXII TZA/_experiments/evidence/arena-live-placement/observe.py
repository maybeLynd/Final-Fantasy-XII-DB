"""Bounded read-only arena snapshots, using runtime_probe and EXP031 identity controls."""
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
assert label in ('title','loaded')
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
    assert any(t['id']=='ASTRA-ARENA-PLACEMENT-RUNTIME' and t['agent']=='ASTRA' and t['status']=='ACTIVE' for t in board['tasks'])
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
        s=dict(start_unix=time.time())
        for name,addr,size in [('base',0x1f83530,8),('selector',0x22d89a8,0x20),('arenas',0x22d7fd0,15*0xa8)]:
            b=reader.read(addr,size)
            assert b is not None,(name,hex(addr),size)
            s[name]=dict(address=addr,bytes=b.hex())
        sel=bytes.fromhex(s['selector']['bytes'])
        mask=struct.unpack_from('<I',sel,0x10)[0]
        assert mask and mask<1<<15 and all(x<15 for x in sel[:15])
        s['enabled_mask']=mask
        s['selected_arena']=struct.unpack_from('<i',sel,0x14)[0]
        s['decoder_base']=struct.unpack('<Q',bytes.fromhex(s['base']['bytes']))[0]
        records=bytes.fromhex(s['arenas']['bytes'])
        s['enabled_records']=[]
        for i in range(15):
            if not mask&(1<<i):continue
            b=records[i*0xa8:(i+1)*0xa8]
            item=dict(id=i,fields={hex(o):struct.unpack_from('<Q',b,o)[0] for o in (8,0x20,0x28,0x30,0x38,0x40,0x90,0x98)},pointed_bytes=[])
            for o in (8,0x38,0x90,0x98):
                a=item['fields'][hex(o)]
                if not a:continue
                got=reader.read(a,64)
                item['pointed_bytes'].append(dict(field=hex(o),address=a,bytes=got.hex() if got is not None else None))
            s['enabled_records'].append(item)
        s['selector_after']=reader.read(0x22d89a8,0x20).hex()
        s['base_after']=reader.read(0x1f83530,8).hex()
        s['end_unix']=time.time()
        record['samples'].append(s)
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
    print('sample',s['start_unix'],'mask',hex(s['enabled_mask']),'base',hex(s['decoder_base']),'selected',s['selected_arena'])
    for i in s['enabled_records']:print('arena',i['id'],{k:hex(v) for k,v in i['fields'].items()})
sys.exit(0 if record['status']=='OBSERVED' and record.get('read_handle_closed') else 1)
