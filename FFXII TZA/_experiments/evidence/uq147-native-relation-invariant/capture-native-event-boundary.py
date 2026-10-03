"""Scoped Method A for the event body omitted by EXP091's stub.

Not an execution: validate the physical extent and actual shared role path.
"""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';BASE=0x120000
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def main():
    output=P/sys.argv[1];need(not output.exists(),'fresh output required')
    lookup=P/'lookup-native-event-preparation-01.json';z=json.loads(lookup.read_text())
    need(z.get('complete') is True and z['exe_sha256']==PIN and not z['matches'] and z['requested']==['0x512f30','0x513144'],'consume retained covering source instead')
    raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference changed')
    pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;oz=struct.unpack_from('<H',raw,pe+20)[0]
    secs=[struct.unpack_from('<IIII',raw,pe+32+oz+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def read(a,n):
        for _,v,s,o in secs:
            if BASE+v<=a and a+n<=BASE+v+s:return raw[o+a-BASE-v:o+a-BASE-v+n]
        raise ValueError('unbacked source')
    rva,n=struct.unpack_from('<II',raw,opt+112+24);b=read(BASE+rva,n)
    rows=[struct.unpack_from('<III',b,k) for k in range(0,len(b),12)]
    def root(t):
        seen=set()
        while True:
            need(t not in seen and t in rows,'unbound/cyclic unwind chain')
            seen.add(t);h=read(BASE+t[2],4)
            if not(h[0]>>3)&4:return t
            t=struct.unpack('<III',read(BASE+t[2]+4+((h[2]+1)//2)*4,12))
    selected=sorted(t for t in rows if BASE+t[0]<0x513144 and 0x512f30<BASE+t[1])
    need(len(selected)==7 and BASE+selected[0][0]==0x512f30 and BASE+selected[-1][1]==0x513144 and
         all(a[1]==b[0] for a,b in zip(selected,selected[1:])) and all(root(t)==selected[0] for t in selected),'complete native-event physical extent changed')
    driver=W/'ov42-gauge-callback-binding/capture-index-path.py'
    need(sha(driver)=='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497','actual reviewed adapter path changed')
    spec=importlib.util.spec_from_file_location('reviewed_capture',driver);C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
    C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=[(0x512f30,0x513144)]
    sys.argv=[str(driver),str(output)];C.main()
    s=json.loads(output.read_text());s.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),
        preparation_lookup_sha256=sha(lookup),physical_bodies=[dict(start=hex(BASE+t[0]),end_exclusive=hex(BASE+t[1]),unwind_rva=hex(t[2]),root_start=hex(BASE+root(t)[0])) for t in selected],
        question='Which local effects and native delegate boundaries were omitted by EXP091512F30 stub?',
        limits='Static physical access only. EXP091 did not execute this native body. No game, initialization, receiver-lifetime or transitive effect closure implied.')
    output.write_text(json.dumps(s,indent=2)+'\n')
    print('Qualified original532B/seven native-event fragments; no execution or semantic closure.')
if __name__=='__main__':main()
