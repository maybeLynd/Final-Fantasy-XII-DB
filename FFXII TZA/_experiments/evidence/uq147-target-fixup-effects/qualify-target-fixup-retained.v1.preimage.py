"""Method A: reuse retained original-code identities; no old native suites rerun."""
import hashlib, importlib.util, json, struct, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent; W=P.parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'; BASE=0x120000
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
def main():
    out=P/sys.argv[1];need(not out.exists(),'fresh source required')
    identity=[
      (ROOT/'Database/FFXII TZA/_experiments/evidence/commit-callees-exec/bodies.json','a4dadd1ad580917767dcd29b3f337c8f1110be7ebdb11295930c9aa8731e8276'),
      (ROOT/'Database/FFXII TZA/_experiments/evidence/unit-resolver-family-exec/bodies.json','0abd9369e4b8097f818bb8ad12516e4c465a2f774edf15c59ff444d4b11cf670'),
      (W/'uq147-mode-query-frozen-ready/source-mode-query-01.json','2218c4f027e33a8d878c65301004911e83076848de74303c2b44de3824473651')]
    for f,pin in identity:need(sha(f)==pin,'retained identity changed '+str(f))
    old=json.loads(identity[0][0].read_text());unit=json.loads(identity[1][0].read_text());mode=json.loads(identity[2][0].read_text())
    selected=[]
    for va in [0x2fead0,0x30c0e0]:
        z=[x for x in old if int(x['va'],16)==va];need(len(z)==1,'missing/ambiguous retained body')
        z=z[0];lo,hi=map(lambda x:int(x,16),z['span'].split('-'))
        selected.append(dict(start=lo,end=hi,sha256=z['sha256'],basis='Retained EXP091 original-byte body identity, not new native execution'))
    for va in [0x236820,0x236850,0x31b7e0,0x20e600,0x3588b0,0x263ff0,0x263e30]:
        z=[x for x in unit['real'] if int(x['va'],16)==va];need(len(z)==1,'missing/ambiguous retained resolver')
        z=z[0];selected.append(dict(start=va,end=int(z['end'],16),sha256=z['sha256'],basis='Retained EXP102 exact end/hash; no suite/sample rerun'))
    for r in mode['ranges']:
        selected.append(dict(start=int(r['start'],16),end=int(r['end_exclusive'],16),sha256=r['sha256'],basis='Retained mode-query original bytes; earlier new package acceptance still pending'))
    need(len(selected)==13 and len({x['start'] for x in selected})==13,'closure source domain missing/duplicate')
    exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';raw=exe.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference changed')
    pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;osz=struct.unpack_from('<H',raw,pe+20)[0]
    need(struct.unpack_from('<Q',raw,opt+24)[0]==BASE,'wrong image base')
    secs=[struct.unpack_from('<IIII',raw,pe+32+osz+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def read(a,n):
        for _,rva,size,off in secs:
            if BASE+rva<=a and a+n<=BASE+rva+size:return raw[off+a-BASE-rva:off+a-BASE-rva+n]
        raise ValueError('unbacked span')
    for r in selected:need(hashlib.sha256(read(r['start'],r['end']-r['start'])).hexdigest()==r['sha256'],'retained code hash differs')
    driver=W/'ov42-gauge-callback-binding/capture-index-path.py'
    need(sha(driver)=='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497','reviewed adapter invocation changed')
    s=importlib.util.spec_from_file_location('reviewed_capture_path',driver);C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
    C.ROOT=ROOT;C.EXE=exe;C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=[(x['start'],x['end']) for x in selected]
    sys.argv=[str(driver),str(out)];C.main()
    x=json.loads(out.read_text())
    for r,z in zip(x['ranges'],selected):need(''.join(i['bytes'] for i in r['instructions'])==read(z['start'],z['end']-z['start']).hex(),'actual decode incomplete')
    x.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),retained_inputs=[dict(path=f.relative_to(ROOT).as_posix(),sha256=pin) for f,pin in identity],selected_original_identities=[dict(start=hex(z['start']),end_exclusive=hex(z['end']),sha256=z['sha256'],basis=z['basis']) for z in selected],limits='Bounded Method A normalization of already retained shipping bodies with shared reviewed roles. No EXP091/102 native tests rerun; no new game/initialized state/sample. Complete effect claims require separately checked CFG/callee closure and private-stack/valid-state assumptions.')
    out.write_text(json.dumps(x,indent=2)+'\n');print('Qualified 13 retained original body identities; STATIC_ONLY, old native runs not repeated')
if __name__=='__main__':main()
