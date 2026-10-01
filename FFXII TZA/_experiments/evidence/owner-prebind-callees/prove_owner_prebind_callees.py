"""Closed pre-binder call slice and conditional data-write bounds, static only."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
ESHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def load(name,path,pin):
    if sha(path)!=pin:raise ValueError('reviewed helper changed')
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def main(out,src):
    if out.exists():raise ValueError('immutable result exists')
    roles=load('prebind_roles',src/'validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13')
    cfg=load('prebind_cfg',HERE/'prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')
    status=json.loads((src/'owner-prebind-source-run-01.status.json').read_text());driver=src/'qualify_owner_prebind_source.py'
    if status['exit']!=0 or status['driver_sha256']!=sha(driver):raise ValueError('required qualifier failed/stale')
    if not(src/'owner-prebind-source-run-01.stdout').read_bytes().strip() or (src/'owner-prebind-source-run-01.stderr').read_bytes():raise ValueError('qualifier missing/error output')
    source=src/'owner-prebind-source-01.json';v=json.loads(source.read_text());annotation=roles.validate(v)
    if v['driver_sha256']!=sha(driver) or v['exe_sha256']!=ESHA:raise ValueError('qualifier identity changed')
    required=[(0x36c1d0,0x36c1e4),(0x36c1f0,0x36c286),(0x32f850,0x32fa09),(0x36b200,0x36b20f)]
    if [(int(r['start'],16),int(r['end_exclusive'],16)) for r in v['ranges']]!=required:raise ValueError('required range population missing/changed')
    premise=json.loads((src/'owner-prebind-bounds-premise-01.json').read_text())
    if premise!=dict(kind='conditional valid-context premise, not observed live state',bank=0,depth_min=0,depth_max=30,arena_ids=[5,13,14]):
        raise ValueError('required valid-context bounds premise changed')
    data=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(data).hexdigest()!=ESHA:raise ValueError('wrong original image')
    pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0]
    secs=[struct.unpack_from('<IIII',data,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
    def read(a,n):
        for vs,rva,size,offset in secs:
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:return data[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
        raise ValueError('unbacked original range')
    for r,(entry,end) in zip(v['ranges'],required):
        if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(entry,end-entry):raise ValueError('original byte mismatch')
    ix={int(i['pc'],16):i for r in v['ranges'] for i in r['instructions']}
    def need(pc,m,args):
        if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('operation changed '+hex(pc))
    for op in [(0x36b200,'mov','edx, dword ptr [rip + 0x1f6d7b2]'),(0x36b206,'xor','eax, eax'),
      (0x36b208,'bt','edx, ecx'),(0x36b20b,'setb','al'),(0x36b20e,'ret',''),
      (0x36c1d0,'lea','r9, [rsp]'),(0x36c1d4,'xor','r8d, r8d'),
      (0x36c1d7,'mov','r9, qword ptr [r9 + 4]'),(0x36c1db,'sub','r9, 5'),(0x36c1df,'jmp','0x36c1f0'),
      (0x36c1f5,'movsxd','r10, r8d'),(0x36c1f8,'lea','rbx, [rip - 0x24c1ff]'),
      (0x36c1ff,'lea','r11, [r10*4 + 0x21b89c0]'),(0x36c207,'movsxd','r8, dword ptr [r11 + rbx]'),
      (0x36c20b,'cmp','r8d, 0x1f'),(0x36c20f,'jl','0x36c213'),(0x36c211,'jmp','0x36c211'),
      (0x36c21a,'shl','r10, 5'),(0x36c21e,'add','r10, r8'),(0x36c221,'add','r10, r10'),
      (0x36c25a,'lea','eax, [r8 + 1]'),(0x36c25e,'mov','dword ptr [r11 + rbx], eax'),
      (0x36c265,'mov','dword ptr [rip + 0x1f6cbad], edx'),(0x36c26b,'mov','qword ptr [rip + 0x1f6cbae], r9')]:need(*op)
    if ix[0x36b200]['memory'][0]['rip_target']!='0x22d89b8' or ix[0x36c1f8]['memory'][0]['rip_target']!='0x120000':raise ValueError('arena context identity changed')
    loader=cfg.graph(ix,0x32f850,0x32fa09,fatal=(0x32fa04,))
    prebind=[(pc,t) for pc,t in loader['calls'] if 0x32f8b6<pc<0x32f966]
    if {t for pc,t in prebind}!={'0x36b200','0x36c1d0'}:raise ValueError('prebind callee set not closed')
    for pc,t in prebind:
        if not cfg.dominates(loader,0x32f8b6,pc):raise ValueError('prebind interval not after enable')
    wrapper=cfg.graph(ix,0x36c1d0,0x36c1e4,tail='0x36c1f0')
    context=cfg.graph(ix,0x36c1f0,0x36c286)
    leaf=cfg.graph(ix,0x36b200,0x36b20f)
    if wrapper['calls'] or wrapper['tails']!=[0x36c1df] or context['calls'] or context['tails'] or leaf['calls'] or leaf['tails']:
        raise ValueError('callee boundary not closed')
    writes=[(int(i['pc'],16),m) for i in v['ranges'][1]['instructions'] for m in i['memory'] if m['role'] in ['w','rw']]
    expected=[0x36c1f0,0x36c224,0x36c234,0x36c243,0x36c252,0x36c25e,0x36c265,0x36c26b,0x36c27f]
    if [pc for pc,m in writes]!=expected:raise ValueError('context write population changed')
    intervals=[]
    for pc,m in writes:
        if m['base']=='rsp':
            intervals.append(dict(pc=hex(pc),kind='caller shadow-stack slot',base='entry RSP+8',size=m['size'],nonaliasing='explicit normal stack premise'));continue
        if pc in [0x36c224,0x36c234,0x36c243,0x36c252]:
            if m['base']!='rbx' or m['index']!='r10' or m['scale']!=8:raise ValueError('saved-context address expression changed')
            lo=0x120000+m['displacement'];hi=lo+16*premise['depth_max']+m['size']
        elif pc==0x36c25e:
            if (m['base'],m['index'])!=('r11','rbx'):raise ValueError('bank count address changed')
            lo=0x22d89c0;hi=lo+m['size']
        else:
            lo=int(m['rip_target'],16);hi=lo+m['size']
        intervals.append(dict(pc=hex(pc),low=hex(lo),high_exclusive=hex(hi),size=m['size']))
    protected=[('pending head/tail/free globals',0x22c51c0,0x22c51d8),('group enable bytes',0x22c6d18,0x22c6d1d),
               ('indexed owners and masks',0x2b581a0,0x2b58a74)]
    for span in intervals:
        if 'low' not in span:continue
        lo=int(span['low'],16);hi=int(span['high_exclusive'],16)
        for label,a,b in protected:
            if lo<b and a<hi:raise ValueError('context write can overlap protected '+label)
    result=dict(status='PRODUCER_VALID_CONDITIONAL_PREBIND_CALLEE_CLOSURE_INDEPENDENT_PENDING',producer_complete=True,
      source_pins=[dict(path=source.name,sha256=sha(source))],driver_sha256=sha(Path(__file__)),exe_sha256=ESHA,
      method='A ORIGINAL_SOURCE_CLOSED_CALL_SLICE_AND_CONDITIONAL_BOUNDS',annotation_receipt=annotation,
      reused_cfg_sha256=sha(HERE/'prove_owner_reload_order.py'),retained_dependencies=[v['dependency']]+v['retained_extra'],
      premise=premise,prebind_sites=[dict(pc=hex(pc),target=t) for pc,t in prebind],context_writes=intervals,
      established=['The complete source-local enable1-to-binder interval invokes only36B200 and36C1D0.36B200 is a15B flag getter with no call/tail;36C1D0 tails only36C1F0, whose complete150B original body contains no calls/callbacks/tails.',
        'Under valid bank0/depth0..30 and nonaliasing normal-stack premises, all context writes are bounded saved-context/count/metadata fields, disjoint from pending globals, group enable bytes and indexed owner/mask storage. R9 metadata is stored, never called or dereferenced by36C1F0.',
        'These exact callees cannot synchronously service3DD4C0/owner submission/queue callbacks in this interval on the stated normal path. The prior opaque-looking call names no longer require live absence sampling for this limited proposition.'],
      limits=['Normal original function entry/ABI/accessible nonaliasing storage and conditional initialized bounds, not captured process state or universal initialization proof. Depth31+ locally spins; signed-negative count is not guarded below zero and is excluded from valid bounds.',
        'The wrapper reads QWORD at entryRSP+4 then subtracts5. Preserve original bytes/unaligned read; no portable source/debug-statement attribution or assumed saved-return-address value.',
        'No asynchronous thread/scheduler/exception/unwind closure, natural producer reachability, earlier/later caller interval exclusion, direct D4/world-reset guarantee or full owner uniqueness/safe reload.',
        'The field may be changed by unrelated concurrency. No game/native run or external-audit count credited. Independent review and FABLE/OPUS canonical consumption required.'],
      affected_claims=['Owner reset/lifetime sufficiency: pre-binder synchronous-service gap for normal32F850','Arena context metadata versus callback boundary in this exact path'],
      next_discriminator='Actual same-thread caller/update order and any alternative submit/reentry paths before primary completion, plus independent D4/world reset. Reuse retained scheduling bodies and prove bounded call relationships before requesting minimal process observation.',
      native_runs=0,live_runs=0,whole_runtime_rows_closed=0,cleanup='Read-only original/retained source; finite children terminal; no game/PC/save/config/reference or peer writes')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('PREBIND_CALLEE_CLOSURE: no synchronous producer service on valid context path; asynchronous/natural lifetime OPEN; native/game0')


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else HERE)
