"""Read documented R2 globals across one ordinary key press with explicit phase controls."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

root=Path(__file__).resolve().parent
kit=root.parents[3]/'Tools/analysis-kit/gfz-scripts'
sys.path[:0]=[str(root.parent/'EXP-024-group-approach'),str(root.parent/'EXP-023-camera-input'),str(kit)]
import step
import key_packet
import runtime_probe as rp
import window_focus as wf

FIELDS={'toggle':(0x020927E0,'<I'),'latch':(0x020927E4,'<B'),
        'sticky':(0x01E0C2B4,'<I'),'flag':(0x01E0C2B8,'<I'),
        'enable_a':(0x02B4053C,'<B'),'enable_b':(0x02B4053D,'<B'),
        'input_snapshot':(0x02F97360,'<I'),'ui_register':(0x022C83EC,'<I'),
        'override':(0x020927CC,'<I'),'audio_word':(0x022CB728,'<H'),'audio_byte':(0x022CB726,'<b')}

def main():
    p=argparse.ArgumentParser();p.add_argument('--pid',type=int,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    sources=[Path(__file__),Path(step.__file__),Path(key_packet.__file__),kit/'runtime_probe.py',kit/'runtime_input_probe.py',kit/'runtime_poke.py',kit/'window_focus.py']
    result=dict(pid=a.pid,command=sys.argv,start_unix=time.time(),status='INCOMPLETE',samples=[],
                sources={str(s):hashlib.sha256(s.read_bytes()).hexdigest() for s in sources})
    reader=None;pressed=False
    try:
        found=rp.find_process('FFXII_TZA.exe');assert len(found)==1 and found[0][0]==a.pid
        result['exe_sha256']=hashlib.sha256(Path(found[0][1]).read_bytes()).hexdigest()
        assert result['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
        reader=step.Reader(a.pid)
        assert rp.module_base(reader.handle)==rp.IMAGE_BASE
        assert reader.read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES))==rp.CONTROL_BYTES
        wins=wf.windows_of(a.pid);assert wins
        hwnd=max(wins,key=lambda w:w[2]*w[3])[0]
        ok,fg=wf.focus(hwnd);assert ok
        result['foreground']=dict(expected=hwnd,observed=fg)
        result['field_before']=reader.field()
        start=time.perf_counter()
        def sample(phase):
            frame0=reader.num(0x0208D45C,'<I')
            va,raw=reader.held()
            values={name:reader.num(addr,fmt) for name,(addr,fmt) in FIELDS.items()}
            entry=dict(phase=phase,seconds=time.perf_counter()-start,frame_before=frame0,
                       frame_after=reader.num(0x0208D45C,'<I'),held_va=va,held_raw=raw.hex(),values=values,
                       foreground=key_packet.probe.u32.GetForegroundWindow())
            result['samples'].append(entry)
            assert entry['foreground']==hwnd,'lost focus'
            return {i for i,b in enumerate(raw) if b}
        def phase(name,expected):
            begin=time.perf_counter();seen=set();polls=0
            while time.perf_counter()-begin<1:
                held=sample(name);seen.update(held);polls+=1
                if name=='baseline':assert not held,'baseline not clean'
                time.sleep(.01)
            assert polls>0
            assert seen==expected,(name,seen,expected)
        phase('baseline',set())
        pressed=True;result['down_accepted']=key_packet.send_key(0xA2,False)
        try:phase('held',{89})
        finally:result['up_accepted']=key_packet.send_key(0xA2,True);pressed=False
        time.sleep(.06)
        phase('released',set())
        result['field_after']=reader.field()
        result['status']='CONTROLLED_PRESS_RELEASE'
    except BaseException as e:
        result['error']=repr(e);raise
    finally:
        if pressed:
            try:key_packet.send_key(0xA2,True)
            except BaseException as e:result['release_error']=repr(e)
        if reader:reader.close()
        result['end_unix']=time.time()
        a.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        states={phase:sorted({tuple(s['values'][k] for k in ['toggle','latch','sticky','flag','enable_a','enable_b','ui_register']) for s in result['samples'] if s['phase']==phase}) for phase in ['baseline','held','released']}
        print(json.dumps(dict(status=result['status'],states=states,error=result.get('error'))))

if __name__=='__main__':main()
