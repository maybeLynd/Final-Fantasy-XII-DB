"""Source-bound admission/service order; no assumed natural full pool or callback."""
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
    roles=load('fullpool_roles',src/'validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13')
    cfg=load('fullpool_cfg',HERE/'prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')
    status=json.loads((src/'owner-fullpool-source-run-01.status.json').read_text())
    outer=src/'qualify_owner_fullpool_source.py';helper=src/'qualify_owner_queue_order_source.py'
    if status['exit']!=0 or status['driver_sha256']!=sha(outer) or status['helper_sha256']!=sha(helper):raise ValueError('required qualifier failed/stale')
    stdout=(src/'owner-fullpool-source-run-01.stdout').read_text()
    if 'OUTER_DRIVER_SHA256:'+sha(outer) not in stdout or (src/'owner-fullpool-source-run-01.stderr').read_bytes():raise ValueError('qualifier missing/error output')
    source=src/'owner-fullpool-source-01.json';v=json.loads(source.read_text());annotation=roles.validate(v)
    if v['driver_sha256']!=sha(helper) or v['exe_sha256']!=ESHA:raise ValueError('qualifier identity changed')
    if v.get('selected_entries')!=['0x3dda70','0x32e620','0x32e870'] or v.get('include_pump_table') is not False or v.get('table') is not None:
        raise ValueError('required bounded selection changed')
    required=[(0x3dda70,0x3ddacb),(0x32e620,0x32e774),(0x32e870,0x32e98d)]
    if [(int(r['start'],16),int(r['end_exclusive'],16)) for r in v['ranges']]!=required:raise ValueError('required range population missing/changed')
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
    for op in [(0x3dda76,'mov','rbx, rcx'),(0x3dda7b,'call','0x36b130'),
      (0x3dda80,'mov','edx, dword ptr [rbx + 0x18]'),(0x3dda83,'lea','rcx, [rip - 0x23a]'),
      (0x3dda8a,'mov','r9d, dword ptr [rbx + 0x14]'),(0x3dda8e,'lea','r8, [rsp + 0x30]'),
      (0x3dda93,'mov','qword ptr [rsp + 0x40], rcx'),(0x3dda98,'movsx','ecx, word ptr [rbx + 0x10]'),
      (0x3dda9c,'mov','qword ptr [rsp + 0x20], r8'),(0x3ddaa1,'mov','r8, rax'),
      (0x3ddaa4,'mov','dword ptr [rsp + 0x30], edx'),(0x3ddaa8,'movsx','edx, word ptr [rbx + 0x12]'),
      (0x3ddaac,'mov','qword ptr [rsp + 0x48], 0'),(0x3ddab5,'mov','dword ptr [rsp + 0x38], ebx'),
      (0x3ddab9,'call','0x32e620'),(0x3ddabe,'mov','dword ptr [rbx + 4], 3'),
      (0x32e64a,'test','edx, edx'),(0x32e64c,'jns','0x32e656'),(0x32e656,'call','0x3eb0d0'),
      (0x32e665,'je','0x32e742'),(0x32e6dd,'call','0x32e870'),(0x32e759,'call','0x32e870'),
      (0x32e88d,'cmp','qword ptr [rip + 0x1f9693c], rbx'),(0x32e888,'xor','ebx, ebx'),
      (0x32e8a0,'jne','0x32e8c5'),(0x32e8a8,'xor','ecx, ecx'),(0x32e8aa,'call','0x32e070'),
      (0x32e8af,'call','0x46dfe0'),(0x32e8b6,'call','0x35ea30'),
      (0x32e8bb,'cmp','qword ptr [rip + 0x1f9690d], 0'),(0x32e8c3,'je','0x32e8a2'),
      (0x32e8c9,'call','0x32e990'),(0x32e8ce,'mov','rcx, qword ptr [rsp + 0x60]')]:need(*op)
    if ix[0x3dda83]['memory'][0]['rip_target']!='0x3dd850' or any(ix[pc]['memory'][0]['rip_target']!='0x22c51d0' for pc in [0x32e88d,0x32e8bb]):
        raise ValueError('callback/free-head identity changed')
    owner=cfg.graph(ix,0x3dda70,0x3ddacb)
    requester=cfg.graph(ix,0x32e620,0x32e774)
    receiver=cfg.graph(ix,0x32e870,0x32e98d)
    free=cfg.graph(ix,0x32e870,0x32e98d,fixed={0x32e8a0:True})
    full=cfg.graph(ix,0x32e870,0x32e98d,fixed={0x32e8a0:False})
    if owner['calls']!=[(0x3dda7b,'0x36b130'),(0x3ddab9,'0x32e620')] or owner['returns']!=[0x3ddaca]:raise ValueError('owner call population changed')
    if not cfg.dominates(owner,0x3ddab9,0x3ddabe) or not cfg.dominates(owner,0x3ddabe,0x3ddaca):raise ValueError('postcall state store not obligatory')
    if [pc for pc,t in requester['calls'] if t=='0x32e870']!=[0x32e6dd,0x32e759]:raise ValueError('requester arm population changed')
    if 0x32e8aa in free['visited'] or 0x32e8c9 not in free['visited']:raise ValueError('free-slot service exclusion changed')
    if not cfg.dominates(full,0x32e8aa,0x32e8c9) or not cfg.dominates(full,0x32e8c9,0x32e98c):raise ValueError('fullpool service-before-acceptance order changed')
    # Full-pool calls precede the original descriptor read/callback copy. The
    # stack descriptor itself was staged before the caller invokes32E620.
    for pc in [0x3ddaa4,0x3ddab5,0x3dda93,0x3ddaac]:
        if not cfg.dominates(owner,pc,0x3ddab9):raise ValueError('descriptor staging not obligatory')
    for pc in [0x32e8ce,0x32e8dd,0x32e951]:
        if not cfg.dominates(full,0x32e8aa,pc):raise ValueError('descriptor consumption not after fullpool service')
    defs=[i['pc'] for i in v['ranges'][0]['instructions'] if i['args'].split(', ')[0] in ['rbx','ebx','bl','bh'] and i['mnemonic'] not in ['cmp','test','push']]
    if defs!=['0x3dda76','0x3ddac9']:raise ValueError('owner pointer provenance changed')
    state_stores=[i['pc'] for i in v['ranges'][0]['instructions'] for m in i['memory'] if m['base']=='rbx' and m['role'] in ['w','rw'] and m['displacement']==4]
    if state_stores!=['0x3ddabe']:raise ValueError('owner state-store population changed')
    result=dict(status='PRODUCER_VALID_FULLPOOL_ADMISSION_ORDER_INDEPENDENT_PENDING',producer_complete=True,
      source_pins=[dict(path=source.name,sha256=sha(source))],driver_sha256=sha(Path(__file__)),exe_sha256=ESHA,
      qualifier_outer_sha256=sha(outer),qualifier_helper_sha256=sha(helper),annotation_receipt=annotation,
      reused_cfg_sha256=sha(HERE/'prove_owner_reload_order.py'),retained_dependency=v['dependency'],method='A RETAINED_ORIGINAL_SOURCE_BRANCH_ORDER',
      partitions=[dict(free_head_nonzero=True,local_pump_before_insert=False,allocation_site='0x32e8c9'),
                  dict(free_head_nonzero=False,local_pump_before_insert=True,pump_site='0x32e8aa',allocation_site='0x32e8c9',loop='may repeat or never return')],
      descriptor=dict(base='caller RSP+30',length_at='+0',owner_data32_at='+8',callback_at='+10',callback='0x3dd850',cancel_at='+18',cancel=0,
                      premise='accessible normal stack/nonaliasing ABI; staged before opaque request call, consumed after fullpool service'),
      established=['3DDA70 stages the owner descriptor and invokes32E620 before its sole owner state+4 write3. Normal local return does not re-read, branch on or reconcile state changed by the opaque requester; the postcall store is unconditional.',
        'Both nonnegative requester arms can invoke32E870. On its observed free-head-zero branch, original32E8AA calls32E070 synchronously before allocation/insertion32E8C9 and later descriptor consumption. Free-head-nonzero control skips that local service loop.',
        'Thus queue service is not universally deferred until this owner submission returns. That source boundary needs no new game session. A pump call is not proof a callback actually executes; completion still depends on prior pump head/state/IO evidence.',
        'IF a normally returning serviced callback changes the current owner state during this call, original3DDA70 subsequently writes3 to its retained owner pointer. This is a conditional local effect, not an observed same-group reset, natural double request or safe lifetime claim.'],
      limits=['Source CFG partitions, no new FF12/native/game execution. Full pool, actual head/completion, initialized fields/resource destination validity, natural caller timing/thread state and callback effects are unproved here.',
        'Normal ABI preserves RBX and stack; valid accessible disjoint queue/free/storage and stable descriptor stack. Opaque calls/EH/concurrency/invalid memory can prevent normal return; service loops have no deadline.',
        'Descriptor fields are staged before service. This does not prove the old resource-derived destination/size still valid if callbacks change resources, nor lifetime/ABA/pointer identity stability.',
        'No assertion32E620 rejection is naturally reachable or all submit paths use3DDA70. Prior rejection/gate/queue/callback evidence kept at its existing scope; no repeat samples or enlarged native credit.',
        'Independent SPEC verdict and FABLE/OPUS canonical incorporation pending. Whole OV19/21/36/natural owner uniqueness remain open.'],
      affected_claims=['Owner submit state transition and allowed synchronous-service boundary','Lifetime/reset pending exclusion during queue-pool pressure'],
      next_discriminator='Reuse original full-pool/generation/callback evidence to prove or bound actual same-group primary reset and staged destination lifetime; natural occupancy/entry only if needed by canonical consumer. Avoid recapturing the settled local branch.',
      native_runs=0,live_runs=0,whole_runtime_rows_closed=0,cleanup='Read-only original/retained inputs; finite children terminal; no PC/game/save/config/reference or peer writes')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('FULLPOOL_ADMISSION_ORDER: service before insertion/postcall state3; free-slot control no local pump; natural callback/lifetime OPEN; native/game0')


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else HERE)
