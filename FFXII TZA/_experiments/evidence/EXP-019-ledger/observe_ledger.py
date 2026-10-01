"""Read-only EXP019: retain changed ledger/unit states, sampling times and frame brackets.

No debugger, writes, focus or input. A missed transient is not proof of absence.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

KIT = Path(__file__).resolve().parents[4] / 'Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(KIT))
import runtime_probe as rp
import ffxii_runtime as runtime


def decode_ledger(raw):
    if len(raw) != 64*24:
        raise ValueError('ledger must contain exactly64 entries')
    return [dict(group=i+1, member=struct.unpack_from('<Q',raw,i*24)[0],
                 dead=struct.unpack_from('<Q',raw,i*24+8)[0], flags=raw[i*24+16])
            for i in range(64)]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--pid',required=True,type=int)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--seconds',type=float,default=3)
    parser.add_argument('--hz',type=int,default=20)
    args=parser.parse_args()
    assert 0 < args.seconds <= 180 and 1 <= args.hz <= 100
    assert not args.out.exists(), 'never overwrite a previous observation'
    result=dict(pid=args.pid,command=sys.argv,start_unix=time.time(),status='INVALID',states=[],samples=[],
                source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                               [Path(__file__),KIT/'runtime_probe.py',KIT/'ffxii_runtime.py']})
    handle=None
    try:
        found=rp.find_process('FFXII_TZA.exe')
        assert len(found)==1 and found[0][0]==args.pid
        exe=Path(found[0][1]);data=exe.read_bytes()
        result.update(exe=str(exe),exe_sha256=hashlib.sha256(data).hexdigest())
        assert result['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
        verdict,hits,modules=runtime.classify(args.pid)
        result.update(module_verdict=verdict,watched_modules=hits,modules=modules)
        assert verdict=='clean' and modules
        handle=rp.k32.OpenProcess(rp.PROCESS_VM_READ|rp.PROCESS_QUERY_INFORMATION,False,args.pid)
        assert handle
        reader=rp.Probe(handle)
        def read(address,size):
            raw=reader.read(address,size)
            if raw is None:raise ValueError('unreadable %x/%d'%(address,size))
            return raw
        def number(address,fmt):return struct.unpack(fmt,read(address,struct.calcsize(fmt)))[0]
        assert rp.module_base(handle)==rp.IMAGE_BASE
        assert read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES))==rp.CONTROL_BYTES
        pe=struct.unpack_from('<I',data,0x3c)[0]
        table=pe+24+struct.unpack_from('<H',data,pe+20)[0]
        sections=[]
        for i in range(struct.unpack_from('<H',data,pe+6)[0]):
            off=table+i*40
            if data[off:off+8].rstrip(bytes([0]))!=b'.text':continue
            virtual,rva,size,raw_off=struct.unpack_from('<4I',data,off+8)
            expected=data[raw_off:raw_off+min(virtual,size)];actual=read(rp.IMAGE_BASE+rva,len(expected))
            assert actual==expected
            sections.append(dict(rva=rva,bytes=len(actual),sha256=hashlib.sha256(actual).hexdigest()))
        assert len(sections)==1
        result['code_identity']=sections
        last=None;start=time.perf_counter()
        print('OBSERVING ledger',args.pid,flush=True)
        while time.perf_counter()-start < args.seconds:
            t0=time.perf_counter()-start;frame0=number(0x0208D45C,'<I')
            pool=number(0x0208E688,'<Q');capacity=number(0x0208E6A0,'<i')
            assert pool and capacity==32, 'pool identity/capacity control'
            units=[]
            for slot in range(capacity):
                address=pool+slot*0xf50;header=read(address,0x18)
                if not header[0]&1:continue
                tail=read(address+0xe98,0x12)
                assert tail[0x11]==slot, 'active slot self-index control'
                actor=struct.unpack_from('<Q',header,0x10)[0]
                page=number(address+0x698,'<Q');spawn=number(address+0x6a0,'<Q')
                lane_map=number(address+0x40,'<Q')
                stats=read(page,0x50) if page else None
                bkei=number(actor+0xf6,'<H') if actor else None
                mapping=read(lane_map,1+number(lane_map,'<B')) if lane_map else None
                resolved=mapping[1+bkei] if mapping and bkei<len(mapping)-1 else None
                units.append(dict(slot=slot,address=address,header=header.hex(),group=tail[0],mode=tail[1],
                                  actor=actor,bkei=bkei,lane_map=lane_map,map_raw=mapping.hex() if mapping else None,
                                  resolved_slot=resolved,page=page,kind=stats[5] if stats else None,
                                  hp=struct.unpack_from('<i',stats,0x48)[0] if stats else None,
                                  hp_raw=stats[0x48:0x4c].hex() if stats else None,spawn=spawn,
                                  spawn_head=read(spawn,0x14).hex() if spawn else None))
            ledger=read(0x02ec13c0,1536)
            table_ptr=number(0x02098E68,'<Q')
            state=dict(pool=pool,capacity=capacity,units=units,ledger_raw=ledger.hex(),
                       table=table_ptr,slot3=number(table_ptr+6,'<H') if table_ptr else None,
                       actor_gate=number(0x02098e20,'<I'),dispatch_gate=number(0x02089340,'<I'),
                       field_gate=number(0x01fd46d4,'<I'),scale=number(0x01dfe0b8,'<f'))
            frame1=number(0x0208d45c,'<I');t1=time.perf_counter()-start
            if state!=last:
                result['states'].append(state);last=state
            result['samples'].append(dict(start_seconds=t0,end_seconds=t1,frame_before=frame0,
                                          frame_after=frame1,state_index=len(result['states'])-1))
            time.sleep(max(0,1/args.hz-(t1-t0)))
        result['status']='OBSERVED'
    except Exception as error:
        result['error']=repr(error)
    finally:
        if handle:rp.k32.CloseHandle(handle)
        result['end_unix']=time.time()
        with args.out.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2)
    for i,state in enumerate(result['states']):
        groups=[x for x in decode_ledger(bytes.fromhex(state['ledger_raw'])) if x['member'] or x['dead'] or x['flags']]
        print('state',i,'units',[(u['slot'],u['kind'],u['hp'],u['group'],u['mode'],u['resolved_slot']) for u in state['units']], 'ledger',groups,'slot3',state['slot3'])
    print(result['status'],result.get('error',''),flush=True)
    return 0 if result['status']=='OBSERVED' else 1


if __name__=='__main__':sys.exit(main())
