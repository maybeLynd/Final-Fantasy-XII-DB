"""Conditional original instruction/data-flow proof; no reconstructed/native run."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
ESHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(src,out):
    if out.exists():raise ValueError('immutable result exists')
    status=json.loads((src/'filecache-equal-key-capture-01.status.json').read_text())
    if status.get('exit')!=0 or status.get('terminal') is not True or status.get('driver_sha256')!=sha(src/'capture-filecache-equal-key.py'):
        raise ValueError('upstream capture failed/incomplete/stale')
    if not (src/'filecache-equal-key-capture-01.stdout').read_bytes().strip() or (src/'filecache-equal-key-capture-01.stderr').read_bytes():
        raise ValueError('upstream output missing/error')
    v=json.loads((src/'filecache-equal-key-source-01.json').read_text())
    if v.get('exe_sha256')!=ESHA or v.get('wrapper_complete') is not True or v.get('invocation_driver_sha256')!=sha(src/'capture-filecache-equal-key.py') or v.get('driver_sha256')!=sha(src/'capture-index-path.py'):
        raise ValueError('actual capture identity/prerequisite failed')
    checked=load('equal_reviewed_annotations',src/'validate-title-source-annotations.py').validate(v)
    required=[(0x1d6a20,0x1d6a6d,'1fb87c5cf1cf0d9cc2f68b6d328a5cef161e4d3286abb179f2299f5b8f30ddb6'),
      (0x20b680,0x20b83b,'6351d3140ac8de9d876ff304797e949053c599ed62218e8075c965d1a8f20e00'),
      (0x20b5f0,0x20b675,'29fb16f493bf88ef4e7c6b860978868f153da61149d3f46355a8c6e2ec6be351'),
      (0x20b0f0,0x20b126,'b1da229162eec2af3b5d3a189ad84cf951c1b3088bf8ec9371c780e918a08ee6'),
      (0x20c300,0x20c438,'7f56074a74f27acc403c1f72c1c8a5d2538e7b889e2056d748f877b3a7918245')]
    if [(int(q['start'],16),int(q['end_exclusive'],16),q['sha256']) for q in v['ranges']]!=required:
        raise ValueError('required original body population/identity incomplete')
    ix={int(i['pc'],16):i for q in v['ranges'] for i in q['instructions']}
    def need(pc,m,args):
        if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('original operation changed '+hex(pc))
    ops=[(0x1d6a3d,'mov','ebp, ecx'),(0x1d6a3a,'mov','rsi, rdx'),(0x1d6a37,'mov','edi, r8d'),
      (0x1d6a34,'mov','ebx, r9d'),(0x1d6a3f,'call','0x20c700'),(0x1d6a47,'mov','dword ptr [rsp + 0x20], ebx'),
      (0x1d6a4b,'mov','r9d, edi'),(0x1d6a4e,'mov','r8, rsi'),(0x1d6a51,'mov','edx, ebp'),(0x1d6a53,'call','0x20b680'),
      (0x20b680,'mov','dword ptr [rsp + 0x10], edx'),(0x20b6aa,'mov','ebp, edx'),(0x20b6a7,'mov','r12, r8'),
      (0x20b6a4,'mov','r14d, r9d'),(0x20b6c8,'cmp','dword ptr [rax + 0x20], ebp'),(0x20b6cb,'jb','0x20b6d6'),
      (0x20b6d0,'mov','rax, qword ptr [rax + 8]'),(0x20b6d6,'mov','rax, qword ptr [rax]'),
      (0x20b6e3,'cmp','ebp, dword ptr [rbx + 0x20]'),(0x20b6e6,'jae','0x20b6eb'),(0x20b6f2,'je','0x20b73f'),
      (0x20b6f4,'mov','rax, qword ptr [rbx + 0x28]'),(0x20b6f8,'mov','edi, dword ptr [rax + 0x14]'),
      (0x20b6fb,'mov','rdx, qword ptr [r12]'),(0x20b702,'call','0x20b0f0'),
      (0x20b707,'mov','r8, qword ptr [rbx + 0x28]'),(0x20b70b,'mov','dword ptr [rsp + 0x28], edi'),
      (0x20b70f,'mov','eax, dword ptr [rsp + 0xa0]'),(0x20b716,'mov','dword ptr [rsp + 0x20], eax'),
      (0x20b71a,'mov','r9d, dword ptr [r8 + 8]'),(0x20b71e,'mov','r8, qword ptr [r8]'),
      (0x20b721,'mov','edx, ebp'),(0x20b726,'call','0x20c300'),(0x20b72b,'mov','rbx, rax'),
      (0x20b732,'call','0x5cd820'),(0x20b737,'mov','rax, rbx'),
      (0x20b7d0,'lea','rdx, [rsp + 0x88]'),(0x20b7e1,'mov','qword ptr [rax], rbx'),
      (0x20b607,'mov','r9d, dword ptr [rdx]'),(0x20b610,'cmp','dword ptr [r8 + 0x20], r9d'),
      (0x20b62f,'cmp','dword ptr [rdx], ecx'),(0x20b631,'jae','0x20b66c'),(0x20b633,'mov','ecx, dword ptr [rdx]'),
      (0x20b64e,'mov','dword ptr [rsp + 0x30], ecx'),(0x20b659,'mov','qword ptr [rsp + 0x38], 0'),
      (0x20b662,'call','0x1ae9b0'),(0x20b66c,'add','rax, 0x28'),
      (0x20b103,'call','qword ptr [rip + 0x6b7a47]'),(0x20b109,'neg','rax'),
      (0x20b10c,'lock xadd','qword ptr [rbx + 0x10], rax'),(0x20b11f,'jmp','qword ptr [rip + 0x6b7a22]'),
      (0x20c31f,'mov','ebp, r9d'),(0x20c322,'mov','r14, r8'),(0x20c328,'inc','dword ptr [rcx + 0x88]'),
      (0x20c32e,'mov','ecx, dword ptr [rsp + 0x78]'),(0x20c335,'mov','ebx, dword ptr [rsp + 0x70]'),
      (0x20c3fb,'mov','ecx, 0x10'),(0x20c400,'call','0x210ec0'),(0x20c40d,'je','0x20c423'),
      (0x20c412,'mov','r8d, ebp'),(0x20c415,'mov','rdx, r14'),(0x20c41b,'call','0x217a60'),(0x20c423,'xor','eax, eax')]
    for op in ops:need(*op)
    decl={x['iat_va']:x for x in v.get('static_release_imports',[])}
    if len(decl)!=2 or {a:x['name'] for a,x in decl.items()}!={'0x8c2b48':'free','0x8c2b50':'_msize'} or any(x['dll']!='api-ms-win-crt-heap-l1-1-0.dll' for x in decl.values()):
        raise ValueError('release import declaration mismatch')
    if ix[0x20b103]['memory'][0]['rip_target']!='0x8c2b50' or ix[0x20b11f]['memory'][0]['rip_target']!='0x8c2b48':raise ValueError('release import reference changed')
    gp=src/'prove_owner_reload_order.py'
    if sha(gp)!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise ValueError('reviewed CFG helper changed')
    G=load('equal_original_cfg',gp)
    graphs={}
    for lo,hi,pin in required:
        g=G.graph(ix,lo,hi,tail='qword ptr [rip + 0x6b7a22]' if lo==0x20b0f0 else None)
        graphs[hex(lo)]={'visited':sorted(g['visited']),'calls':g['calls'],'returns':g['returns'],'tails':g['tails']}
    hit=G.graph(ix,0x20b680,0x20b83b,fixed={0x20b6f2:False})
    if hit['calls']!=[(0x20b6b3,'0x5cd4f0'),(0x20b702,'0x20b0f0'),(0x20b726,'0x20c300'),(0x20b732,'0x5cd820')]:raise ValueError('equal-key local call partition changed')
    for a,b in [(0x20b6f2,0x20b702),(0x20b702,0x20b726),(0x20b726,0x20b732),(0x20b732,0x20b83a)]:
        if not G.dominates(hit,a,b):raise ValueError('equal-key event order changed')
    if 0x20b7e1 in hit['visited']:raise ValueError('new payload assignment reachable on hit')
    # No silent physical alias: both independently derived frame offsets are checked.
    frame_insert=7*8+0x40
    frame_wrapper=3*8+0x30
    if 0x88-frame_insert!=0x10 or 0xa0-frame_insert!=0x28 or 0x70-frame_wrapper!=0x28 or 0x78-frame_wrapper!=0x30:
        raise ValueError('Windows x64 stack argument identity failed')
    pins=[{'path':'filecache-equal-key-source-01.json','sha256':sha(src/'filecache-equal-key-source-01.json')}]
    r=dict(method='A STATIC_ONLY',producer_complete=True,driver_sha256=sha(Path(__file__)),exe_sha256=ESHA,
      source_pins=pins,tool_pins=[{'path':n,'sha256':sha(src/n)} for n in ['capture-index-path.py','capture-filecache-equal-key.py','validate-title-source-annotations.py','prove_owner_reload_order.py']],
      annotation_check=checked,graphs=graphs,instruction_assertions=len(ops),
      hit_partition={'calls':hit['calls'],'returns':hit['returns'],'new_payload_assignment_reachable':False},
      tree_invariant='Finite valid unsigned-key BST. Taking child0 when node<key discards only nodes<key; otherwise retain candidate and take child8, seeking least remaining node>=key. At null, sentinel or lower-bound candidate. Final incoming>=candidate selects equality because candidate>=incoming. No filename comparison participates in these local decisions. This is an induction argument over the ordered tree, not samples proving tree initialization.',
      frame_identity={'insert_frame_bytes':frame_insert,'saved_key_entry_offset':0x10,'miss_accessor_postprologue_offset':0x88,'new_mode_entry_offset':0x28,'hit_old_mode_outgoing_offset':0x28,'hit_new_mode_outgoing_offset':0x20,'wrapper_frame_bytes':frame_wrapper},
      conclusions=['001D6A20 forwards caller unsigned32 numeric key unchanged; no path normalizer/hash recomputation on this wrapper.',
        'Given existing equal numeric key, local20B680 hit branch invokes release boundary on incoming *pointer before forwarding existing payload data/length to20C300. It does not execute miss payload assignment.',
        '20B0F0 statically calls declared _msize, atomically subtracts that size at manager+10, then tailcalls declared free; actual loaded CRT/allocator behavior is unobserved.',
        '20C300 preserves supplied existing data/length in nonvolatile registers and passes them to217A60 after16-byte allocation. Allocation-null branch returns0. Native constructor effects are not established by these call arguments.',
        'Existing and requested mode remain separate stack arguments. Counter/refcount/tag/mode changes are possible; reuse is not a no-side-effects claim.'],
      premises=['finite correctly ordered map and valid initialized memory','valid incoming allocation distinct from retained payload/manager/map memory','normal ABI/callee returns and named CRT contracts','successful mutex behavior/no interfering mutation'],
      unresolved=['actual insertion caller/key-source domain completeness','natural same-key different-file collision/membership/eviction/reachability','constructor/native loaded CRT effects and lifetime/allocator placement','unbounded malformed pointers/keys/tree safety','whole OV33 E2 and runtime-built kind-FF paths'])
    out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print('CONDITIONAL ORIGINAL DATA FLOW VERIFIED; five closed CFGs; assertions='+str(len(ops))+'; no native/live executions; independent acceptance pending')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=W);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.source,a.out)
