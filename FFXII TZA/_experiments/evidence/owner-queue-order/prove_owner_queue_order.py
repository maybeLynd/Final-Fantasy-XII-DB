"""Conditional FIFO source proof. No FF12 code is executed by this reducer.

The list lemma is over arbitrary finite valid lists, not a sample census.
Opaque calls are explicitly constrained by the noninterference premises.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
ESHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
VSHA='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def graph(ix,entry,end,table=None,tail=None):
    todo=[entry];seen=set();edges={};calls=[];returns=[];tails=[]
    while todo:
        pc=todo.pop()
        if pc in seen:continue
        if pc not in ix or not entry<=pc<end:raise ValueError('unclosed local CFG '+hex(pc))
        seen.add(pc);i=ix[pc];m=i['mnemonic'];n=pc+len(bytes.fromhex(i['bytes']))
        if m=='ret':returns.append(pc);successors=[]
        elif m=='jmp' and i['args']==tail:tails.append(pc);successors=[]
        elif m=='jmp' and pc==0x32e0bb:
            if not table or i['args']!='rcx':raise ValueError('missing verified computed jump')
            successors=list(dict.fromkeys(table))
        elif m=='jmp':successors=[int(i['args'],16)]
        elif m.startswith('j'):successors=[int(i['args'],16),n]
        elif m=='int3':raise ValueError('unexpected trap')
        else:
            successors=[n]
            if m=='call':calls.append((pc,i['args']))
        edges[pc]=successors;todo.extend(successors)
    return dict(entry=entry,visited=seen,edges=edges,calls=sorted(calls),returns=sorted(returns),tails=tails)


def dominates(g,a,b):
    if a not in g['visited'] or b not in g['visited']:raise ValueError('missing domination boundary')
    todo=[g['entry']];seen=set()
    while todo:
        pc=todo.pop()
        if pc==a or pc in seen:continue
        if pc==b:return False
        seen.add(pc);todo.extend(g['edges'][pc])
    return True


def main(out,src):
    if out.exists():raise ValueError('immutable result exists')
    if sha(src/'validate-title-source-annotations.py')!=VSHA:raise ValueError('reviewed validator changed')
    spec=importlib.util.spec_from_file_location('queue_reviewed_annotations',src/'validate-title-source-annotations.py')
    roles=importlib.util.module_from_spec(spec);spec.loader.exec_module(roles)
    status=json.loads((src/'owner-queue-order-source-run-02.status.json').read_text())
    driver=src/'qualify_owner_queue_order_source.py'
    if status['exit']!=0 or status['driver_sha256']!=sha(driver):raise ValueError('required qualifier failed/stale')
    if not(src/'owner-queue-order-source-run-02.stdout').read_bytes().strip() or (src/'owner-queue-order-source-run-02.stderr').read_bytes():
        raise ValueError('qualifier missing/error output')
    v=json.loads((src/'owner-queue-order-source-02.json').read_text())
    if v['driver_sha256']!=sha(driver) or v['exe_sha256']!=ESHA:raise ValueError('qualifier identity changed')
    annotation_receipt=roles.validate(v)
    dependency=ROOT/v['dependency']['path']
    if (sha(dependency/'original_body_manifest.json'),sha(dependency/'original_disassembly.txt'))!=(
        '23785132366d8f1464b42ccfec0e1d9d4cbec05a04d733b212270f867a7e9de8',
        '9cb269e7008618d928cb575d5f65a05c544b56da14ac031ffe972182aa0a7304'):
        raise ValueError('retained dependency changed')
    mm=json.loads((dependency/'original_body_manifest.json').read_text())
    required=[(0x32e620,0x32e774),(0x32e870,0x32e98d),(0x32e990,0x32ea4a),
              (0x32ec40,0x32ecd3),(0x32e070,0x32e2cd),(0x32e330,0x32e36b),(0x16d6a0,0x16d6a3)]
    if [(int(r['start'],16),int(r['end_exclusive'],16)) for r in v['ranges']]!=required:
        raise ValueError('required range population missing/changed')
    data=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(data).hexdigest()!=ESHA:raise ValueError('wrong original image')
    pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0]
    secs=[struct.unpack_from('<IIII',data,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
    def read(a,n):
        for vs,rva,size,offset in secs:
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:return data[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
        raise ValueError('unbacked original range')
    for r,(entry,end) in zip(v['ranges'],required):
        f=next(f for f in mm['functions'] if int(f['entry'],16)==entry)
        if r['sha256']!=f['sha256']:raise ValueError('retained original body hash changed')
        if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(entry,end-entry):
            raise ValueError('original byte mismatch')
    table=v.get('table')
    if not table:raise ValueError('required pump table missing')
    blob=read(0x32e2d0,24);targets=[0x120000+struct.unpack_from('<I',blob,4*k)[0] for k in range(6)]
    if (table['address'],table['bytes'],table['sha256'],table['targets'])!=(
        '0x32e2d0',blob.hex(),hashlib.sha256(blob).hexdigest(),[hex(t) for t in targets]):
        raise ValueError('original pump table identity changed')
    ix={int(i['pc'],16):i for r in v['ranges'] for i in r['instructions']}
    def need(pc,m,args):
        if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('operation changed '+hex(pc))
    for op in [(0x32e6b9,'mov','dword ptr [rsp + 0x28], 1'),(0x32e742,'mov','dword ptr [rsp + 0x28], 1'),
      (0x32e87f,'push','rdi'),(0x32e880,'push','r12'),(0x32e882,'push','r14'),(0x32e884,'sub','rsp, 0x20'),
      (0x32e8c5,'mov','ecx, dword ptr [rsp + 0x68]'),(0x32e8c9,'call','0x32e990'),
      (0x32e99a,'mov','r9d, ecx'),(0x32e9e6,'test','r9d, r9d'),(0x32e9e9,'jne','0x32ea1a'),
      (0x32ea3a,'mov','qword ptr [rax + 0x10], rdx'),(0x32ea3e,'mov','qword ptr [rdx + 0x18], rax'),
      (0x32ea45,'mov','qword ptr [rdx + 0x10], r8'),(0x32e997,'xor','r8d, r8d'),
      (0x32ec40,'mov','r8, qword ptr [rcx + 0x18]'),(0x32ec44,'mov','rdx, qword ptr [rcx + 0x10]'),
      (0x32ec52,'cmove','rax, rdx'),(0x32ec67,'cmove','rax, r8'),
      (0x32ec77,'mov','qword ptr [r8 + 0x10], rdx'),(0x32ec84,'mov','qword ptr [rax + 0x18], r8'),
      (0x32ecce,'jmp','0x16d6a0'),(0x16d6a0,'ret','0'),
      (0x32e090,'mov','rbx, qword ptr [rip + 0x1f97129]'),(0x32e0a0,'movzx','eax, byte ptr [rbx + 0x20]'),
      (0x32e0a4,'dec','eax'),(0x32e0a6,'cmp','eax, 5'),(0x32e0a9,'ja','0x32e2a0'),
      (0x32e0b1,'mov','ecx, dword ptr [rdi + rax*4 + 0x20e2d0]'),(0x32e0b8,'add','rcx, rdi'),
      (0x32e336,'mov','rax, qword ptr [rcx + 0x40]'),(0x32e33a,'mov','rbx, rcx'),
      (0x32e342,'mov','rdx, qword ptr [rcx + 0x70]'),(0x32e346,'mov','r8d, 1'),
      (0x32e34c,'mov','ecx, dword ptr [rcx + 0x60]'),(0x32e34f,'call','rax')]:need(*op)
    for pc,target in [(0x32e990,0x22c51d0),(0x32e9ae,0x22c51c0),(0x32ea1a,0x22c51c8),
                      (0x32ea21,0x22c51c8),(0x32ec59,0x22c51c0),(0x32ec6b,0x22c51c8),
                      (0x32ecbe,0x22c51d0),(0x32e090,0x22c51c0),(0x32e07a,0x120000)]:
        if ix[pc]['memory'][0]['rip_target']!=hex(target):raise ValueError('queue object identity changed')
    requester=graph(ix,0x32e620,0x32e774)
    sites=[pc for pc,target in requester['calls'] if target=='0x32e870']
    if sites!=[0x32e6dd,0x32e759]:raise ValueError('requester call population changed')
    writes=[int(i['pc'],16) for i in v['ranges'][0]['instructions'] for m in i['memory']
            if m['base']=='rsp' and m['role'] in ['w','rw'] and m['displacement']<0x2c and m['displacement']+m['size']>0x28]
    if writes!=[0x32e6b9,0x32e742]:raise ValueError('tail argument overwritten')
    for flag,call in zip(writes,sites):
        if not dominates(requester,flag,call):raise ValueError('tail flag not obligatory')
    receiver=graph(ix,0x32e870,0x32e98d)
    if not dominates(receiver,0x32e8c5,0x32e8c9):raise ValueError('tail argument forwarding not obligatory')
    # Receiver stack delta =3 pushes(24)+SUB32; [active RSP+104] = entry+48.
    if 3*8+0x20!=0x68-0x30:raise ValueError('sixth ABI argument changed')
    insert=graph(ix,0x32e990,0x32ea4a)
    remove=graph(ix,0x32ec40,0x32ecd3,tail='0x16d6a0')
    pump=graph(ix,0x32e070,0x32e2cd,table=targets)
    callback=graph(ix,0x32e330,0x32e36b,tail='0x3697f0')
    # Complete selected bodies plus exact hashes qualify all link updates,
    # including redundant removals and empty-list insertion. No hidden local calls.
    if insert['calls'] or remove['calls'] or remove['tails']!=[0x32ecce]:raise ValueError('queue primitive opaque effect changed')
    if pump['returns']!=[0x32e2cc] or requester['returns']!=[0x32e773]:raise ValueError('normal boundary changed')
    defs=[i['pc'] for i in v['ranges'][4]['instructions'] if i['args'].split(', ')[0] in ['rbx','ebx','bl','bh']
          and i['mnemonic'] not in ['cmp','test','push','nop']]
    if defs!=['0x32e090','0x32e2c2']:raise ValueError('selected slot register redefined')
    if any(m['role'] in ['w','rw'] and m['rip_target']=='0x22c51c0' for i in v['ranges'][4]['instructions'] for m in i['memory']):
        raise ValueError('pump directly permutes queue head')
    completion=[pc for pc,t in pump['calls'] if t=='0x32e330']
    retirement=[pc for pc,t in pump['calls'] if t=='0x32ec40']
    if completion!=[0x32e133,0x32e1fa,0x32e26f] or retirement!=[0x32e13f,0x32e192,0x32e1e3,0x32e27b,0x32e291]:
        raise ValueError('completion/retirement population changed')
    for pc in completion+retirement:
        if not dominates(pump,0x32e090,pc):raise ValueError('head selection not dominant')
    # Propagate the actual RCX argument on the local CFG. Opaque calls clobber
    # volatile RCX; a dominating MOV alone would not establish this provenance.
    todo=[(pump['entry'],False)];seen=set();checked=set()
    while todo:
        pc,is_head=todo.pop()
        if (pc,is_head) in seen:continue
        seen.add((pc,is_head));i=ix[pc]
        if pc in completion+retirement:
            if not is_head:raise ValueError('completion/retirement argument not current head '+hex(pc))
            checked.add(pc)
        if i['mnemonic']=='call':is_head=False
        elif i['args'].split(', ')[0] in ['rcx','ecx','cl','ch'] and i['mnemonic'] not in ['cmp','test','push','jmp']:
            is_head=(i['mnemonic'],i['args'])==('mov','rcx, rbx')
        todo.extend((successor,is_head) for successor in pump['edges'][pc])
    if checked!=set(completion+retirement):raise ValueError('missing head argument checks')
    if callback['calls']!=[(0x32e34f,'rax')]:raise ValueError('completion callback population changed')
    controls=[dict(kind='algebraic illustration, not native execution',before=['A','X'],operation='append primary B',after=['A','X','B'],older_precedes_primary=True),
              dict(kind='counterexample to unsupported head-primary extension',before=['A','X'],operation='prepend primary B',after=['B','A','X'],older_precedes_primary=False),
              dict(kind='retirement removes antecedent, not proof of success',before=['A','B'],operation='remove A',after=['B'],older_still_pending=False)]
    if not (controls[0]['after'].index('A')<controls[0]['after'].index('B')) or not (controls[1]['after'].index('B')<controls[1]['after'].index('A')) or 'A' in controls[2]['after']:
        raise ValueError('scope controls failed')
    theorem=dict(antecedent='Distinct request tokens A and B coexist in one valid finite pending list; A was pending before accepted normal tail insertion of B.',
      representation='L = P ++ [A] ++ Q ++ [B] ++ R, arbitrary finite P,Q,R with distinct tokens and disjoint free list.',
      induction=['Base: appending B places every existing token, including A, before B.',
        'Prepending or appending a different fresh token adds a prefix or suffix; the relative order of A and B is unchanged.',
        'Removing any token other than A/B deletes from P,Q,R; A before B is unchanged.',
        'Removing A or B makes the coexistence antecedent false; reusing a physical slot is a different token and is outside unchanged-identity premises.',
        'The selected head cannot be B while A still precedes it.32E070 selects only head; its completion helper receives that head slot and reads that slot callback+40/data+60/destination+70.'],
      conclusion='Under the stated transitions/premises, B completion callback cannot be invoked by this pump while older A remains pending. A must have retired, possibly by cancellation/error, before B delivery.')
    result=dict(status='PRODUCER_VALID_CONDITIONAL_QUEUE_ORDER_INDEPENDENT_PENDING',method='A RETAINED_ORIGINAL_SOURCE_AND_LIST_INVARIANT',
      driver_sha256=sha(Path(__file__)),exe_sha256=ESHA,source_sha256=sha(src/'owner-queue-order-source-02.json'),
      qualifier_sha256=sha(driver),annotation_receipt=annotation_receipt,dependency=v['dependency'],table=table,
      graphs=[dict(entry=hex(g['entry']),instructions=len(g['visited']),calls=[dict(pc=hex(pc),target=t) for pc,t in g['calls']],
                   returns=[hex(pc) for pc in g['returns']],tails=[hex(pc) for pc in g['tails']]) for g in [requester,receiver,insert,remove,pump,callback]],
      theorem=theorem,controls=controls,source_boundaries=dict(tail_flags=[hex(x) for x in writes],completion_sites=[hex(x) for x in completion],retirement_sites=[hex(x) for x in retirement]),
      established=['Both local32E620 request arms pass sixth atTail=1 to32E870, which forwards it to32E990. Nonzero insertion appends to valid pending tail.',
        '32EC40 locally unlinks the selected node, preserves other-node order and puts it on the free list; its shipping tail16D6A0 is RET0.',
        '32E070 services the current pending head, never locally advances RBX to next. Non-progress may retain/revisit head or return; no fairness/deadline is established.',
        'An older request already pending before an accepted ordinary queued primary cannot be overtaken under the explicit valid-list/noninterference premises. This narrows the reset/pending countermodel for that antecedent without proving global uniqueness.'],
      limits=['Static conditional proof and three illustrative algebraic controls; zero new native/live executions. Retained SECTION09 native fixtures remain their prior bounded evidence, not rerun or enlarged.',
        'Normal ABI/valid accessible nonaliasing queue storage and stable sixth stack argument; no recursive pump, concurrent corruption, queue reset/permutation, opaque call that bypasses these transitions, or ABA identity confusion.',
        'Full-pool32E870 may pump before insertion/acceptance. No universal deferred scheduling or successful IO is inferred.',
        'Only requests already pending before B enqueue are covered. Later owner submissions, head-inserted primary32E780 and synchronous D4 direct3304A0/world-reset paths are outside this proof.',
        'Retirement may be cancellation/error, not successful owner completion. No initialized scene, producer-disable invariant, natural caller census, pointer lifetime, allocator placement or safe reload/whole OV19/21 closure.',
        'Non-atomic instruction transitions require stated noninterference; source-local callback association does not establish all callback effects. Independent SPEC and FABLE/OPUS canonical consumption remain pending.'],
      affected_claims=['Owner reload/reset pending-request exclusion for already-pending requests on normal queued primary path','OV36 global owner-uniqueness sufficiency premise; retain valid per-slot delivery and admission-only scope'],
      next_discriminator='Original32ED80 disable interval and32F850 re-enable-before-bind: can later owner work be submitted before queued-primary reset? D4 synchronous override lacks FIFO antecedent; retain independent world-reset bounds.',
      native_runs=0,live_runs=0,whole_runtime_rows_closed=0,cleanup='All read-only original/retained inputs; no game/process/save/config/reference writes; finite children terminal')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('CONDITIONAL_QUEUE_ORDER: old-before-tail-primary invariant; direct/later submissions and natural uniqueness OPEN; native/game0')


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else HERE)
