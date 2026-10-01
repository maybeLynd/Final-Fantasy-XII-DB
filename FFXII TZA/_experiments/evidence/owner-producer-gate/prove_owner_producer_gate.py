"""Original source discriminator for producer disable and local re-enable order."""
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
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main(out,src):
    if out.exists():raise ValueError('immutable result exists')
    roles=load('producer_reviewed_roles',src/'validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13')
    cfg=load('producer_retained_cfg',HERE/'prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')
    s=json.loads((src/'owner-producer-gate-source-run-01.status.json').read_text())
    driver=src/'qualify_owner_producer_gate_source.py'
    if s['exit']!=0 or s['driver_sha256']!=sha(driver):raise ValueError('required qualifier failed/stale')
    if not(src/'owner-producer-gate-source-run-01.stdout').read_bytes().strip() or (src/'owner-producer-gate-source-run-01.stderr').read_bytes():raise ValueError('qualifier missing/error output')
    source=src/'owner-producer-gate-source-01.json';v=json.loads(source.read_text())
    if v['driver_sha256']!=sha(driver) or v['exe_sha256']!=ESHA:raise ValueError('qualifier identity changed')
    annotation=roles.validate(v)
    required=[(0x3dd4c0,0x3dd6bf),(0x32f240,0x32f260),(0x32ed80,0x32f16a),(0x32f850,0x32fa09)]
    if [(int(q['start'],16),int(q['end_exclusive'],16)) for q in v['ranges']]!=required:raise ValueError('required range population missing/changed')
    data=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(data).hexdigest()!=ESHA:raise ValueError('wrong original image')
    pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0]
    secs=[struct.unpack_from('<IIII',data,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
    def read(a,n):
        for vs,rva,size,offset in secs:
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:return data[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
        raise ValueError('unbacked original range')
    for q,(entry,end) in zip(v['ranges'],required):
        if bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(entry,end-entry):raise ValueError('original byte mismatch')
    ix={int(i['pc'],16):i for q in v['ranges'] for i in q['instructions']}
    def need(pc,m,args):
        if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('operation changed '+hex(pc))
    for op in [(0x32f240,'movsxd','rax, ecx'),(0x32f243,'lea','rcx, [rip - 0x20f24a]'),
      (0x32f24a,'cmp','byte ptr [rax + rcx + 0x21a6d18], 0'),(0x32f252,'je','0x32f25c'),
      (0x32f254,'mov','eax, dword ptr [rcx + rax*4 + 0x21a6d28]'),(0x32f25c,'or','eax, 0xffffffff'),
      (0x3dd51c,'xor','esi, esi'),(0x3dd522,'xor','r13d, r13d'),(0x3dd52f,'cmp','dword ptr [rbx + 4], 2'),
      (0x3dd539,'mov','ecx, r12d'),(0x3dd53c,'call','0x32f240'),(0x3dd541,'test','eax, eax'),
      (0x3dd543,'jns','0x3dd54d'),(0x3dd545,'mov','dword ptr [rbx + 4], esi'),(0x3dd548,'jmp','0x3dd656'),
      (0x3dd644,'call','0x3dda70'),(0x3dd656,'mov','rcx, qword ptr [rsp + 0x98]'),
      (0x3dd665,'mov','byte ptr [rbx + 0xd], sil'),(0x3dd669,'test','r13d, r13d'),
      (0x3dd66c,'je','0x3dd675'),(0x3dd672,'and','dword ptr [r15], eax'),
      (0x32ed9a,'movsxd','rdi, ecx'),(0x32edbb,'lea','r14, [rip - 0x20edc2]'),(0x32edc2,'xor','ebp, ebp'),
      (0x32f10d,'mov','byte ptr [rdi + r14 + 0x21a6d18], bpl'),
      (0x32f862,'lea','r14, [rip - 0x20f869]'),(0x32f869,'and','ecx, 0xf'),
      (0x32f87e,'cmp','byte ptr [rdi], 0'),(0x32f881,'jne','0x32f8a7'),
      (0x32f88d,'mov','byte ptr [rcx + r14 + 0x21a6d18], 0'),
      (0x32f8b6,'mov','byte ptr [rcx + r14 + 0x21a6d18], 1'),(0x32f966,'call','0x26c8c0')]:need(*op)
    for pc in [0x32f243,0x32edbb,0x32f862]:
        if ix[pc]['memory'][0]['rip_target']!='0x120000':raise ValueError('enable array base identity changed')
    graphs=[cfg.graph(ix,0x3dd4c0,0x3dd6bf),cfg.graph(ix,0x32f240,0x32f260),
            cfg.graph(ix,0x32ed80,0x32f16a,fatal=(0x32f164,)),cfg.graph(ix,0x32f850,0x32fa09,fatal=(0x32fa04,))]
    tick,getter,reset,binder=graphs
    if getter['calls'] or getter['returns']!=[0x32f25b,0x32f25f]:raise ValueError('getter bounded leaf changed')
    if not cfg.dominates(reset,0x32f10d,0x32f163):raise ValueError('normal reset clear not obligatory')
    if not cfg.dominates(binder,0x32f8b6,0x32f966):raise ValueError('re-enable not before binding')
    # One iteration ends at its next-slot/group-loop boundary. Do not fix the
    # same branch globally and accidentally assert later groups are disabled.
    path=[0x3dd53c,0x3dd541,0x3dd543,0x3dd545,0x3dd548,0x3dd656,0x3dd65e,0x3dd665,0x3dd669,0x3dd66c,0x3dd675,0x3dd67a]
    for a,b in zip(path,path[1:]):
        if b not in tick['edges'][a]:raise ValueError('negative current-iteration CFG changed')
    if 0x3dd644 in path or 0x3dd672 in path:raise ValueError('negative iteration submits/clears mask')
    if any(ix[p]['mnemonic']=='call' for p in path[1:]):raise ValueError('opaque call in negative continuation')
    prefix=list(range(0)) # Exact decoded interval, not integer byte-address iteration.
    prefix=[i for i in v['ranges'][0]['instructions'] if 0x3dd51c<=int(i['pc'],16)<=0x3dd545]
    defs=[i['pc'] for i in prefix if i['args'].split(', ')[0] in ['esi','rsi','sil'] and i['mnemonic'] not in ['cmp','test','push']]
    if defs!=['0x3dd51c']:raise ValueError('state-clear zero provenance changed')
    cleanup_calls=[hex(pc) for pc,t in reset['calls'] if pc<0x32f10d]
    prebind_calls=[dict(pc=hex(pc),target=t) for pc,t in binder['calls'] if 0x32f8b6<pc<0x32f966]
    result=dict(status='PRODUCER_VALID_LOCAL_PRODUCER_GATE_INDEPENDENT_PENDING',producer_complete=True,
      source_pins=[dict(path=source.name,sha256=sha(source))],driver_sha256=sha(Path(__file__)),exe_sha256=ESHA,
      method='A RETAINED_ORIGINAL_SOURCE_LOCAL_CFG',qualifier_sha256=sha(driver),annotation_receipt=annotation,
      reused_cfg_sha256=sha(HERE/'prove_owner_reload_order.py'),retained_dependencies=[v['dependency']]+v['retained_extra'],
      graphs=[dict(entry=hex(g['entry']),instructions=len(g['visited']),returns=[hex(pc) for pc in g['returns']]) for g in graphs],
      negative_iteration_path=[hex(pc) for pc in path],enable=dict(base='0x22c6d18',width=1,valid_group_premise='0..4'),
      cleanup_calls_before_disable=cleanup_calls,opaque_call_sites_after_enable_before_binder=prebind_calls,
      established=['A zero enable byte observed by leaf32F240 returns signed32 -1 without loading the index.3DD4C0 TEST/JNS takes its negative arm, clears current armed owner state+4 to0, and skips local3DDA70 submission for that iteration; other slots/groups are separate.',
        'That negative continuation does not clear the request mask bit: initialized R13D remains0 and bypasses the AND. State0 is not automatic retry; renewed arming/state2 or other behavior is separate.',
        'Original32ED80 normal valid-group return clears this same enable array at32F10D, after its preceding cleanup calls. It does not locally disable the producer at function entry.',
        'Original32F850 nonzero-header path writes1 to this same group enable field at32F8B6 before any reached26C8C0 binder call. A universal uninterrupted local zero-gate-through-binding premise is refuted.'],
      limits=['Read-only source qualification/CFG, not native/live state. No initialized defaults, natural reentry, all writers/callers, thread scheduling, queue drain or global one-live-owner guarantee.',
        'Enable value is the byte at the getter read, not assumed entry value; nonzero getter loads DWORD whose signed value may still be negative. Valid group/storage/ABI/nonaliasing premises.',
        'Opaque cleanup/prebinder calls may mutate state, service callbacks or otherwise prevent normal return. A preceding local store1 does not guarantee field remains1 at binder entry, nor prove an actual intervening producer invocation.',
        'Current negative iteration only; later slots/groups can be enabled. No transitive submission/cancellation absence, deadline, EH/interference closure or automatic whole OV19/21/natural lifetime acceptance.',
        'Independent SPEC acceptance and existing FABLE/OPUS consumption pending. Earlier callback/reload/queue evidence retained at its own scope, no rerun or enlarged native credit.'],
      affected_claims=['Disabled-producer interval premise for owner reset/reload uniqueness','Indexed-owner state/mask behavior after provider gate failure'],
      next_discriminator='Prove relevant opaque pre-binder calls cannot service3DD4C0 or alternate owner submissions under the actual caller/ABI, or identify the exact natural scheduling/ownership state requiring observation. Separate direct D4/world-reset paths; do not spend gameplay on this settled local branch.',
      native_runs=0,live_runs=0,whole_runtime_rows_closed=0,cleanup='Read-only references/retained bytes; finite children terminal; no game/process/save/config or peer writes')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('LOCAL_PRODUCER_GATE: zero skips current submission; local enable restored before bind; reentry/natural lifetime OPEN; native/game0')


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else HERE)
