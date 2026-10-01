"""Method A: specific conditional drain before persistent owner reset.
Fresh result [disposable source]. No native/live execution or all-caller claim.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Database').is_dir())
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
UPSTREAM=ROOT/'Database/FFXII TZA/_experiments/evidence/bts-index-binding'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    return value


def graph(ix,lo,hi,terminal_tail=None,fatal_calls=()):
    todo=[lo];seen=set();edges={};calls=[];tails=[];returns=[]
    while todo:
        pc=todo.pop()
        if pc in seen:continue
        if pc not in ix or not lo<=pc<hi:raise ValueError('unclosed original local CFG '+hex(pc))
        seen.add(pc);i=ix[pc];n=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic'];succ=[]
        if m=='ret':returns.append(pc)
        elif pc in fatal_calls:
            if m!='call' or i['args']!='0x809728':raise ValueError('explicit fatal boundary changed')
        elif m=='jmp' and i['args']==terminal_tail:tails.append(pc)
        elif m=='jmp':succ=[int(i['args'],16)]
        elif m.startswith('j'):succ=[int(i['args'],16),n]
        elif m=='int3':raise ValueError('unexpected trap in normal path')
        else:
            succ=[n]
            if m=='call':calls.append(dict(pc=hex(pc),target=i['args']))
        edges[pc]=succ;todo.extend(succ)
    return dict(entry=lo,visited=seen,edges=edges,calls=sorted(calls,key=lambda x:int(x['pc'],16)),
                tails=tails,returns=returns,fatal_boundaries=list(fatal_calls))


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
    status=json.loads((src/'owner-reset-barrier-capture-01.status.json').read_text())
    if status['exit']!=0 or status['driver_sha256']!=sha(src/'capture-owner-reset-barrier.py'):
        raise ValueError('required original capture failed/stale')
    if not(src/'owner-reset-barrier-capture-01.stdout').read_bytes().strip() or (src/'owner-reset-barrier-capture-01.stderr').read_bytes():
        raise ValueError('missing/error capture output')
    validator=module('owner_reset_reviewed_roles',src/'validate-title-source-annotations.py')
    raw=json.loads((src/'owner-reset-barrier-source-01.json').read_text())
    validation=validator.validate(raw)
    if raw.get('driver_sha256')!=sha(src/'capture-owner-reset-barrier.py'):raise ValueError('capture invocation identity changed')
    data=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(data).hexdigest()!=SHA:raise ValueError('wrong original image')
    pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0]
    sections=[struct.unpack_from('<IIII',data,pe+32+opt+40*i) for i in range(struct.unpack_from('<H',data,pe+6)[0])]
    def read(a,n):
        for vs,rva,size,offset in sections:
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:
                return data[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
        raise ValueError('unbacked original range')
    for q in raw['ranges']:
        a=int(q['start'],16);end=int(q['end_exclusive'],16)
        if bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(a,end-a):raise ValueError('original byte mismatch')
    ix={int(i['pc'],16):i for q in raw['ranges'] for i in q['instructions']}
    def need(pc,m,args):
        if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):
            raise ValueError('original operation changed '+hex(pc))
    operations=[(0x266de6,'call','0x32f430'),(0x267112,'call','0x3dd7e0'),
      (0x26cdbE,'mov','ecx, ebp'),(0x26cde3,'jmp','0x3dd790'),
      (0x32f50e,'mov','edi, 5'),(0x32f5f8,'sub','rdi, 1'),(0x32f5fc,'jne','0x32f520'),
      (0x32f602,'mov','edx, 0x350'),(0x32f60e,'lea','ecx, [rdi + 8]'),(0x32f617,'call','0x32e400'),
      (0x32f621,'mov','edi, eax'),(0x32f623,'test','eax, eax'),(0x32f625,'jle','0x32f692'),
      (0x32f66b,'mov','ecx, 8'),(0x32f670,'call','0x32e620'),(0x32f68b,'xor','ecx, ecx'),(0x32f68d,'call','0x32e520'),
      (0x32e524,'test','ecx, ecx'),(0x32e526,'je','0x32e561'),(0x32e561,'xor','ecx, ecx'),
      (0x32e563,'call','0x32e070'),(0x32e568,'cmp','qword ptr [rip + 0x1f96c50], 0'),
      (0x32e570,'jne','0x32e57b'),(0x32e572,'call','0x46dfe0'),(0x32e577,'test','eax, eax'),
      (0x32e579,'je','0x32e584'),(0x32e57d,'call','0x35ea30'),(0x32e582,'jmp','0x32e561'),(0x32e58a,'ret',''),
      (0x32e41a,'test','r8, r8'),(0x32e41d,'je','0x32e431'),(0x32e431,'call','0x46de70'),
      (0x46de70,'jmp','0x2df960'),(0x2df963,'imul','r8, rax, 0x1388'),(0x2df974,'add','r8, rcx'),
      (0x3dd7b6,'mov','qword ptr [rax - 0xd], r10'),(0x3dd826,'mov','qword ptr [rax - 0xd], r8')]
    for item in operations:need(*item)
    if ix[0x32e40f]['memory'][0]['rip_target']!='0x22c51f0' or ix[0x2df96d]['memory'][0]['rip_target']!='0x2ec3ee0':raise ValueError('size binding changed')
    # Normal local CFGs only: calls treated as normally returning opaque edges.
    # The actual world body ends in a tail dispatch to3EC620, not a RET.
    # Close this bounded local path explicitly; omitted tail effects stay open.
    world=graph(ix,0x266d10,0x2671b1,terminal_tail='0x3ec620')
    binder=graph(ix,0x26c8c0,0x26cdf4,terminal_tail='0x3dd790',fatal_calls=(0x26cde8,0x26cdee))
    startup=graph(ix,0x32f430,0x32f6be,fatal_calls=(0x32f6b9,))
    wait=graph(ix,0x32e561,0x32e58b)
    if not dominates(world,0x266de6,0x267112):raise ValueError('reset bypasses named pre-call')
    if not dominates(binder,0x26cdbe,0x26cde3) or binder['tails']!=[0x26cde3]:raise ValueError('binder reset argument/tail changed')
    if [c for c in startup['calls'] if c['target']=='0x32e520']!=[dict(pc='0x32f68d',target='0x32e520')]:raise ValueError('wait call set changed')
    skip=graph(ix,0x32f692,0x32f6b9)
    if any(c['target'] in ['0x32e620','0x32e520'] for c in skip['calls']):raise ValueError('nonpositive suffix now submits/waits')
    if not dominates(startup,0x32f625,0x32f68d):raise ValueError('size guard no longer bounds wait')
    # This loop has exactly init5 then decrement1 and only ABI-preserving calls.
    rdi_writes=[i for pc,i in sorted(ix.items()) if 0x32f50e<=pc<=0x32f60e
                and i['args'].split(', ')[0] in ['rdi','edi']]
    if [(i['mnemonic'],i['args']) for i in rdi_writes]!=[('mov','edi, 5'),('sub','rdi, 1')]:raise ValueError('kind8 loop argument provenance changed')
    basefiles='bts-index-binding-inputs-01/'
    manifest=json.loads((UPSTREAM/'manifest.json').read_text())
    members=[m for m in manifest['members'] if m['path'].startswith(basefiles) and m['path'].endswith('.fst')]
    if len(members)!=12 or len({m['path'] for m in members})!=12:raise ValueError('missing retained FST population')
    results=[];offset=4*(8*5000+0x350)
    for member in members:
        path=UPSTREAM/member['path'];blob=path.read_bytes()
        if hashlib.sha256(blob).hexdigest()!=member['sha256'] or len(blob)!=820000:raise ValueError('retained FST changed/incomplete')
        value=struct.unpack_from('<i',blob,offset)[0]
        results.append(dict(path=member['path'],sha256=member['sha256'],offset=offset,
                            raw_hex=blob[offset:offset+4].hex(),signed_value=value,selects_wait=value>0))
    expected={Path(r['path']).name:r['signed_value'] for r in results}
    if expected.get('FileSizeTable_UK.fst')!=-1 or any(v!=3840 for k,v in expected.items() if k!='FileSizeTable_UK.fst'):
        raise ValueError('retained regional discriminator changed')
    result=dict(status='PRODUCER_VALID_CONDITIONAL_OWNER_RESET_BARRIER_INDEPENDENT_PENDING',method='A STATIC_ONLY',
      exe_sha256=SHA,driver_sha256=sha(Path(__file__)),source_sha256=sha(src/'owner-reset-barrier-source-01.json'),
      source_validation=validation,world_call_order=dict(precall='0x266de6 ->0x32f430',reset='0x267112 ->0x3dd7e0',dominates=True),
      binder_tail=dict(argument='ECX = original EBP group before saved-register restore',pc='0x26cde3',target='0x3dd790'),
      conditional_size=dict(kind=8,index=0x350,override_pointer='0x22c5230',null_override_required=True),
      fst_dependency=dict(path=str(UPSTREAM.relative_to(ROOT)),manifest_sha256=sha(UPSTREAM/'manifest.json'),members=results),
      wait_normal_return=dict(pending_head='0x22c51c0',observed_condition='head==0 then normally returned46DFE0()==0',atomic=False,time_bound=False),
      established=['266D10 normal local path calls32F430 before clearing all indexed owner records through3DD7E0.',
        '32F430 wait32E520(0) is conditional on positive kind8/0350 size. Under nulloverride and selected unchanged retained FST, eleven3840 variants select the call and UK-1 skips this submit/wait segment.',
        'The specific unconditional-wait premise is refuted by an original supported data/branch path. This does not show UK never waits elsewhere or that any stale request survives naturally.',
        '32E520(0) pumps and retries until its sequential pending-head/service checks permit normal return; it gives no deadline or atomic guarantee of continuing emptiness.',
        '26C8C0 normal completion restores its frame and tail-jumps to3DD790 with its original group argument; its opaque prior callees and actual actor-load lifetime remain separate.'],
      limits=['All source/local CFG statements assume valid ABI/storage and normally returning relevant calls. EH, opaque transitive effects, concurrent submissions and other reset callers are not closed.',
        'Selected regional FST/null runtime size override are explicit premises, not observed initialization, process file selection or save/load proof.',
        'No universal safe reset/destructor, callback-generation/lifetime or wholeOV19/21/database closure. Current UC1 extent/catalogue dispositions unchanged.',
        'Twelve retained-data computations are not new original-code/live experiments; prior SECTION09 initializer fixtures not repeated.'],
      native_runs=0,live_runs=0,whole_runtime_rows_closed=0)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('CONDITIONAL_OWNER_RESET_BARRIER:11 retained FST variants positive; UK-1 skips namedwait; other callers/state/lifetime OPEN')


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else HERE)
