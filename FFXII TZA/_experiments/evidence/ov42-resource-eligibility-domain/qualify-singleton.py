"""Qualify the precise initialized-root premise from original accessor code.

Consumes the existing output invariant; does not run machine code or recapture
the already published constructor. Constructor calls remain opaque effects.
"""
import copy, hashlib, importlib.util, json, struct, sys
import capstone
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def need(x,m):
    if not x: raise ValueError(m)

def module(n,f):
    s=importlib.util.spec_from_file_location(n,P/f)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def derive(ix,G):
    ops=[(0x1d50dd,'mov','rax, qword ptr [rip + 0x1dac344]'),
         (0x1d50e4,'test','rax, rax'),(0x1d50e7,'jne','0x1d510d'),
         (0x1d50e9,'mov','ecx, 0x10e8'),(0x1d50ee,'call','0x210ec0'),
         (0x1d50f8,'test','rax, rax'),(0x1d50fb,'je','0x1d5106'),
         (0x1d50fd,'mov','rcx, rax'),(0x1d5100,'call','0x1ccb20'),
         (0x1d5106,'mov','qword ptr [rip + 0x1dac31b], rax'),
         (0x1ccb42,'mov','rdi, rcx'),(0x1ccb45,'xor','ebp, ebp'),
         (0x1ccc4b,'mov','dword ptr [rdi + 0xc20], ebp'),
         (0x1ccfc2,'mov','rax, rdi')]
    for pc,m,a in ops:
        need(pc in ix and (ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'singleton operation changed '+hex(pc))
    body=G.graph(ix,0x1d50d0,0x1d5112)
    need(body['calls']==[(0x1d50ee,'0x210ec0'),(0x1d5100,'0x1ccb20')] and body['returns']==[0x1d5111],'singleton body boundaries/calls changed')
    def root(m,pc):
        return m['base']=='rip' and pc+len(bytes.fromhex(ix[pc]['bytes']))+m['displacement']==0x1f81428
    read=ix[0x1d50dd]['memory'];write=ix[0x1d5106]['memory']
    need(len(read)==len(write)==1 and root(read[0],0x1d50dd) and root(write[0],0x1d5106) and read[0]['size']==write[0]['size']==8,'singleton cell identity/width changed')
    fast=G.graph(ix,0x1d50d0,0x1d5112,fixed={0x1d50e7:True})
    stores=[(pc,m) for pc in fast['visited'] for m in ix[pc]['memory'] if m['role'] in ['w','rw']]
    need(not fast['calls'] and fast['returns']==[0x1d5111] and all(m['base']=='rsp' for pc,m in stores),'initialized singleton path has new call/nonstack write')
    ctor=G.graph(ix,0x1ccb20,0x1ccfda)
    need(G.dominates(ctor,0x1ccb45,0x1ccc4b),'constructor zero register initialization can be bypassed')
    # EBP is nonvolatile under the required ABI. The own prefix does not change
    # it after XOR; omitted callee ABI violations are not silently excluded.
    decoder=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);decoder.detail=True
    for pc in sorted(ctor['visited']):
        if 0x1ccb45<pc<0x1ccc4b:
            inst=list(decoder.disasm(bytes.fromhex(ix[pc]['bytes']),pc))
            need(len(inst)==1 and (inst[0].mnemonic,inst[0].op_str)==(ix[pc]['mnemonic'],ix[pc]['args']),'constructor register control requires real instruction identity')
            written=[inst[0].reg_name(r) for r in inst[0].regs_access()[1]]
            need(not {'ebp','rbp','bp','bpl'}.intersection(written),'constructor prefix overwrites zero register')
    after=[(hex(pc),target) for pc,target in ctor['calls'] if pc>0x1ccc4b]
    return dict(
        known_fact='Lazy allocation/constructor/root publication was already canonical in s26-runtime-per-invariant-exposure and Developer-Tuning-Console. This source qualification is not new discovery or a new execution.',
        accessor='1D50D0 reads QWORD cell01F81428. NonNULL fast path returns that exact pointer without calls or own nonstack writes. NULL path requests0x10E8 bytes through210EC0, conditionally calls1CCB20 with allocation asRCX, then stores resultingRAX to01F81428. Allocation/constructor effects remain opaque; no atomically initialized or thread-safe publication claim.',
        conditional_two_reads='With initially nonNULL01F81428, accessible same object/private frames/ordinaryABI, and no other mutation of the root/C20 during30B7F0, both17D470 calls take the call-free initialized accessor path and read the sameC20. The query body has no calls other than those two getters and only private output-stack writes. Consequently the existing upperWORD formula narrows0..3 to0..2 in that stated window. This does not prove natural initialized root, lifetime or absence of concurrent/alias writes.',
        missing_root='If allocation returnsNULL normally,1D50D0 publishes/returnsNULL and17D470 then attemptsDWORD read[0+C20]. This is a source-level precondition, not an observed fault or proof the shipping allocator returnsNULL.',
        constructor_store='Retained complete1CCB20 has ownDWORDobject+C20=0 store at1CCC4B, EBP zero established1CCB45 under normalnonvolatileABI. Later calls are opaque here: this store alone does not prove final constructor default or allplayC20=0.',
        post_store_opaque_calls=after,
        remaining='Actual initialized root and writer/alias/lifetime/scheduling closure remain separate. Do not assert Invincible unreachable/unchanging from this body or re-run the prior console dispatcher census.',
        limits='STATIC_ONLY source/dataflow conditional proof. No native/emulated/live execution; no sampled settings values, natural command reachability, visible effects or transitive constructor purity.'
    )

