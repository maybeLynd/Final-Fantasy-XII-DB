"""One bounded input pulse with exact reads and fresh actor positions; no game-memory writes."""
import argparse
import ctypes
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import time

root=Path(__file__).resolve().parent
kit=root.parents[3]/'Tools/analysis-kit/gfz-scripts'
sys.path[:0]=[str(kit),str(root.parent/'EXP-023-camera-input')]
import runtime_probe as rp
import window_focus as wf
import key_packet

KEYS={'Space':(0x20,80),'C':(0x43,30),'W':(0x57,50),'A':(0x41,28),
      'S':(0x53,46),'D':(0x44,31),'Right':(0x27,92),'Left':(0x25,91),
      'I':(0x49,36),'J':(0x4A,37),'K':(0x4B,38),'L':(0x4C,39)}

class Reader:
    def __init__(self,pid):
        self.handle=rp.k32.OpenProcess(rp.PROCESS_VM_READ|rp.PROCESS_QUERY_INFORMATION,False,pid)
        if not self.handle: raise OSError(ctypes.get_last_error(),'OpenProcess(read)')
        self.probe=rp.Probe(self.handle)
    def read(self,a,n):
        raw=self.probe.read(a,n)
        if raw is None or len(raw)!=n: raise ValueError('short read %#x/%d'%(a,n))
        return raw
    def num(self,a,fmt):return struct.unpack(fmt,self.read(a,struct.calcsize(fmt)))[0]
    def close(self):rp.k32.CloseHandle(self.handle)
    def held(self):
        manager=self.num(0x02EA5368,'<Q');assert manager
        backend=self.num(manager+0xDF8,'<Q');assert backend
        block=self.num(backend+0x118,'<Q');assert block
        return block+0x30,self.read(block+0x30,256)
    def field(self):
        start=self.num(0x0208D45C,'<I')
        pool=self.num(0x0208E688,'<Q');assert pool
        assert self.num(0x0208E6A0,'<i')==32
        rows=[]
        for slot in range(32):
            unit=pool+slot*0xF50
            if not self.num(unit,'<B')&1:continue
            assert self.num(unit+0xEA9,'<B')==slot
            actor=self.num(unit+0x10,'<Q')
            if not actor:continue
            cls=self.num(actor+3,'<B')>>5
            if cls not in (1,3):continue
            movement=self.num(actor+0xB8,'<Q')
            if not movement:continue
            raw=self.read(movement,12);position=struct.unpack('<3f',raw)
            assert all(math.isfinite(x) for x in position)
            page=self.num(unit+0x698,'<Q')
            rows.append(dict(slot=slot,unit=unit,actor=actor,actor_class=cls,movement=movement,
                             group=self.num(unit+0xE98,'<B'),mode=self.num(unit+0xE99,'<B'),
                             position=position,position_raw=raw.hex(),
                             hp=self.num(page+0x48,'<i') if page else None))
        return dict(frame_before=start,frame_after=self.num(0x0208D45C,'<I'),rows=rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--pid',type=int,required=True)
    p.add_argument('--key',choices=KEYS)
    p.add_argument('--hold',type=float,default=.35)
    p.add_argument('--field',action='store_true')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();assert 0<a.hold<=1 and not a.out.exists()
    record=dict(pid=a.pid,command=sys.argv,start_unix=time.time(),status='INCOMPLETE',
                sources={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in
                         [Path(__file__),Path(key_packet.__file__),kit/'runtime_probe.py',kit/'window_focus.py']})
    reader=None;pressed=False
    try:
        found=rp.find_process('FFXII_TZA.exe');assert len(found)==1 and found[0][0]==a.pid
        record['exe_sha256']=hashlib.sha256(Path(found[0][1]).read_bytes()).hexdigest()
        assert record['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
        reader=Reader(a.pid)
        assert rp.module_base(reader.handle)==rp.IMAGE_BASE
        assert reader.read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES))==rp.CONTROL_BYTES
        if a.field:record['before']=reader.field()
        if a.key:
            wins=wf.windows_of(a.pid);assert wins
            hwnd=max(wins,key=lambda x:x[2]*x[3])[0]
            ok,foreground=wf.focus(hwnd);record['foreground']=dict(hwnd=hwnd,observed=foreground,ok=ok);assert ok
            baseline=[]
            for i in range(10):
                va,raw=reader.held();baseline.append(raw.hex());assert not any(raw);time.sleep(.01)
            record['baseline']=baseline
            vk,code=KEYS[a.key];record.update(key=a.key,hold=a.hold,expected_code=code)
            event=key_packet.packet(vk,False)
            record['packet']=dict(vk=event.u.ki.wVk,scan=event.u.ki.wScan,flags=event.u.ki.dwFlags)
            pressed=True;key_packet.send_key(vk,False)
            started=time.perf_counter();seen=set();polls=0
            try:
                while time.perf_counter()-started<a.hold:
                    current,raw=reader.held();assert current==va
                    seen.update(i for i,v in enumerate(raw) if v);polls+=1
                    assert key_packet.probe.u32.GetForegroundWindow()==hwnd,'lost focus'
                    time.sleep(.01)
            finally:
                key_packet.send_key(vk,True);pressed=False
            record.update(actual_hold=time.perf_counter()-started,seen_indices=sorted(seen),polls=polls)
            time.sleep(.06)
            current,raw=reader.held();record['after_release']=raw.hex();assert current==va and not any(raw)
            assert seen=={code-28},'wrong or ambiguous delivered code'
        if a.field:record['after']=reader.field()
        record['status']='CONTROLLED_PULSE' if a.key else 'READ_ONLY_SNAPSHOT'
    except BaseException as e:
        record['error']=repr(e)
        raise
    finally:
        if pressed:
            try:key_packet.send_key(KEYS[a.key][0],True)
            except BaseException as e:record['release_error']=repr(e)
        if reader:reader.close()
        record['end_unix']=time.time()
        a.out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in record.items() if k in ('status','error','key','seen_indices','after')}))

if __name__=='__main__':main()
