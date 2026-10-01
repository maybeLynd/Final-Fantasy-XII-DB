"""Focused original local CFG partition; no native/live state supplied."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
UPSTREAM=ROOT/'Database/FFXII TZA/_experiments/evidence/bts-index-binding'
UPSHA='c57c6b668c5b567014a01c5da45dcbf7899645e4547a6bc310edce0972891abb'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def graph(ix,lo,hi,fixed=None,tail=None,fatal=()):
    todo=[lo];seen=set();edges={};calls=[];returns=[];tails=[]
    while todo:
        pc=todo.pop()
        if pc in seen:continue
        if pc not in ix or not lo<=pc<hi:raise ValueError('unclosed local CFG '+hex(pc))
        seen.add(pc);i=ix[pc];n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
        if m=='ret':returns.append(pc);succ=[]
        elif pc in fatal:
            if (m,i['args'])!=('call','0x809728'):raise ValueError('fatal boundary changed')
            succ=[]
        elif m=='jmp' and i['args']==tail:tails.append(pc);succ=[]
        elif m=='jmp':succ=[int(i['args'],16)]
        elif m.startswith('j'):
            t=int(i['args'],16)
            succ=[t if fixed[pc] else n] if fixed and pc in fixed else [t,n]
        elif m=='int3':raise ValueError('unexpected trap')
        else:
            succ=[n]
            if m=='call':calls.append((pc,i['args']))
        edges[pc]=succ;todo.extend(succ)
    return dict(entry=lo,visited=seen,edges=edges,calls=sorted(calls),returns=sorted(returns),tails=tails)


def dominates(g,a,b):
    if a not in g['visited'] or b not in g['visited']:raise ValueError('missing domination boundary')
    todo=[g['entry']];seen=set()
    while todo:
        p=todo.pop()
        if p==a or p in seen:continue
        if p==b:return False
        seen.add(p);todo.extend(g['edges'][p])
    return True


def main(out,src,upstream):
    if out.exists():raise ValueError('immutable result exists')
    spec=importlib.util.spec_from_file_location('reload_reviewed_roles',src/'validate-title-source-annotations.py')
    roles=importlib.util.module_from_spec(spec);spec.loader.exec_module(roles)
    raw=[];receipts=[]
    for prefix,driver,source in [('owner-reload-order-capture-01','capture-owner-reload-order.py','owner-reload-order-source-01.json'),
                                 ('owner-reload-gate-capture-01','capture-owner-reload-gate.py','owner-reload-gate-source-01.json')]:
        status=json.loads((src/(prefix+'.status.json')).read_text())
        if status['exit']!=0 or status['driver_sha256']!=sha(src/driver):raise ValueError('required capture failed/stale')
        if not(src/(prefix+'.stdout')).read_bytes().strip() or (src/(prefix+'.stderr')).read_bytes():raise ValueError('capture missing/error output')
        v=json.loads((src/source).read_text());roles.validate(v)
        if v.get('driver_sha256')!=sha(src/driver):raise ValueError('capture driver changed')
        raw.append(v)
        receipts.extend(dict(path=p,sha256=sha(src/p)) for p in [driver,source,prefix+'.status.json',prefix+'.stdout',prefix+'.stderr'])
    if sha(upstream/'manifest.json')!=UPSHA:raise ValueError('retained manifest changed')
    manifest=json.loads((upstream/'manifest.json').read_text())
    member=next(m for m in manifest['members'] if m['path']=='index-path-raw-02.json')
    path=upstream/member['path']
    if sha(path)!=member['sha256']:raise ValueError('retained caller source changed')
    retained=json.loads(path.read_text());roles.validate(retained)
    q=next(q for q in retained['ranges'] if q['start']=='0x32fca0')
    if (q['end_exclusive'],q['sha256'])!=('0x330048','1d796bf176912574660eedaa1919235222d3a34b66f6492014cae31b3884f9f7'):
        raise ValueError('retained caller range changed')
    ranges=[q]+[r for v in raw for r in v['ranges']]
    required=[(0x32fca0,0x330048),(0x2628b0,0x262f49),(0x330310,0x330497),
              (0x3304a0,0x3306da),(0x32f850,0x32fa09),(0x3603c0,0x3603c8)]
    if [(int(r['start'],16),int(r['end_exclusive'],16)) for r in ranges]!=required:
        raise ValueError('required range population missing/changed')
    data=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(data).hexdigest()!=SHA:raise ValueError('wrong original image')
    pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0]
    secs=[struct.unpack_from('<IIII',data,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
    def read(a,n):
        for vs,rva,size,offset in secs:
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:return data[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
        raise ValueError('unbacked original range')
    for r in ranges:
        lo=int(r['start'],16);hi=int(r['end_exclusive'],16)
        if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(lo,hi-lo):raise ValueError('original byte mismatch')
    ix={int(i['pc'],16):i for r in ranges for i in r['instructions']}
    def need(pc,m,args):
        if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('operation changed '+hex(pc))
    ops=[(0x32fcf4,'mov','ecx, edi'),(0x32fcf6,'call','0x2628b0'),(0x32fcfd,'call','0x32ed80'),
      (0x330030,'call','0x330310'),(0x32ff0b,'call','0x32e620'),
      (0x2628d3,'movsxd','rdi, ecx'),(0x2628e4,'mov','esi, 1'),
      (0x2628ec,'test','ecx, ecx'),(0x2628ee,'je','0x262905'),(0x2628f0,'cmp','edi, 3'),(0x2628f3,'jne','0x26292a'),
      (0x26292c,'test','byte ptr [rbx + 0x10], sil'),(0x262930,'je','0x262d96'),
      (0x262980,'mov','ecx, edi'),(0x262982,'call','0x3dd380'),
      (0x2629ba,'test','edi, edi'),(0x2629bc,'je','0x262a03'),(0x2629be,'jle','0x262d25'),
      (0x2629c4,'cmp','edi, 2'),(0x2629c7,'jle','0x2629dc'),(0x2629c9,'cmp','edi, 3'),(0x2629cc,'jne','0x262d25'),
      (0x262a87,'call','0x3603c0'),(0x262a8c,'test','eax, eax'),(0x262a8e,'je','0x262b38'),
      (0x262af0,'xor','ecx, ecx'),(0x262af2,'call','0x32e520'),
      (0x262b0b,'xor','ecx, ecx'),(0x262b0d,'call','0x32e520'),
      (0x262b1c,'xor','ecx, ecx'),(0x262b1e,'call','0x32e520'),
      (0x262d2c,'cmp','edi, 4'),(0x262d2f,'je','0x262d96'),(0x262d3e,'test','edi, edi'),(0x262d40,'je','0x262d8f'),
      (0x3603c0,'movsx','eax, byte ptr [rip + 0x1f6b35f]'),(0x3603c7,'ret',''),
      (0x3303bf,'mov','ebx, r15d'),(0x3303c2,'or','ebx, r14d'),
      (0x330417,'mov','dword ptr [rsp + 0x38], ebx'),(0x33041b,'lea','rax, [rip + 0x7e]'),
      (0x330426,'mov','qword ptr [rsp + 0x40], rax'),(0x330433,'mov','qword ptr [rsp + 0x48], rcx'),
      (0x33043b,'mov','qword ptr [rsp + 0x20], rax'),(0x330444,'call','0x32e620'),
      (0x330404,'mov','rcx, r15'),(0x330407,'call','0x861eba'),(0x33040c,'mov','ecx, ebx'),(0x33040e,'call','0x3304a0'),
      (0x3304b5,'mov','ebx, ecx'),(0x3304bc,'mov','edi, ebx'),(0x3304c5,'and','ebx, 0xf'),
      (0x3304c8,'mov','eax, 0xfffffff0'),(0x3304d9,'and','rdi, rax'),
      (0x3304f9,'test','rdi, rdi'),(0x3304fc,'je','0x33056a'),(0x3304fe,'cmp','dword ptr [rdi + 4], 0'),
      (0x330502,'jbe','0x330519'),(0x330504,'mov','eax, dword ptr [rdi + 0x10]'),(0x330507,'test','eax, eax'),
      (0x330509,'je','0x330519'),(0x33050b,'add','rax, rdi'),(0x33050e,'je','0x330519'),
      (0x330510,'or','eax, ebx'),(0x330512,'mov','ecx, eax'),(0x330514,'call','0x32f850'),
      (0x32f860,'mov','edi, ecx'),(0x32f869,'and','ecx, 0xf'),(0x32f86c,'mov','eax, 0xfffffff0'),
      (0x32f871,'and','rdi, rax'),(0x32f87e,'cmp','byte ptr [rdi], 0'),(0x32f881,'jne','0x32f8a7'),
      (0x32f961,'mov','rdx, rdi'),(0x32f964,'mov','ecx, ebx'),(0x32f966,'call','0x26c8c0')]
    for op in ops:need(*op)
    if ix[0x3603c0]['memory'][0]['rip_target']!='0x22cb726' or ix[0x33041b]['memory'][0]['rip_target']!='0x3304a0':raise ValueError('gate/callback identity changed')
    writes=[(i['pc'],i['mnemonic'],i['args']) for r in ranges if r['start']=='0x2628b0' for i in r['instructions']
            if i['args'].split(', ')[0] in ['edi','rdi','esi','rsi'] and i['mnemonic'] not in ['cmp','test','push']]
    if writes!=[('0x2628d3','movsxd','rdi, ecx'),('0x2628e4','mov','esi, 1'),
                ('0x262f3e','mov','rsi, qword ptr [rsp + 0x78]'),('0x262f47','pop','rdi')]:raise ValueError('group/flag provenance changed')
    full=graph(ix,0x2628b0,0x262f49)
    waits=[pc for pc,target in full['calls'] if target=='0x32e520']
    if waits!=[0x262af2,0x262b0d,0x262b1e]:raise ValueError('named wait call population changed')
    rows=[]
    for group in range(5):
        for live in [False,True]:
            for gate in ([False,True] if group==0 and live else [None]):
                fixed={0x2628ee:group==0,0x2628f3:group!=3,0x262930:not live,
                       0x2629bc:group==0,0x2629be:group<=0,0x2629c7:group<=2,0x2629cc:group!=3,
                       0x262d2f:group==4,0x262d40:group==0}
                if gate is not None:fixed[0x262a8e]=not gate
                g=graph(ix,0x2628b0,0x262f49,fixed=fixed)
                found=[pc for pc,target in g['calls'] if target=='0x32e520']
                expected=waits if group==0 and live and gate else []
                if found!=expected or g['returns']!=[0x262f48]:raise ValueError('local partition changed')
                deleted=0x262982 in g['visited']
                if deleted!=live:raise ValueError('delete/live partition changed')
                for pc in found:
                    if not dominates(g,0x262982,pc) or not dominates(g,pc,0x262f48):raise ValueError('delete/wait order not obligatory on normal return')
                rows.append(dict(group=group,live_gate=live,byte_gate_nonzero=gate,owner_delete_site=deleted,
                                 named_waits=[hex(pc) for pc in found],visited_instructions=len(g['visited']),normal_return=True))
    caller=graph(ix,0x32fca0,0x330048,tail='0x36c140')
    for pc in [0x32fcfd,0x32ff0b,0x330030]:
        if not dominates(caller,0x32fcf6,pc):raise ValueError('unload precursor not dominant')
    primary=graph(ix,0x330310,0x330497)
    dispatch=graph(ix,0x3304a0,0x3306da)
    definition=graph(ix,0x32f850,0x32fa09,fatal=(0x32fa04,))
    if not dominates(definition,0x32f881,0x32f966):raise ValueError('definition header gate not dominant')
    if not dominates(dispatch,0x3304fe,0x330514):raise ValueError('section count gate not dominant')
    result=dict(status='PRODUCER_VALID_CONDITIONAL_RELOAD_ORDER_INDEPENDENT_PENDING',method='A STATIC_ONLY',
      exe_sha256=SHA,driver_sha256=sha(Path(__file__)),source_pins=receipts,
      retained_dependency=dict(path=str(upstream.relative_to(ROOT)) if upstream.is_relative_to(ROOT) else str(upstream),manifest_sha256=UPSHA,member=member),
      partition=rows,gate=dict(address='0x22cb726',width=1,load='MOVSX EAX,BYTE;RET',timing='value when3603C0 executes, not assumed entry value'),
      established=['Retained32FCA0 normal local CFG unload2628B0 precedes its reset32ED80, auxiliary request32FF0B and primary330310 entry. This existing caller evidence is reused, not a new allcaller census.',
        'In2628B0, the named3DD380 group deletion site is selected by the observed slot live-bit gate. All three named32E520(0) waits are reachable only for group0/live and nonzero3603C0 byte gate; on any normal return in that partition deletion precedes all three waits.',
        'The other ten equivalent group/live/gate partitions have no named local32E520 site, including live group0 with gate zero. A universal local unload-drain premise is refuted. Unobserved opaque/transitive callbacks may still wait or submit elsewhere.',
        '330310 normal positive-size primary path stages callback3304A0 and packed low32 allocation pointer OR group in descriptor+8; D4/nonNULL override instead copies then directly invokes3304A0. Queue admission/IO/callback scheduling remain separate.',
        '3304A0 conditionally dispatches section+10 through32F850, not the incoming destination argument. Count>0, nonzero offset and nonzero pointer sum gate it; low32 pointer/tag packing is preserved.32F850 binds through26C8C0 only on a nonzero first section byte and a selected supported arena branch. Binder reset3DD790 remains the prior conditional original body result.'],
      limits=['Local CFG includes opaque normally returning direct and indirect callees; normal ABI preserves group registers. No transitive pump/drain absence, EH/unwind, concurrency, reentry or natural entry closure.',
        'Branch partitions concern values at actual tests, not portable constructor defaults, stable entry live-bit or byte gate. No assertion any synthetic combination occurs naturally.',
        'Callback code proves behavior IF reached; allocation success, queue descriptor consumption, initialized resources, tag alignment/low-address validity, callback timing and reset-versus-pending-request lifetime remain separate.',
        'Prior SECTION09 controlled machine-code results, GR17 reviewer/census and bts retained sources are dependencies/corroboration, not new runs or automatic semantic acceptance.',
        'Eleven bounded CFG partitions are static computations, not machine-code experiments. No whole OV19/21 closure or safe reload award.'],
      affected_claims=['FABLE indexed owner/reset caller ordering and explicit reload barrier preconditions','OPUS persistent owner lifetime and ActorManagerSlot/payload callback contract'],
      next_discriminator='Trace/prove whether queued indexed-owner requests can remain for the same group when this gated reload reaches3DD790. First reuse original32ED80 and accepted callback-delivery/cancellation/producer evidence; no absence-sampling or gameplay just for local branches.',
      native_runs=0,live_runs=0,whole_runtime_rows_closed=0,cleanup='Read-only sources/disposable controls; no process/game/save/configuration/reference writes')
    out.write_text(json.dumps(result,indent=2)+'\n');print('CONDITIONAL_RELOAD_ORDER:11 static partitions; local waits require live group0 AND nonzero byte gate; lifetime remains OPEN')


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else HERE,Path(sys.argv[3]) if len(sys.argv)>3 else UPSTREAM)