def main():
    out=P/sys.argv[1];need(not out.exists(),'immutable output exists')
    need(sha(P/'prove.py')=='d9210a436de2bf6080f360e64716544db022a097ae29ac4c5785b98585c8bac7','base invariant producer changed')
    status=json.loads((P/'proof-02.status.json').read_text());base=json.loads((P/'result-02.json').read_text())
    need(status.get('terminal') is True and status.get('exit')==0 and status.get('exception') is None and status.get('driver_sha256')==sha(P/'prove.py') and base.get('producer_complete') is True and base.get('driver_sha256')==sha(P/'prove.py'),'base invariant result/status failed')
    need((P/'proof-02.stdout').read_bytes() and not (P/'proof-02.stderr').read_bytes(),'base invariant missing/nonclean output')
    for x in base['source_pins']:need(sha(P/x['path'])==x['sha256'],'base source changed')
    C=module('prerequisites','capture_prerequisites.py')
    qualifications=[C.check(P,'prepare-extents.py','capture.py','extents-01','capture-01','extents-01.json','source-01.json',['0x30b770','0x30b7f0']),
      C.check(P,'prepare-mode-extents.py','capture-mode.py','mode-extents-01','mode-capture-01','mode-extents-01.json','mode-source-01.json',['0x17d470']),
      C.check(P,'prepare-singleton-extents.py','capture-singleton.py','singleton-extents-01','singleton-capture-01','singleton-extents-01.json','singleton-source-01.json',['0x1d50d0'])]
    need(sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13' and sha(P/'prove_owner_reload_order.py')=='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864','reviewed source dependencies changed')
    raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'image changed')
    pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0]
    secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def read(a,n):
        for _,rva,sz,off in secs:
            if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
        raise ValueError('unbacked original bytes')
    V=module('roles','validate-title-source-annotations.py');G=module('cfg','prove_owner_reload_order.py');ix={};annotation=[]
    files=[x['path'] for x in base['source_pins']]+['singleton-source-01.json','retained-constructor-source-01.json']
    for f in files:
        x=json.loads((P/f).read_text());need(x['exe_sha256']==PIN,'source image mismatch');annotation.append(V.validate(x))
        for r in x['ranges']:
            a,b=int(r['start'],16),int(r['end_exclusive'],16)
            need(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))==read(a,b-a),'not original code')
            ix.update({int(i['pc'],16):i for i in r['instructions']})
    need(sha(P/'retained-constructor-source-01.json')=='91747eb0ccddaa9a37c3e1fbb3498a3d1995032e7d6137de16d4b62e91529656','retained constructor changed')
    facts=derive(ix,G);controls=[]
    for label,pc,val in [('root-publication-different-cell',0x1d5106,'qword ptr [rip + 0x1dac323], rax'),('initialized-branch-enters-allocation',0x1d50e7,'0x1d50e9'),('narrower-default-store',0x1ccc4b,'word ptr [rdi + 0xc20], bp'),('zero-register-clobber-prefix',0x1ccb96,'rbp, 1')]:
        changed=copy.deepcopy(ix);changed[pc]['args']=val
        try:derive(changed,G)
        except ValueError as e:controls.append(dict(label=label,refused=str(e),method='Synthetic source discrimination control, not original execution'))
        else:raise ValueError('source control accepted')
    result=dict(producer_complete=True,driver_sha256=sha(Path(__file__)),exe_sha256=PIN,method='A STATIC_ONLY original query invariants and initialized-root boundary',base_result=dict(path='result-02.json',sha256=sha(P/'result-02.json')),source_pins=[dict(path=f,sha256=sha(P/f)) for f in files],capture_prerequisites=qualifications,annotation_prerequisites=annotation,facts=facts,base_facts=base['facts'],source_controls=controls,limits=facts['limits'],acceptance='Producer valid; independent review/canonical incorporation pending')
    with out.open('x') as f:json.dump(result,f,indent=2)
    print('QUALIFIED initialized-root fast path; first-use effects remain explicit; retained constructor not recaptured')

if __name__=='__main__':main()
