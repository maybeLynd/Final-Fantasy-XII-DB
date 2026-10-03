"""Scoped static identity for linked clear and inline reset; no physical roots invented."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
from capstone.x86_const import X86_OP_IMM
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';BASE=0x120000
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
def main():
    output=P/sys.argv[1];need(not output.exists(),'fresh output required')
    leaf=P/'source-relation-remove-leaf-01.json';need(sha(leaf)=='974aec9544ed4837a248d4c4f669435c6bbd24e232beb4906cef3037d64f911a' and json.loads(leaf.read_text())['entry']=='0x512cd0','preceding stop entry not qualified')
    raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference changed')
    pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;oz=struct.unpack_from('<H',raw,pe+20)[0]
    secs=[struct.unpack_from('<IIII',raw,pe+32+oz+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def read(a,n):
        for _,v,s,o in secs:
            if BASE+v<=a and a+n<=BASE+v+s:return raw[o+a-BASE-v:o+a-BASE-v+n]
        raise ValueError('unbacked original bytes')
    rva,n=struct.unpack_from('<II',raw,opt+112+24);pd=read(BASE+rva,n);rows=[struct.unpack_from('<III',pd,k) for k in range(0,len(pd),12)]
    need(any(BASE+a==0x512f30 for a,b,u in rows),'physical upper neighbor changed')
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
    complete={};bounds=[];ranges=[]
    for entry,upper in [(0x512c80,0x512cd0),(0x512ee0,0x512f30)]:
        need(not any(BASE+a<=entry<BASE+b for a,b,u in rows),'physical identity exists; consume it')
        pending=[entry];seen={};edges={}
        while pending:
            pc=pending.pop()
            if pc in seen:continue
            need(entry<=pc<upper and len(seen)<64,'bounded leaf escaped')
            i=next(cs.disasm(read(pc,min(15,upper-pc)),pc,count=1),None);need(i is not None,'undecoded instruction')
            need(not any(a<pc<a+z.size or pc<a<pc+i.size for a,z in seen.items()),'overlapping instruction boundaries')
            seen[pc]=i;m=i.mnemonic;nxt=pc+i.size
            if m=='ret':succ=[]
            elif m=='call':raise ValueError('opaque callee: revise exact claim')
            elif m.startswith('j'):
                need(len(i.operands)==1 and i.operands[0].type==X86_OP_IMM,'indirect successor')
                succ=[i.operands[0].imm]+([] if m=='jmp' else [nxt])
            else:succ=[nxt]
            edges[hex(pc)]=[hex(x) for x in succ];pending.extend(succ)
        need(any(i.mnemonic=='ret' for i in seen.values()),'normal RET missing')
        addresses=sorted(seen);a=addresses[0];end=a+seen[a].size
        for pc in addresses[1:]:
            if pc!=end:ranges.append((a,end));a=pc
            end=pc+seen[pc].size
        ranges.append((a,end));complete.update(seen)
        bounds.append(dict(entry=hex(entry),stop_entry=hex(upper),no_covering_pdata=True,instructions=len(seen),normal_cfg_edges=edges))
    driver=W/'ov42-gauge-callback-binding/capture-index-path.py';need(sha(driver)=='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497','reviewed capture path changed')
    spec=importlib.util.spec_from_file_location('reviewed_capture',driver);C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
    C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=ranges
    sys.argv=[str(driver),str(output)];C.main()
    s=json.loads(output.read_text());need({int(i['pc'],16) for r in s['ranges'] for i in r['instructions']}==set(complete),'actual normalized PC domain changed')
    s.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),entry_boundaries=bounds,limits='Static entry-reachable CFG only, no physical function root invented. No execution/initialization/caller order/reuse/semantic acceptance.')
    output.write_text(json.dumps(s,indent=2)+'\n');print('Qualified linked-clear and inline-reset leaves; no execution or ownership conclusion.')
if __name__=='__main__':main()
