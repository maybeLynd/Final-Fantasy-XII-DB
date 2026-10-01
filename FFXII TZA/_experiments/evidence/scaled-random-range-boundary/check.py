import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((W/'raw.json').read_text());assert s['method'].startswith('B ')
r=s['reference'];assert r['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
code=(W/'retained/window.bin').read_bytes();assert len(code)==58 and sha(code)==r['window_sha256']=='f35064469004fa9448432dd22dc7c46767058dbb4c833ab86c8063ea4bc3cdd8'
assert (W/'retained/one.bin').read_bytes()==bytes.fromhex('0000803f')
assert sha((W/'retained/prior-capture.py').read_bytes())==s['observer_reuse']['prior_capture_sha256']
assert sha((W/'retained/reused-observer.txt').read_bytes())==s['observer_reuse']['adopted_function_sha256']
assert sha((W/'retained/prior-observer.txt').read_bytes())==s['observer_reuse']['prior_function_sha256']
assert s['observer_reuse']['prior_cases_not_rerun'] and len(s['tools']['binaries'])==2
assert {x['label'] for x in s['tools']['binaries']}=={'unicorn','capstone'} and s['tools']['recorded_before_capture_utc']
assert len(s['cases'])==4
# Validate actual original decode rather than guessing the instruction count.
import capstone
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);decoded=list(cs.disasm(code,0x3D8F3F));assert sum(x.size for x in decoded)==58
actualpcs=[hex(x.address) for x in decoded]
assert (decoded[0].address,decoded[0].mnemonic,decoded[0].op_str)==(0x3D8F3F,'movsxd','rax, dword ptr [rsp + 0x30]')
assert all(pc in actualpcs for pc in ('0x3d8f52','0x3d8f5d','0x3d8f6d','0x3d8f71'))
for x in s['cases']:
 assert x['failure'] is None and x['stop_pc']=='0x3d8f79' and x['visited']==actualpcs
 assert x['input']['sample_bits']=='0x3fffffff' and x['input']['mxcsr']=='0x1f80' and x['rsp_after']==x['input']['rsp']
 assert (int(x['mxcsr_after'],16)&~0x3F)==0x1F80 # Recorded actual control bits; status semantics not promoted.
 assert not any(i.mnemonic=='ldmxcsr' for i in decoded)
 assert [(w['pc'],w['address'],len(bytes.fromhex(w['bytes']))) for w in x['writes']]==[('0x3d8f44','0x22d8f30',8),('0x3d8f56','0x22d92e0',16),('0x3d8f65','0x22d91a0',4),('0x3d8f71','0x22d92e0',4)]
 assert x['before']['0x1ef93fc']==x['after']['0x1ef93fc']=='0000803f'
 assert x['initial_state']==dict(rsp=x['input']['rsp'],sample_bits='0x3fffffff',mxcsr='0x1f80')
 assert x['writes'][0]['bytes']==int(x['input']['amplitude_bits'],16).to_bytes(8,'little').hex() # Positive amplitude MOVSXD store, NOT sample.
 assert x['writes'][0]['bytes']!='ffffff3f00000000' # Small regression: distinct amplitude cannot masquerade as sample.
 assert x['before']['0x60001830']==x['after']['0x60001830']==int(x['input']['amplitude_bits'],16).to_bytes(4,'little').hex()
 assert x['writes'][-1]['bytes']==int(x['output_bits'],16).to_bytes(4,'little').hex()
 assert x['after']['0x22d92e0'][:8]==x['writes'][-1]['bytes']
 if not x['mutated']:assert x['running_code_sha256']==sha(code)
sub,normal,large,mut=s['cases']
assert not any(x['mutated'] for x in (sub,normal,large)) and mut['mutated']
assert sub['input']['amplitude_bits']=='0x1' and sub['output_bits']=='0x1'
assert normal['input']['amplitude_bits']=='0x3f000000' and normal['output_bits']=='0x3efffffe'
assert large['input']['amplitude_bits']=='0x7f7fffff' and large['output_bits']=='0x7f800000'
mutcode=bytearray(code);assert mutcode[0x3D8F6D-0x3D8F3F:0x3D8F6D-0x3D8F3F+4]==bytes.fromhex('f30f5cc8');mutcode[0x3D8F6D-0x3D8F3F+2]=0x58
assert mut['running_code_sha256']==sha(bytes(mutcode)) and mut['output_bits']=='0x3fc00000'
assert mut['writes'][-1]['bytes']!=normal['writes'][-1]['bytes'] and mut['output_bits']!=mut['model']['original_order']
v=dict(status='PASS_ORIGINAL_RANGE_WINDOW',claims=['Under injected sample3FFFFFFF/MXCSR1F80 original58B output equals smallest positive amplitude00000001, refuting universal strict out<A.', 'Largest positive finite amplitude7F7FFFFF produces +infinity7F800000 under the same controlled window, refuting universal finite range.', 'Normal0.5f control produces3EFFFFFE strictly below A; SUBSS->ADDSS control changes the stored result.'],limits=s['limits'],cleanup=s['cleanup'])
if (W/'manifest.json').exists():
 manifest=json.loads((W/'manifest.json').read_text());assert manifest['members']
 actual={p.relative_to(W).as_posix() for p in W.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=W/'manifest.json'}
 assert actual=={m['path'] for m in manifest['members']}
 for m in manifest['members']:
  b=(W/m['path']).read_bytes();assert len(b)==m['bytes'] and sha(b)==m['sha256']
if (W/'manifest.json').exists():assert json.loads((W/'validation.json').read_text())==v
elif (W/'validation.json').exists():assert json.loads((W/'validation.json').read_text())==v
else:(W/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('PASS original range window: subnormal endpoint=A, maxfinite->+inf, normal/control stores discriminate. No full/live range.',flush=True)
