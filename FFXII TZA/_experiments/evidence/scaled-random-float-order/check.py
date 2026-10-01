import hashlib,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;s=json.loads((W/'raw.json').read_text());R=W/'retained'
sha=lambda b:hashlib.sha256(b).hexdigest()
source=json.loads((R/'parent-source.json').read_text());body=bytes.fromhex(source['raw_hex']);code=(R/'window.bin').read_bytes()
assert sha(body)==s['reference']['parent_body_sha256']=='32f4c93324e6c153518b5b42e85597f75495de8f66171fd58daf355e7b9a063a'
assert code==body[0x3D8F3F-0x3D8E50:0x3D8F79-0x3D8E50] and len(code)==58
assert sha(code)==s['reference']['window_sha256']
assert sha((R/'parent-source.json').read_bytes())==s['reference']['parent_source_sha256']
assert sha((R/'parent-manifest.json').read_bytes())==s['reference']['parent_manifest_sha256']
assert sha((W/'capture.py').read_bytes())==s['driver_sha256']
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ii=list(cs.disasm(code,0x3D8F3F))
assert sum(i.size for i in ii)==58 and not any(i.mnemonic.startswith('j') or i.mnemonic=='call' for i in ii)
assert [(i.address,i.op_str) for i in ii if i.mnemonic in ('mulss','subss')]==[(0x3D8F52,'xmm1, xmm0'),(0x3D8F5D,'xmm0, dword ptr [rip + 0x1b20497]'),(0x3D8F6D,'xmm1, xmm0')]
assert len(s['cases'])==3
original,control,mutant=s['cases']
for c in s['cases']:
 assert c['failure'] is None and c['stop_pc']=='0x3d8f79' and c['rsp_after']==c['input']['rsp']
 assert c['visited']==[hex(i.address) for i in ii]
 assert c['input']['mxcsr']=='0x1f80' and int(c['mxcsr_after'],16)&0xFFC0==0x1F80
 assert [(x['pc'],x['address'],len(bytes.fromhex(x['bytes']))) for x in c['writes']]==[('0x3d8f44','0x22d8f30',8),('0x3d8f56','0x22d92e0',16),('0x3d8f65','0x22d91a0',4),('0x3d8f71','0x22d92e0',4)]
 assert c['after']['0x60001830']==c['before']['0x60001830'] and c['after']['0x1ef93fc']==c['before']['0x1ef93fc']=='0000803f'
 assert int.from_bytes(bytes.fromhex(c['after']['0x22d92e0'])[:4],'little')==int(c['output_bits'],16)
 assert c['writes'][-1]['bytes']==c['after']['0x22d92e0'][:8]
 assert any(x['address']=='0x1ef93fc' and x['pc']=='0x3d8f5d' for x in c['reads'])
for c in (original,control):
 assert not c['mutated'] and c['running_code_sha256']==sha(code) and c['output_bits']==c['model']['original_order']
assert original['output_bits']=='0x3d1999a0' and original['model']['factored']=='0x3d1999a4'
assert control['output_bits']==control['model']['factored'] # disagreement is input-sensitive
assert mutant['mutated'] and mutant['running_code_sha256']!=sha(code) and mutant['output_bits']!=mutant['model']['original_order']
assert mutant['writes'][-1]['bytes']!=original['writes'][-1]['bytes'] # observer sees altered consequence, not return-only
assert len(set(s['failed_discriminator']['prediction'].values()))==1
v=dict(status='PASS_ORIGINAL_WINDOW',claims_established=['For injected sample3F900001 and amplitude3E99999A under MXCSR1F80, original result3D1999A0 differs from factored3D1999A4.',
 'MULSS(sample,A), MULSS(A,1), then SUBSS is required for these exact bits; power-of-two agreement alone cannot distinguish.',
 'Four write transitions and read-only input/constant controls verified; subtract-to-add mutation changes observed stored result.'],
 limitations=s['limits'],original_cases=2,explicit_mutant_controls=1,live_cases=0,cleanup=s['cleanup'])
if (W/'manifest.json').exists():assert json.loads((W/'validation.json').read_text())==v
else:(W/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('PASS original58B arithmetic: 3D1999A0 != factored3D1999A4; exact-control and mutation/write detector pass. Native invocation/live effects unobserved.',flush=True)
