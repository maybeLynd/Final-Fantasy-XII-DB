"""Canonical drain correction from source; require real upstream receipts."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('drain_proof','prove-title-queue-consumption.py');S=module('drain_annotations','validate-title-source-annotations.py')
def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    d=src/'capture-lane-drain-correction.py';st=json.loads((src/'lane-drain-correction-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(d):raise ValueError('capture failed/stale')
    if not (src/'lane-drain-correction-capture-01.stdout').read_bytes().strip() or (src/'lane-drain-correction-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'lane-drain-correction-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(d):raise ValueError('capture provenance changed')
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    q=v['ranges'][0];a,z=int(q['start'],16),int(q['end_exclusive'],16)
    raw=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
    if raw!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('reference byte identity changed')
    cfg=P.closed(ix,0x2e6900,0x2e6a7a)
    ops=[(0x2e6908,'mov','rbx, qword ptr [rip + 0x1e79481]'),(0x2e6916,'mov','r13d, ecx'),(0x2e6950,'mov','r12, qword ptr [r15]'),
      (0x2e6960,'test','dword ptr [r15 + 0x1c], ebx'),(0x2e6966,'test','dword ptr [r15 + 0x14], ebx'),
      (0x2e698c,'call','0x41e490'),(0x2e6994,'call','0x369800'),(0x2e6999,'xor','edi, edi'),(0x2e699f,'mov','dword ptr [r14], edi'),
      (0x2e69a2,'and','dword ptr [r15 + 0x14], eax'),(0x2e69a6,'and','dword ptr [r15 + 0x1c], eax'),
      (0x2e69c7,'mov','qword ptr [rdx], rcx'),(0x2e69cf,'mov','qword ptr [rcx + 8], rdx'),
      (0x2e69d3,'mov','qword ptr [r15 + 8], rdi'),(0x2e69d7,'mov','qword ptr [r15], rdi'),
      (0x2e69ed,'mov','rbx, qword ptr [rip + 0x1e7939c]'),(0x2e69f4,'cmp','r15, rbx'),(0x2e69f7,'mov','r15, r12'),
      (0x2e69fa,'cmove','rbx, rdi'),(0x2e69fe,'mov','qword ptr [rip + 0x1e7938b], rbx'),(0x2e6a0a,'test','r13d, r13d'),(0x2e6a0d,'jne','0x2e6950'),
      (0x2e6a40,'lea','rcx, [rbx - 0x10]'),(0x2e6a48,'cmp','word ptr [rcx + 0x22], si'),(0x2e6a4c,'jge','0x2e6a68'),
      (0x2e6a4e,'call','0x2e6a80'),(0x2e6a53,'mov','rax, qword ptr [rip + 0x1e79336]'),(0x2e6a5a,'cmp','rbx, rax'),
      (0x2e6a5d,'cmove','rax, rsi'),(0x2e6a61,'mov','qword ptr [rip + 0x1e79328], rax'),(0x2e6a70,'xor','eax, eax'),(0x2e6a79,'ret','')]
    for pc,m,args in ops:P.need(ix,pc,m,args)
    if cfg['returns']!=['0x2e6a79']:raise ValueError('normal return set changed')
    terminal=[i for pc,i in sorted(ix.items()) if 0x2e6a70<pc<=0x2e6a79]
    if [(i['mnemonic'],i['args']) for i in terminal]!=[('add','rsp, 0x30'),('pop','rdi'),('pop','rsi'),('pop','rbx'),('ret','')]:raise ValueError('return register definition not preserved')
    # Enumerate complete normal CFG predecessors to RET and to its sole EAX0 definition.
    preds={a:[] for a in ix}
    for pc,i in ix.items():
        n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
        ends=[] if m=='ret' else [int(i['args'],16)] if m=='jmp' else [n,int(i['args'],16)] if m.startswith('j') else [n]
        for end in ends:
            if end in preds:preds[end].append(pc)
    post=[0x2e6a72,0x2e6a76,0x2e6a77,0x2e6a78,0x2e6a79];chain=[0x2e6a70]+post
    if any(preds[b]!=[a] for a,b in zip(chain,chain[1:])):raise ValueError('normal bypass of EAX0 definition')
    writes=[dict(pc=i['pc'],base=m['base'],displacement=m['displacement'],rip_target=m['rip_target']) for i in ix.values() for m in i['memory'] if m['role'] in ['w','rw'] and m['rip_target']=='0x215fd90']
    if [w['pc'] for w in writes]!=['0x2e69fe','0x2e6a61']:raise ValueError('queue head writer set changed')
    claim=json.loads((src/'lane-drain-correction-consumer-01.json').read_text())
    if 'the list append' not in claim.get('original_2e6900_paragraph','') or 'tail insert' not in claim['original_2e6900_paragraph']:raise ValueError('missing canonical contradiction snapshot')
    result=dict(status='PRODUCER_VALID_DRAIN_CANONICAL_CORRECTION_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,normal_cfg=cfg,normal_return=0,return_definition_chain=[hex(x) for x in chain],direct_queue_head_writes=writes,
      established=['Original2E6900 starts from sweep head0215FD90, walks to the tail, services requested AND loaded lanes, clears serviced handle/loaded/requested, unlinks the node and conditionally calls sub-record recycler. It is not the locally described node builder/list append.',
      'ModeECX0 limits the first reverse walk to one node; nonzero continues while previous exists. A later pass calls2E6A80 only for records with negative node index. These are distinct local phases, not a once-per-frame or always-full-drain guarantee.',
      'The only direct queue-head writes preserve current head or set it0 when the removed node was that head, after the relevant helper. They do not locally insert a new node. Opaque callees can have effects outside this local footprint.',
      'Every normal return is dominated by XOR EAX,EAX at2E6A70; following stack restoration does not write EAX. Thus the shipping function returns0 normally for either mode. Exceptions, ABI violations or nontermination are not normal-return counterexamples.',
      'Current frame contract2E6900 paragraph describes a list append/build/tail insert and requires semantic correction. Its2E6A80 no-flags wording also needs exact loaded+24|mask28, not all masks/pending, under separately retained lane source.'],
      consumer_snapshot_sha256=P.sha(src/'lane-drain-correction-consumer-01.json'),
      affected_claims=['00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md2E6900 and2E6A80 paragraphs','Name-binding drain return0 guard in prior scoped ASTRA package','FABLE/OPUS original scheduling and list operation classification'],
      limitations=['Valid lists/state, normal ABI/returns and no interfering writes; local code not global allocator/IO effects','No actual frame schedule, natural outstanding IO, callback delivery or full-drain progress proof','2E6A80 mask qualification reuses prior source result pending independent review, not a new native run','Producer and invocation checks are not independent acceptance or canonical repair'],
      checker_sha256=P.sha(pathlib.Path(__file__)),required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-lane-drain-correction.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','lane-drain-correction-consumer-01.json','lane-drain-correction-capture-01.status.json','lane-drain-correction-capture-01.stdout','lane-drain-correction-capture-01.stderr']],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
      next_discriminator='Owner correction and independent primary review; original caller/service guarantees remain open, do not turn return0 into proof of completed IO',cleanup='Finite original reference/current consumer reads and private source controls only')
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Original2E6900 is a local drain/unlink, not append; all normal returns0')
if __name__=='__main__':main()
