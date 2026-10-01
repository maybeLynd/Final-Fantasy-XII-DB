"""Reset/admission source discriminator; conditional countermodel, not live reachability."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
UP=ROOT/'Database/FFXII TZA/_experiments/evidence/owner-reset-barrier/qualified-02'
UPS='82f5bf38b2239395628083ca267e14ca29d5679308f7e8f01ce467bb31a2319e'
MANIFEST=ROOT/'Database/FFXII TZA/_experiments/evidence/continuation-section09-owner-producer/original_body_manifest.json'
MSHA='23785132366d8f1464b42ccfec0e1d9d4cbec05a04d733b212270f867a7e9de8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main(out,src,up):
    if out.exists():raise ValueError('immutable result exists')
    spec=importlib.util.spec_from_file_location('admission_reviewed_roles',src/'validate-title-source-annotations.py')
    roles=importlib.util.module_from_spec(spec);spec.loader.exec_module(roles)
    s=json.loads((src/'owner-admission-capture-01.status.json').read_text())
    if s['exit']!=0 or s['driver_sha256']!=sha(src/'capture-owner-admission.py'):raise ValueError('required admission capture failed/stale')
    if not(src/'owner-admission-capture-01.stdout').read_bytes().strip() or (src/'owner-admission-capture-01.stderr').read_bytes():raise ValueError('capture missing/error output')
    arm=json.loads((src/'owner-admission-source-01.json').read_text());roles.validate(arm)
    if arm['driver_sha256']!=sha(src/'capture-owner-admission.py'):raise ValueError('capture driver changed')
    if sha(up/'manifest.json')!=UPS:raise ValueError('reset manifest changed')
    m=json.loads((up/'manifest.json').read_text())
    member=next(m for m in m['members'] if m['path']=='owner-reset-barrier-source-01.json')
    p=up/member['path']
    if sha(p)!=member['sha256']:raise ValueError('retained reset source changed')
    v=json.loads(p.read_text());roles.validate(v)
    reset=next(r for r in v['ranges'] if r['start']=='0x3dd790')
    if sha(MANIFEST)!=MSHA:raise ValueError('SECTION09 manifest changed')
    mm=json.loads(MANIFEST.read_text())
    data=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(data).hexdigest()!=SHA:raise ValueError('wrong original image')
    pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0]
    secs=[struct.unpack_from('<IIII',data,pe+32+opt+40*i) for i in range(struct.unpack_from('<H',data,pe+6)[0])]
    def read(a,n):
        for vs,rva,size,offset in secs:
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:return data[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
        raise ValueError('unbacked original range')
    ranges=arm['ranges']+[reset]
    if len(ranges)!=2:raise ValueError('missing original population')
    for r,entry,hi in zip(ranges,[0x3dda20,0x3dd790],[0x3dda6c,0x3dd7d5]):
        lo=int(r['start'],16);end=int(r['end_exclusive'],16)
        f=next(f for f in mm['functions'] if int(f['entry'],16)==entry)
        if (lo,end,r['sha256'])!=(entry,hi,f['sha256']):raise ValueError('retained boundary/hash changed')
        if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(lo,end-lo):raise ValueError('original byte mismatch')
    ix={int(i['pc'],16):i for r in ranges for i in r['instructions']}
    def need(pc,m,args):
        if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('operation changed '+hex(pc))
    ops=[(0x3dd790,'xor','r10d, r10d'),(0x3dd793,'movsxd','r8, ecx'),(0x3dd796,'imul','rax, r8, 0x1c0'),
      (0x3dd79d,'lea','r9, [rip + 0x277aa09]'),(0x3dd7a4,'mov','edx, r10d'),(0x3dd7a7,'add','rax, r9'),
      (0x3dd7b0,'mov','word ptr [rax + 1], dx'),(0x3dd7b4,'inc','edx'),
      (0x3dd7b6,'mov','qword ptr [rax - 0xd], r10'),(0x3dd7ba,'mov','byte ptr [rax], r10b'),
      (0x3dd7bd,'mov','byte ptr [rax - 1], cl'),(0x3dd7c0,'lea','rax, [rax + 0x1c]'),
      (0x3dd7c4,'cmp','edx, 0x10'),(0x3dd7c7,'jl','0x3dd7b0'),(0x3dd7d0,'mov','dword ptr [rax + r8*4], r10d'),
      (0x3dda20,'movsxd','r9, ecx'),(0x3dda23,'movsxd','rax, edx'),(0x3dda26,'mov','rcx, r9'),
      (0x3dda29,'shl','rcx, 4'),(0x3dda2d,'add','rcx, rax'),(0x3dda30,'imul','rax, rcx, 0x1c'),
      (0x3dda3b,'cmp','dword ptr [rax + rcx + 4], 0'),(0x3dda40,'jne','0x3dda69'),
      (0x3dda42,'mov','dword ptr [rax + rcx + 8], r8d'),(0x3dda4e,'mov','dword ptr [rax + rcx + 4], 2'),
      (0x3dda5f,'or','dword ptr [r8 + r9*4], eax'),(0x3dda63,'mov','eax, 1'),(0x3dda68,'ret','')]
    for op in ops:need(*op)
    if ix[0x3dda34]['memory'][0]['rip_target']!='0x2b581a0' or ix[0x3dd79d]['memory'][0]['rip_target']!='0x2b581ad':raise ValueError('same owner base changed')
    if ix[0x3dd7c9]['memory'][0]['rip_target']!='0x2b58a60' or ix[0x3dda47]['memory'][0]['rip_target']!='0x2b58a60':raise ValueError('mask base changed')
    for r in ranges:
        if any(i['mnemonic']=='call' for i in r['instructions']):raise ValueError('unexpected opaque call in local reset/armer')
    # Reset has only a finite fixed loop; armer reads exactly the state DWORD.
    reads=[(i['pc'],mem['size']) for i in arm['ranges'][0]['instructions'] for mem in i['memory'] if mem['role'] in ['r','rw']]
    if reads!=[('0x3dda3b',4),('0x3dda5f',4)]:raise ValueError('another armer memory dependency exists')
    status=json.loads((src/'owner-uniqueness-existing-check-01.status.json').read_text())
    driver=src/'owner-uniqueness-delivery-source-01.py'
    output=(src/'owner-uniqueness-existing-check-01.stdout').read_text()
    if status['exit']!=0 or status['driver_sha256']!=sha(driver) or (src/'owner-uniqueness-existing-check-01.stderr').read_bytes():raise ValueError('original O control failed/stale')
    if 'PASS  O armer admits only state 0' not in output or 'FAILS 0' not in output:raise ValueError('original O result missing')
    tree=ast.parse(driver.read_text())
    checks=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check'
            and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value=='O']
    if len(checks)!=1:raise ValueError('O invocation boundary changed')
    predicate=ast.get_source_segment(driver.read_text(),checks[0].args[1])
    expected='arm.get(0x3DDA3B) == "cmp dword ptr [rax + rcx + 4], 0" and arm.get(0x3DDA4E) == "mov dword ptr [rax + rcx + 4], 2"'
    if predicate!=expected:raise ValueError('original O admission predicate changed')
    # A source-compositional countermodel, explicitly IF reset can run before
    # retirement. No queue marker represents captured/native process memory.
    group=1;slot=0;owner=0x2b581a0+group*0x1c0+slot*0x1c
    reset_first=0x2b581ad+group*0x1c0-0xd
    if owner!=reset_first:raise ValueError('different reset/armer object')
    cases=[dict(group=group,slot=slot,owner=hex(owner),initial_state=state,pending_queue_marker=1,
                state_after_original_reset=0,armer_predicate_accepts=True,state_after_original_armer=2,
                queue_marker_unchanged_locally=True,condition='reset runs before pending request retirement') for state in [3,5]]
    result=dict(status='PRODUCER_VALID_OWNER_ADMISSION_SCOPE_INDEPENDENT_PENDING',method='A STATIC_ONLY',exe_sha256=SHA,
      checker_sha256=sha(Path(__file__)),armer_source_sha256=sha(src/'owner-admission-source-01.json'),
      reset_dependency=dict(manifest_sha256=UPS,member=member),section09_manifest_sha256=MSHA,
      original_O_predicate=predicate,original_producer_control='Unmodified delivery.py exits0/FAILS0 including O; its admission-only scope is reproduced, not independently re-accepted.',
      conditional_countermodels=cases,
      established=['Same static owner DWORD+4 is unconditionally cleared by original3DD790 and is the sole admission-state read of3DDA20. Reset has no entry-state guard or local call; armer does not read queue head, slot identity or pending request count.',
        'IF reset runs before a pending owner request retires, the armer locally admits the reset owner again from state0. The existing O check passes while omitting this exact reset/pending exclusion. Admission alone is not a global one-live-request proof.',
        'This identifies a missing sufficiency premise, not a natural two-request occurrence or an automatic refutation of OV36 per-slot delivery. Prior D/P/H evidence remains at its existing scope.'],
      limits=['Two source-compositional state/queue-marker cases are neither native executions nor captured live states. No original second submission was performed or claimed.',
        'Normal initialized call flow may exclude the conditional countermodel through queue FIFO, disabled producers, cleanup or other mechanisms. The reset/retirement ordering proof remains required before global uniqueness.',
        'Group1/slot0 valid storage, certified unmodified bytes, no interference/alias corruption. Mask memory is distinct from queue slot storage; neither function establishes natural timing/lifetime.',
        'No automatic register/OV36/all-L2 reopening. FABLE scope adjudication and independent review must identify which stronger prose depends on this premise.'],
      affected_claims=['ov36-callback-delivery-fable README/headline/O: universal one-live-request-per-owner scope','Owner lifetime consumers that infer pending exclusion from armer admission alone'],
      next_discriminator='Retained original queued-primary FIFO and producer-disable interval versus synchronous D4 override/world-reset ordering; prove pending-owner exclusion if possible, otherwise preserve precise natural-state requirement.',
      native_runs=0,live_runs=0,whole_runtime_rows_closed=0)
    out.write_text(json.dumps(result,indent=2)+'\n');print('OWNER_ADMISSION_SCOPE:original O passes; reset/pending exclusion is a separate required premise; per-slot delivery preserved')


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else HERE,Path(sys.argv[3]) if len(sys.argv)>3 else UP)
