"""Normalize one retained original body; no new native/game sampling."""
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
    lookup=P/'lookup-notify-preparation-01.json';z=json.loads(lookup.read_text())
    need(z.get('complete') is True and z.get('exe_sha256')==PIN and not z['matches'] and
         z['requested']==['0x313b30','0x313cca'],'consume existing covering map instead')
    bodies=ROOT/'Database/FFXII TZA/_experiments/evidence/commit-callees-exec/bodies.json'
    need(sha(bodies)=='a4dadd1ad580917767dcd29b3f337c8f1110be7ebdb11295930c9aa8731e8276','retained body identities changed')
    b=json.loads(bodies.read_text());need(b['exe_sha256']==PIN,'wrong original image')
    matches=[r for r in b['real_bodies_executed'] if int(r['va'],16)==0x313b30]
    need(len(matches)==1 and matches[0]['span']=='0x313B30-0x313CCA','exact retained body missing')
    codepin='ae38b605a33a5e7bf053f2482cf02f9d9e89625bad67651bf586dedd1c2ef4c1'
    need(matches[0]['sha256']==codepin==z['requested_sha256'],'retained/lookup bytes disagree')
    exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';raw=exe.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference changed')
    pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;optlen=struct.unpack_from('<H',raw,pe+20)[0]
    need(struct.unpack_from('<Q',raw,opt+24)[0]==BASE,'wrong image base')
    sections=[struct.unpack_from('<IIII',raw,pe+32+optlen+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def read(va,size):
        for _,rva,n,off in sections:
            if BASE+rva<=va and va+size<=BASE+rva+n:return raw[off+va-BASE-rva:off+va-BASE-rva+size]
        raise ValueError('unbacked original bytes')
    need(hashlib.sha256(read(0x313b30,410)).hexdigest()==codepin,'retained code differs')
    rva,n=struct.unpack_from('<II',raw,opt+112+3*8);pdata=read(BASE+rva,n)
    rows=[struct.unpack_from('<III',pdata,k) for k in range(0,len(pdata),12)]
    rows=[r for r in rows if BASE+r[0]<0x313cca and 0x313b30<BASE+r[1]]
    need(len(rows)==1 and (BASE+rows[0][0],BASE+rows[0][1])==(0x313b30,0x313cca),'physical function extent differs; revise preparation')
    driver=W/'ov42-gauge-callback-binding/capture-index-path.py'
    need(sha(driver)=='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497','actual reviewed capture path changed')
    s=importlib.util.spec_from_file_location('reviewed_capture',driver);C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
    C.ROOT=ROOT;C.EXE=exe;C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=[(0x313b30,0x313cca)]
    sys.argv=[str(driver),str(output)];C.main()
    result=json.loads(output.read_text());result.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),
        retained_identity=dict(path=bodies.relative_to(ROOT).as_posix(),sha256=sha(bodies),body=matches[0]),
        physical_bodies=[dict(start='0x313b30',end_exclusive='0x313cca',unwind_rva=hex(rows[0][2]),basis='Exact single physical exception-directory row')],
        preparation_lookup_sha256=sha(lookup),limits='Normalization of retained body only. No new machine-code/game execution, initialization, semantics or independent acceptance.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('Qualified retained410B notification body and exact physical extent; semantics pending, no native/game sample.')
if __name__=='__main__':main()
