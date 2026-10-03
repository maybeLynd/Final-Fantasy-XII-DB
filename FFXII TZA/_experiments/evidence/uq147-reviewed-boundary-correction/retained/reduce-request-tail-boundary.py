"""One bounded static consequence of the exact notification arguments; not natural reachability."""
import hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=P/sys.argv[1]
if out.exists():raise ValueError('fresh output required')
driver=P/'capture-request-tail.py';status=json.loads((P/'capture-request-tail-01.status.json').read_text())
pin='89796185513456c9faffc1bea6cfe1f6aaaf492eab7215fd9c7114d4a9f497e1'
if not(status['terminal'] is True and status['exit']==0 and status['exception'] is None and status['driver_sha256']==pin==sha(driver)):raise ValueError('required successful current capture')
source=P/'source-request-tail-01.json';source_bytes=source.read_bytes()
if hashlib.sha256(source_bytes).hexdigest()!='7536b76bfaabfee9319268822c1463df39550d0516f17f22c580ea14e4889454':raise ValueError('exact certified source preimage changed')
s=json.loads(source_bytes)
if s.get('wrapper_complete') is not True or s.get('invocation_driver_sha256')!=pin:raise ValueError('required complete actual wrapper')
validator=W/'validate-title-source-annotations.py'
if sha(validator)!='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13':raise ValueError('reviewed validator changed')
spec=importlib.util.spec_from_file_location('reviewed_annotations',validator);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
agreement=v.validate(s)
ix={int(i['pc'],16):i for r in s['ranges'] for i in r['instructions']}
pins=[(0x317ea9,'xor','edx, edx'),(0x317eab,'lea','ecx, [rdx + 1]'),(0x317eb2,'jmp','0x25aad0'),(0x25aad6,'mov','ebx, ecx'),(0x25aad8,'mov','ecx, edx'),(0x25aada,'call','0x3588b0'),(0x25aadf,'test','ebx, ebx'),(0x25aae1,'jne','0x25ab1c'),(0x25ab1c,'add','rsp, 0x20'),(0x25ab20,'pop','rbx'),(0x25ab21,'ret','')]
for pc,m,a in pins:
    if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise ValueError('required argument/branch/epilogue changed '+hex(pc))
writes=[dict(pc=i['pc'],memory=m) for r in s['ranges'] if r['start']=='0x25aad0' for i in r['instructions'] for m in i['memory'] if m['role'] in ['w','rw'] and m['base']!='rsp']
if [i['pc'] for i in writes]!=['0x25aaf2','0x25aaf8','0x25ab00','0x25ab06','0x25ab15']:raise ValueError('complete notification own-write footprint changed')
transfers=[dict(pc=i['pc'],mnemonic=i['mnemonic'],args=i['args']) for r in s['ranges'] for i in r['instructions'] if i['mnemonic'].startswith(('call','j'))]
row=dict(status='BOUNDED_NOTIFICATION_WRITE_BRANCH_EXCLUDED_NATURAL_KO_STILL_OPEN',method='A complete shipping bytes and normal-ABI constant-argument dataflow; no execution',driver_sha256=sha(Path(__file__)),source_sha256=sha(source),exe_sha256=s['exe_sha256'],capture_driver_sha256=pin,annotation_agreement=agreement,physical_bodies=s['physical_bodies'],argument_branch_instructions=[ix[pc] for pc,_,_ in pins],all_local_transfers=transfers,unreached_own_writes=writes,
    established=['Every normal tail of00317E60 sets EDX0 and ECX1, restores its stack, then jumps to0025AAD0.','0025AAD0 saves incomingECX in EBX. Under normal x64 ABI the preceding003588B0 call preserves EBX1, so test/jne at0025AADF/E1 takes0025AB1C. The five own publication writes and002F1710 call at0025AB10 are unreachable on this exact argument leg. The resolver still executes before the branch.'],
    implication='Exclude the0025AAD0 publication block and002F1710 from synchronous cleanup dependencies for this leg; do not exclude preceding resolver/conditional path-reset helpers or other callers.',
    unresolved=['Effects/identity/noninterference of003590D0,003588B0,00263E30 and conditional0033C9B0.','Actual action acceptance/commit/execution and KO-to-capability scheduling; direct and aliased mode-word writers and special-sequence cleanup.','Natural mode1 KOcounterpart reachability and mask7 observation, lifetime and presentation.'],
    limits='Producer static reduction, not independent acceptance. Original169B capture is new source availability, not169B of new game behavior or native execution. No whole UQ147 or formerly-runtime question closure. Normal ABI, intact code, normal returns and valid memory are explicit premises; cannot infer mode preservation across opaque calls.')
with out.open('x') as f:json.dump(row,f,indent=2)
print('Excluded notification write/callback block on exact tail(1,0); earlier helper effects and natural KO-order question remain OPEN')
