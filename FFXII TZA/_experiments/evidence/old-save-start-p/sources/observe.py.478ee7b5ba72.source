"""Bounded read-only BattleUnit binding and save snapshots, using runtime_probe and EXP031 identity controls."""
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
assert label in ('current-complete','current-field','returned-title','old-after-current-complete','old-after-current-field','old-after-current-field-settled')
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
    assert any(t['id']=='FABLE-REQ-ASTRA-OLD-SAVE-LOAD' and t['agent']=='ASTRA' and t['status']=='ACTIVE' and any(r['key']=='@runtime' for r in t.get('claimed_resources',t['resources'])) for t in board['tasks'])
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
    for sample_index in range(2):
        s=dict(index=sample_index,start_unix=time.time(),reads=[])
        record['samples'].append(s) # retain incomplete data if a subsequent control fails
        def read(name,address,size):
            assert 0<size<=0x100000,(name,'bounded extent',size)
            b=reader.read(address,size)
            assert b is not None and len(b)==size,(name,hex(address),size)
            s['reads'].append(dict(name=name,address=address,size=size,bytes=b.hex(),sha256=hashlib.sha256(b).hexdigest()))
            return b
        base_raw=read('image_address_base_before',0x1F83530,8)
        base=struct.unpack('<Q',base_raw)[0]
        registry=read('registry_before',0x2EBF120,0x78)
        pool_header=read('pool_keep_capacity_before',0x208E688,0x20)
        pool,keep1,keep2,capacity=struct.unpack_from('<QQQi',pool_header)
        s.update(pool=pool,capacity=capacity,keep_bindings=[keep1,keep2],tables={})
        assert 0<=capacity<=32,'Unexpected pool extent'
        read('field_history_stamp_before',0x208936C,12)
        read('clock_parity_before',0x208D450,16)
        read('active_save_image',0x2164280,0x56690)
        battle=struct.unpack_from('<Q',registry,0x70)[0]
        s['battle_binding']=battle
        if battle:read('bound_battle_block',battle,0x7410)
        for n,p in enumerate([keep1,keep2],1):
            if p:read('keep_bank_'+str(n),p,0x9400)
        for name,off in [('enemy',0),('party',0x10),('class',0x30)]:
            descriptor=struct.unpack_from('<Q',registry,off)[0]
            entry=dict(descriptor=descriptor);s['tables'][name]=entry
            if not descriptor:continue
            header=read(name+'_table_header',descriptor,0x20)
            count=struct.unpack_from('<I',header,4)[0]
            stride=struct.unpack_from('<H',header,8)[0]
            reference=struct.unpack_from('<I',header,12)[0]
            resolved=(base+reference)&0xffffffffffffffff
            entry.update(count=count,stride=stride,reference=reference,resolved_base=resolved)
            assert count<=4096 and 0<stride<=0x400 and count*stride<=0x100000,'Unexpected table extent'
            if count:
                assert resolved,'Null row address'
                read(name+'_table_rows',resolved,count*stride)
        if pool and capacity:
            units=read('battle_unit_pool',pool,capacity*0xF50)
            # Read targets only for occupied slots with a bound actor and stats pointer.
            # Expected ownership is evaluated later, never an inclusion filter.
            for slot in range(capacity):
                u=units[slot*0xF50:(slot+1)*0xF50]
                actor=struct.unpack_from('<Q',u,0x10)[0]
                stats=struct.unpack_from('<Q',u,0x698)[0]
                if u[0]&1 and actor and stats:
                    read('unit_'+str(slot)+'_stats',stats,0x1C8)
            after=read('battle_unit_pool_after',pool,capacity*0xF50)
            def identities(raw):
                return [(bool(raw[k*0xF50]&1),raw[k*0xF50+8:k*0xF50+0x18],
                         raw[k*0xF50+0x698:k*0xF50+0x6A8],
                         raw[k*0xF50+0xE60:k*0xF50+0xE70],raw[k*0xF50+0xEA9])
                        for k in range(capacity)]
            s['unit_bindings_stable']=identities(units)==identities(after)
        else:s['unit_bindings_stable']=None
        s['registry_stable']=read('registry_after',0x2EBF120,0x78)==registry
        s['pool_keep_stable']=read('pool_keep_capacity_after',0x208E688,0x20)==pool_header
        s['base_stable']=read('image_address_base_after',0x1F83530,8)==base_raw
        read('field_history_stamp_after',0x208936C,12)
        read('clock_parity_after',0x208D450,16)
        s['end_unix']=time.time()
        assert s['registry_stable'] and s['pool_keep_stable'] and s['base_stable'],'Binding changed during sequential capture'
        assert s['unit_bindings_stable'] is not False,'Unit identity or pointer changed during sequential capture'
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
    print('sample',s['index'],'pool',hex(s.get('pool',0)),'reads',len(s['reads']),'unit_bindings_stable',s.get('unit_bindings_stable'))
sys.exit(0 if record['status']=='OBSERVED' and record.get('read_handle_closed') else 1)
