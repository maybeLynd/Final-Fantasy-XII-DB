"""Source-linked local insertion versus execution, with event-path invariant.

Method A: all three branch-closed original bodies, positive physical key/call
dataflow and a finite abstract event automaton. Calls may return normally or not;
only normal-return paths are claimed. This does not execute reconstructed code.
"""
import importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
    s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('retained_normal','prove-title-queue-consumption.py');S=module('actual_annotations','validate-title-source-annotations.py')
def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [source directory]')
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    pins=[];raw,x=P.load(src,'texture-queue-tree-source-02.json',pins);agreement=S.validate(raw)
    spans={
      '0x199db0':('0x199f05','f700e2ccd2219c8c1647991bd32746c7703639ce898dc13d5946e8896b2d1f70'),
      '0x16d720':('0x16d77e','77a485db846240eb40cfbfa35bbe28e14e3e1997e1abfcacdaea36ebe80de151'),
      '0x16d840':('0x16da54','8ce5d39ffb8426db79a20e262f6f08df48f660707e51255bc170f24815f15dfc')}
    if len(raw['ranges'])!=3 or any(q['start'] not in spans or (q['end_exclusive'],q['sha256'])!=spans[q['start']] for q in raw['ranges']):raise ValueError('wrong/incomplete tree body')
    if raw.get('pdata_entries')!=[[0x199DB0,0x199F05,0x1D57E48]]:raise ValueError('wrong tree root metadata')
    if raw.get('leaves')!=[dict(start='0x16d720',end_exclusive='0x16d77e',padding='cc'*2),dict(start='0x16d840',end_exclusive='0x16da54',padding='cc'*12)]:raise ValueError('wrong helper leaf boundaries')
    if raw.get('wrapper_call')!=dict(pc='0x62ebb3',bytes='e8f8b1b6ff',target='0x199db0'):raise ValueError('wrong wrapper target')
    cfgs=[P.closed(x,int(a,16),int(b,16)) for a,(b,h) in spans.items()]
    expected_calls=[dict(pc=hex(pc),target=t) for pc,t in [(0x199E23,'0x16d720'),(0x199E70,'qword ptr [rax + 0x10]'),(0x199E8E,'0x16d840'),(0x199EB0,'qword ptr [rax + 0x10]'),(0x199ECE,'0x16d840')]]
    if cfgs[0]['calls']!=expected_calls or cfgs[1]['calls'] or cfgs[2]['calls']:raise ValueError('unexpected transitive local call boundary')
    for pc,m,a in [
      (0x199DCD,'lea','r12, [rcx + 8]'),(0x199DD1,'mov','rsi, rdx'),(0x199DD4,'mov','r15, r8'),(0x199DD7,'mov','rbp, rcx'),
      (0x199DE4,'mov','r9, qword ptr [r8]'),(0x199DF0,'cmp','r9, qword ptr [rax + 0x20]'),(0x199DF7,'setb','dl'),(0x199DFE,'jae','0x199e06'),
      (0x199E2B,'mov','rax, qword ptr [r15]'),(0x199E2E,'cmp','qword ptr [rbx + 0x20], rax'),(0x199E32,'jae','0x199edc'),
      (0x199E61,'mov','rax, qword ptr [rcx + 0x30]'),(0x199E65,'add','rcx, 0x30'),(0x199E69,'xor','r8d, r8d'),(0x199E6C,'lea','edx, [r8 + 0x28]'),
      (0x199E7C,'mov','rcx, qword ptr [r15]'),(0x199E7F,'mov','qword ptr [rax], rcx'),(0x199E85,'mov','r8, r12'),(0x199E93,'inc','dword ptr [rbp + 0x28]'),
      (0x199EA1,'mov','rax, qword ptr [rbp + 0x30]'),(0x199EA5,'lea','rcx, [rbp + 0x30]'),(0x199EA9,'xor','r8d, r8d'),(0x199EAC,'lea','edx, [r8 + 0x28]'),
      (0x199EBC,'mov','rcx, qword ptr [r15]'),(0x199EBF,'mov','qword ptr [rax], rcx'),(0x199EC5,'mov','r8, r12'),(0x199ED3,'inc','dword ptr [rbp + 0x28]'),
      (0x199E99,'mov','byte ptr [rsi + 8], 1'),(0x199ED6,'mov','byte ptr [rsi + 8], 1'),(0x199EDC,'mov','byte ptr [rsi + 8], 0'),
      (0x199EE8,'mov','rax, rsi'),(0x16D842,'mov','qword ptr [rcx + 0x10], rdx'),(0x16D846,'mov','qword ptr [rcx], rax'),(0x16D849,'mov','qword ptr [rcx + 8], rax')]:P.need(x,pc,m,a)
    # Inductive local event order, over the actual CFG, including lookup cycles.
    # Events are physical call/store sites; allocator effects remain opaque.
    events={0x199E70:'allocate',0x199EB0:'allocate',0x199E8E:'link',0x199ECE:'link',0x199E93:'increment',0x199ED3:'increment',0x199E99:'inserted',0x199ED6:'inserted',0x199EDC:'not-inserted'}
    nextstage={('start','allocate'):'allocated',('allocated','link'):'linked',('linked','increment'):'counted',('counted','inserted'):'inserted',('start','not-inserted'):'not-inserted'}
    todo=[(0x199DB0,'start')];seen=set();ends=set()
    while todo:
        pc,stage=todo.pop()
        if (pc,stage) in seen:continue
        seen.add((pc,stage));i=x[pc]
        if pc in events:
            key=(stage,events[pc])
            if key not in nextstage:raise ValueError('local insertion event-order invariant fails')
            stage=nextstage[key]
        m=i['mnemonic'];following=pc+len(bytes.fromhex(i['bytes']))
        if m=='ret':ends.add(stage);continue
        if m=='jmp':todo.append((int(i['args'],16),stage));continue
        if m.startswith('j'):todo.append((int(i['args'],16),stage))
        todo.append((following,stage))
    if ends!={'inserted','not-inserted'}:raise ValueError('missing normal insertion/duplicate return')
    result=dict(status='PRODUCER_CHECKED_POINTER_KEY_INSERTION_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisite=agreement,normal_cfgs=cfgs,normal_event_invariant=dict(states=len(seen),terminal_stages=sorted(ends),scope='Local physical insertion/count/output order, not allocator success/exception or universal tree termination'),checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),
      question='Does the verified62EB90 callee execute the embedded async object or instead maintain pointer-key storage, and which count changes locally?',
      established=[
        '199DB0 compares the unsigned pointer value loaded from inputR8 with node+20, following node+8 or node+0. Under a valid finite ordered-tree/sentinel invariant this is keyed insertion with an existing-key refusal, not a FIFO callback-pair append. The physical result is an iterator/node pointer and byte insertion flag through inputRDX; RAX returns that result address.',
        'Both normal insertion branches request28B via container+30 allocator vslot10, conditionally copy the pointer value to allocated node+20, call16D840 to link/rebalance node fields, increment DWORD[container+28], and set result+8=1. The local non-insertion branch sets result+8=0 and performs none of those insertion events. The finite event analysis checks this order across every decoded normal branch, including lookup cycles; it does not assert termination on cyclic/malformed trees.',
        'All local call targets are16D720 (node traversal),16D840 (node link/rebalance), and the two allocator-vslot10 sites. Both complete local helpers have no calls. The queued async object pointer is compared/copied as a key, never used as the direct target of a callback call in these three bodies. Opaque allocator transitive effects are excluded from this conclusion.',
        'The increment is container+28, with container supplied by62EB90 as context+38*zeroextend32(bank). It is distinct in expression and ownership premise from element+38 observed by the texture drain; this is not the missing complete writer closure for that element field.',
        'The entry makes no local control-flow test of incomingR9D. It usesR9 for the loaded key during nonempty search and resetsR9D for the link direction. An initially empty route can carry incomingR9 into the opaque allocator call, so neither its transitive relevance nor a universal unused-fourth-argument ABI is proved.'
      ],
      assumptions=['Normally returning ABI-preserving callees, correctly backed result/container/key/node storage','Valid finite unsigned-pointer-ordered tree and matching sentinel/node layout for keyed/deduplicating interpretation','Successful correctly sized nonNULL allocator result and distinct container/node/texture allocations for ordinary ownership claims; failure, alias and arithmetic-wrap cases are not sanitized by this proof'],
      unresolved=['Actual initialized container construction, slot binding, insertion caller/thread/schedule and consumption/removal','Element pendingCount+38 complete writer set and relationship to this pointer-key container','Opaque allocator/native effects, failed allocation behavior, natural title-object binding and destruction/cancellation/lifetime'],
      affected_claims=['OPUS Phyre async container ABI and container+28 versus texture-element+38','FABLE admission versus invocation and natural scheduler/lifetime premises'],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Only original file reads/source analysis; all scripts terminal; no game/control/instrument/save/config/reference/peer mutations')
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print('Pointer-key insertion/count/order established locally; async invocation and element-counter writer remain OPEN')
if __name__=='__main__':main()
