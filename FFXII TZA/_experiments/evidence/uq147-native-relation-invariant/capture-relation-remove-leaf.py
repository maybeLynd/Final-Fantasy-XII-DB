"""Bounded original-code CFG qualification for the512CD0 leaf entry.

No .pdata row is invented. Only entry-reachable instructions are normalized;
the following known physical function begins at512D80. No execution occurs.
"""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
from capstone.x86_const import X86_OP_IMM
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';BASE=0x120000
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def main():
    output=P/sys.argv[1];need(not output.exists(),'fresh source required')
    exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';raw=exe.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference changed')
    pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;oz=struct.unpack_from('<H',raw,pe+20)[0]
    secs=[struct.unpack_from('<IIII',raw,pe+32+oz+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def read(a,n):
        for _,v,s,o in secs:
            if BASE+v<=a and a+n<=BASE+v+s:return raw[o+a-BASE-v:o+a-BASE-v+n]
        raise ValueError('unbacked original bytes')
    rva,n=struct.unpack_from('<II',raw,opt+112+24);pd=read(BASE+rva,n)
    rows=[struct.unpack_from('<III',pd,k) for k in range(0,len(pd),12)]
    need(not any(BASE+a<=0x512cd0<BASE+b for a,b,u in rows),'covering physical identity exists; consume it')
    need(any(BASE+a==0x512d80 for a,b,u in rows),'next physical entry changed')
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
    pending=[0x512cd0];seen={};edges={}
    while pending:
        pc=pending.pop()
        if pc in seen:continue
        need(0x512cd0<=pc<0x512d80 and len(seen)<96,'proposed leaf CFG escaped its bounded window')
        ins=next(cs.disasm(read(pc,min(15,0x512d80-pc)),pc,count=1),None)
        need(ins is not None,'incomplete original instruction')
        for a,i in seen.items():need(not a<pc<a+i.size,'branch into existing instruction')
        need(not any(pc<a<pc+ins.size for a in seen),'overlapping instruction boundaries')
        seen[pc]=ins;nextpc=pc+ins.size;m=ins.mnemonic
        if m=='ret':succ=[]
        elif m=='call':raise ValueError('original callee present; revise the leaf closure question')
        elif m.startswith('j'):
            need(len(ins.operands)==1 and ins.operands[0].type==X86_OP_IMM,'indirect control-flow boundary requires separate identity')
            succ=[ins.operands[0].imm]+([] if m=='jmp' else [nextpc])
        else:succ=[nextpc]
        edges[hex(pc)]=[hex(x) for x in succ];pending.extend(succ)
    need(seen and any(i.mnemonic=='ret' for i in seen.values()),'no normal return witness')
    addresses=sorted(seen);ranges=[];a=addresses[0];end=a+seen[a].size
    for pc in addresses[1:]:
        if pc!=end:ranges.append((a,end));a=pc
        end=pc+seen[pc].size
    ranges.append((a,end))
    driver=W/'ov42-gauge-callback-binding/capture-index-path.py'
    need(sha(driver)=='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497','actual reviewed access adapter path changed')
    spec=importlib.util.spec_from_file_location('reviewed_capture',driver);C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
    C.ROOT=ROOT;C.EXE=exe;C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=ranges
    sys.argv=[str(driver),str(output)];C.main()
    result=json.loads(output.read_text());need({int(i['pc'],16) for r in result['ranges'] for i in r['instructions']}==set(seen),'normalization reachable-PC domain changed')
    result.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),entry='0x512cd0',normal_cfg_edges=edges,
        physical_identity=dict(covering_pdata_rows=[],upper_neighbor_entry='0x512d80',basis='Verified direct native512F30 call/tail target; all bounded local successors and normal returns qualified. Not a fabricated physical function extent.'),
        limits='MethodA static original code/entry-reachable CFG only. Malformed pointers/cycles, initialization/lifetime and semantic effects still require separate analysis. No native/emulated/game execution.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('Qualified entry-reachable original removal leaf with actual shared byte roles; no .pdata root invented, no execution.')
if __name__=='__main__':main()
