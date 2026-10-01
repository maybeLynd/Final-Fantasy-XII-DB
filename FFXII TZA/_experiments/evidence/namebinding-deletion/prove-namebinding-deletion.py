"""Conditional local name-binding removal/completion/release rules, Method A.

Fresh result [disposable source]. Flags are masks; no native/live execution.
No assumed allocator effect or natural key-overlap/full-bank reachability.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('deletion_proof','prove-title-queue-consumption.py');S=module('deletion_roles','validate-title-source-annotations.py')

def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    d=src/'capture-namebinding-deletion.py';st=json.loads((src/'namebinding-deletion-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(d):raise ValueError('capture failed/stale')
    if not (src/'namebinding-deletion-capture-01.stdout').read_bytes().strip() or (src/'namebinding-deletion-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'namebinding-deletion-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(d):raise ValueError('capture provenance changed')
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    def read(a,n):
        for _,va,rs,ro in sec:
            if 0x120000+va<=a and a+n<=0x120000+va+rs:return b[ro+a-0x120000-va:ro+a-0x120000-va+n]
        raise ValueError('original range unbacked')
    for q in v['ranges']:
        a,z=int(q['start'],16),int(q['end_exclusive'],16)
        if bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(a,z-a):raise ValueError('reference byte identity changed')
    cfgs=[P.closed(ix,a,z) for a,z in [(0x2eaeb0,0x2eaf70),(0x2e4d20,0x2e4dfe),(0x2ea6e0,0x2ea77d),(0x2e6d60,0x2e6e25),(0x2e9360,0x2e946b)]]
    ops=[(0x2eaeb0,'movzx','r8d, byte ptr [rcx + 0x18]'),(0x2eaeb8,'test','r8b, 2'),(0x2eaebc,'jne','0x2eaecd'),
      (0x2eaebe,'test','byte ptr [rcx + 0x19], 4'),(0x2eaec2,'jne','0x2eaecd'),(0x2eaec4,'or','r8b, 4'),(0x2eaec8,'mov','byte ptr [rcx + 0x18], r8b'),(0x2eaecc,'ret',''),
      (0x2eaeeb,'add','rcx, rax'),(0x2eaef1,'cmp','dword ptr [rcx + 0x5c], eax'),(0x2eaef8,'inc','dword ptr [rdx + 0x24]'),
      (0x2eaefb,'and','r8b, 0xfd'),(0x2eaeff,'mov','word ptr [rdx + 0x26], r9w'),(0x2eaf04,'mov','byte ptr [rdx + 0x18], r8b'),
      (0x2eaf10,'mov','dword ptr [r10 + 0x5c], eax'),(0x2eaf59,'mov','qword ptr [rdx], r9'),(0x2eaf5c,'mov','qword ptr [rdx + 8], rax'),
      (0x2e4d3e,'movsxd','rdi, ecx'),(0x2e4d87,'mov','ecx, esi'),(0x2e4d89,'call','0x36d170'),
      (0x2e4d92,'test','al, 4'),(0x2e4d94,'je','0x2e4d9d'),(0x2e4d96,'or','al, 8'),(0x2e4d9b,'jmp','0x2e4db9'),
      (0x2e4db4,'call','0x41e580'),(0x2e4db9,'lea','r8, [rsp + 0x24]'),(0x2e4dbe,'mov','edx, 3'),
      (0x2e4dc3,'mov','rcx, rdi'),(0x2e4dc6,'call','0x2ea6e0'),(0x2e4dcb,'test','eax, eax'),(0x2e4dcd,'jne','0x2e4de1'),
      (0x2e4dcf,'or','byte ptr [rdi + 0x18], 2'),(0x2e4dd3,'test','byte ptr [rdi + 0x18], 4'),(0x2e4ddc,'call','0x2eaeb0'),
      (0x2ea6ef,'test','byte ptr [rcx + 0x18], 4'),(0x2ea6fc,'jne','0x2ea76b'),(0x2ea70b,'call','0x2f16b0'),
      (0x2ea744,'mov','qword ptr [rax + 0x10], rcx'),(0x2ea750,'mov','qword ptr [rax + 0x28], rdi'),
      (0x2ea75b,'mov','rbx, qword ptr [rsp + 0x30]'),(0x2ea770,'xor','eax, eax'),
      (0x2e6d6b,'test','eax, eax'),(0x2e6d6d,'jne','0x2e6e1e'),(0x2e6dac,'mov','eax, dword ptr [rdi + 0x10]'),
      (0x2e6db1,'je','0x2e6df6'),(0x2e6db3,'test','byte ptr [rdi + 0x18], 8'),(0x2e6db7,'jne','0x2e6de7'),
      (0x2e6db9,'test','byte ptr [rdi + 0x19], 4'),(0x2e6dbd,'jne','0x2e6de7'),(0x2e6ddd,'call','0x41e490'),(0x2e6dea,'call','0x2e9360'),
      (0x2e93b6,'call','0x2eafa0'),(0x2e93be,'cmp','r10d, 0x20'),(0x2e93c8,'mov','esi, 3'),(0x2e93d2,'call','0x3a0f80'),
      (0x2e93e1,'mov','ecx, dword ptr [rbx + 0x10]'),(0x2e93f0,'je','0x2e93fa'),(0x2e93f2,'call','0x369800'),
      (0x2e93f7,'mov','dword ptr [rbx + 0x10], ebp'),(0x2e944b,'inc','dword ptr [rbx + 0x24]'),
      (0x2e944e,'mov','word ptr [rbx + 0x26], bp'),(0x2e9452,'mov','byte ptr [rbx + 0x18], bpl'),(0x2e9456,'mov','dword ptr [rbx + 0x14], ebp'),
      (0x2e60ff,'mov','rsi, qword ptr [rcx + 0x28]'),(0x2e629e,'or','byte ptr [rsi + 0x18], 2'),
      (0x2e62a2,'test','byte ptr [rsi + 0x18], 4'),(0x2e62a8,'mov','rcx, rsi'),(0x2e62ab,'call','0x2eaeb0')]
    for pc,m,a in ops:P.need(ix,pc,m,a)
    # The mark-only arm terminates before any call or other memory write.
    mark=[i for pc,i in ix.items() if 0x2eaeb0<=pc<=0x2eaecc]
    writes=[(i['pc'],m['displacement']) for i in mark for m in i['memory'] if m['role'] in ['w','rw']]
    if writes!=[('0x2eaec8',0x18)] or any(i['mnemonic']=='call' for i in mark):raise ValueError('mark-only footprint changed')
    if any(i['mnemonic']=='call' for pc,i in ix.items() if 0x2eaeb0<=pc<0x2eaf70):raise ValueError('removal has an unexpected callee')
    if (ix[0x2eaed2]['mnemonic'],ix[0x2eaed2]['args'])!=('xor','r9d, r9d') or (ix[0x2e937b]['mnemonic'],ix[0x2e937b]['args'])!=('xor','ebp, ebp'):raise ValueError('generation upperword zero source changed')
    cases=[dict(flag18_mask02=f,flag19_mask04=g,removal='mark04_only' if not f and not g else 'retire_to_list') for f in [False,True] for g in [False,True]]
    generation=[dict(before=hex(x),after_inc_clear=hex(((x+1)&0xffffffff)&0xffff)) for x in [0,0xfffe,0xffff,0x1234ffff,0xffffffff]]
    result=dict(status='PRODUCER_VALID_CONDITIONAL_NAMEBINDING_DELETION_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,normal_cfgs=cfgs,removal_partition=cases,generation_boundary_controls=generation,mark_only_memory_writes=writes,
      established=[
      '2EAEB0 is a concrete setter of record+18 mask04: when18mask02=0 and19mask04=0 it writes only18|04 then returns. No call, backing release, generation advance or list unlink occurs on that arm. The record19mask04 exception bypasses this pending mark-only rule.',
      'Otherwise2EAEB0 advances generation, clears18mask02, unlinks the same record and links it to retired-list0215FD88. Matching child generation+5C is updated. INC DWORD+24 followed by zero WORD+26 leaves only (old+1)&FFFF, including rolloverFFFF->0; this is not an unbounded32-bit generation fence.',
      '2E4D20 unpins its backing before the04 decision. With04 it sets08 and skips41E580 registration. Its2EA6E0 call then takes the04 early-return0 arm, so it creates no follow-up task through that path; callback sets02 and calls2EAEB0, retiring this record. It does not free the backing itself.',
      'Without04,2EA6E0 can allocate a follow-up command with callback2E60F0 and data=record;2E4D20 sets02 only on return0. Successful continuation is a separate phase: retained prefix/tail2E60F0 establishes data->record and its reached completion tail sets02, then retires if04. Full command scheduling/secondary load reachability remains outside this slice.',
      'If2E6900(0) returns0 and the selected retired record has a nonzero handle,2E6D60 skips41E490 unregister when18mask08 or19mask04 is set, but still calls2E9360. With neither mask, it unregisters before that call. A zero-handle selected record bypasses this cleanup call locally; no universal drain guarantee is inferred.',
      'Reached2E9360 conditionally requests32 child-lane releases when generation matches, requests release of three+30 handles, calls369800 for nonzero primary+10 then zeroes+10 after normal return, releases+14 through17F040 and recycles the record. It also applies the same16-bit generation advance, clears18 and+14. Opaque callee success/allocator completion is not assumed.'],
      limitations=['Original normal-return/ABI, valid record/list/metadata and no interfering writes premises; no malformed-list safety or threading/atomicity claim',
      'Flags are masks02/04/08, not bit indices. Meaning of record19mask04 and its natural coexistence with a pending primary read are not independently established',
      'Raw completion argument is MOVSXD fromECX; low32 pointer/list comparisons are not a universal64-bit allocation-placement guarantee',
      'No actual execution/native/live timing or proof of natural equal-key competing owners/full bank; wholeOV21 and callback single-delivery/reuse remainOPEN',
      'Only local release calls/order/clears, not universal native allocator success or transitive child release; command consumer is prefix/tail, not full reachability proof',
      'Producer evidence/controls differ from independent acceptance/canonical incorporation; peer family census/fixtures are not tests run here'],
      affected_claims=['OV25 carried script-name-binding deletion-policy local rules','FABLE/OPUS external-source owner family comparison and generation width','FRONTIER OV21 ownership/lifetime preparation, actual reachability separate'],
      checker_sha256=P.sha(pathlib.Path(__file__)),required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-namebinding-deletion.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','namebinding-deletion-capture-01.status.json','namebinding-deletion-capture-01.stdout','namebinding-deletion-capture-01.stderr']],
      next_discriminator='Consume local deletion rule after independent review; if natural19mask04/pending combination or generation-cycle protection matters, trace its actual producer statically before proposing a live collector.',native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
      cleanup='Finite reference/source reads and private controls only, no game/PC/native/instrument/save/config/reference/peer changes')
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Conditional pending removal and suppressed registration/list cleanup;16-bit generation rollover, original code only')

if __name__=='__main__':main()
