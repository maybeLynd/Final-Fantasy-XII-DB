"""Two exact UQ147 request-tail dependencies; reuse the reviewed capture path."""
import hashlib, importlib.util, json, struct, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
BASE=0x120000
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    out=P/sys.argv[1]
    if out.exists():raise ValueError('fresh output required')
    # Feasibility is not semantic evidence; whole bounds are proved from .pdata below.
    for tag in ['preview-request-tail-01','preview-publish-01']:
        st=json.loads((P/(tag+'.status.json')).read_text())
        if st['terminal'] is not True or st['exit']!=0 or st['exception'] is not None or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise ValueError('exact dependency preview failed '+tag)
    for tag,wanted in [('lookup-request-tail-01',['0x317e60','0x317eb7']),('lookup-publish-01',['0x25aad0','0x25ab22'])]:
        st=json.loads((P/(tag+'.status.json')).read_text());lookup=json.loads((P/(tag+'.json')).read_text())
        if st['terminal'] is not True or st['exit']!=0 or st['exception'] is not None or lookup['complete'] is not True or lookup['requested']!=wanted or lookup['exe_sha256']!=PIN:raise ValueError('required retained lookup failed '+tag)
        if lookup['matches']:raise ValueError('retained covering map exists; consume it rather than recapture')
    raw=EXE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('reference image changed')
    pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;os=struct.unpack_from('<H',raw,pe+20)[0]
    if struct.unpack_from('<H',raw,opt)[0]!=0x20b or struct.unpack_from('<Q',raw,opt+24)[0]!=BASE:raise ValueError('wrong image type/base')
    secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def read(a,n):
        for _,rva,size,off in secs:
            if BASE+rva<=a and a+n<=BASE+rva+size:return raw[off+a-BASE-rva:off+a-BASE-rva+n]
        raise ValueError('unbacked original bytes')
    directory=raw[opt+136:opt+144];rva,n=struct.unpack('<II',directory)
    if not n or n%12:raise ValueError('malformed exception directory')
    data=read(BASE+rva,n);rows=[struct.unpack_from('<III',data,k) for k in range(0,n,12)];known=set(rows)
    def chain(row):
        seen=set();steps=[]
        while True:
            if row in seen or row not in known:raise ValueError('cyclic or unlisted chain')
            seen.add(row);h=read(BASE+row[2],4);flags=h[0]>>3
            if h[0]&7!=1:raise ValueError('unhandled unwind version')
            step=dict(record_bytes=struct.pack('<III',*row).hex(),header_address=hex(BASE+row[2]),header_bytes=h.hex())
            if flags&4:
                if flags&3:raise ValueError('mixed chain/handler flags')
                footer=BASE+row[2]+((4+h[2]*2+3)&~3);triple=read(footer,12)
                step.update(chain_footer=hex(footer),chain_bytes=triple.hex());row=struct.unpack('<III',triple);steps.append(step)
            else:steps.append(step);return row,steps
    bodies=[]
    for entry in [0x317e60,0x25aad0]:
        roots=[r for r in rows if r[0]==entry-BASE]
        if len(roots)!=1:raise ValueError('ambiguous physical root')
        root=roots[0];members=[]
        for row in rows:
            if entry-BASE<=row[0]<entry-BASE+4096:
                target,steps=chain(row)
                if target==root:members.append(dict(begin=hex(BASE+row[0]),end_exclusive=hex(BASE+row[1]),chain=steps))
        end=entry
        for m in members:
            if int(m['begin'],16)!=end or int(m['end_exclusive'],16)<=end:raise ValueError('noncontiguous body metadata')
            end=int(m['end_exclusive'],16)
        if not entry<end<=entry+4096:raise ValueError('bounded extent unavailable')
        z=read(entry,end-entry);bodies.append(dict(entry=hex(entry),end_exclusive=hex(end),bytes=len(z),sha256=hashlib.sha256(z).hexdigest(),physical_bytes=z.hex(),records=members))
    driver=W/'ov42-gauge-callback-binding/capture-index-path.py'
    if sha(driver)!='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497':raise ValueError('reviewed capture path changed')
    s=importlib.util.spec_from_file_location('reviewed_capture_path',driver);C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
    C.ROOT=ROOT;C.EXE=EXE;C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=[(int(b['entry'],16),int(b['end_exclusive'],16)) for b in bodies]
    sys.argv=[str(driver),str(out)];C.main()
    x=json.loads(out.read_text())
    for b,r in zip(bodies,x['ranges']):
        if b['physical_bytes']!=''.join(i['bytes'] for i in r['instructions']):raise ValueError('decoder/source correspondence failed')
    x.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),physical_exception_directory=directory.hex(),physical_bodies=bodies,limits='Complete local shipping bodies and actual reviewed role controls, not callee effects, command acceptance, cleanup timing, natural state/reachability or presentation. Two prerequisite previews are feasibility only; retained-map absence applies only to the searched corpus. Transitive callees/alias preconditions remain unproved.')
    out.write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps([dict(entry=b['entry'],bytes=b['bytes']) for b in bodies]))
if __name__=='__main__':main()
