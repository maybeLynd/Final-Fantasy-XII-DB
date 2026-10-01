import hashlib,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
r=json.loads((W/'raw.json').read_text());ref=r['reference'];assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert r['driver_sha256']==sha((W/'capture.py').read_bytes())
assert sha((W/'retained/source.json').read_bytes())==ref['parent_source_sha256'] and sha((W/'retained/parent-manifest.json').read_bytes())==ref['parent_manifest_sha256']
source=json.loads((W/'retained/source.json').read_text());body=bytes.fromhex(source['raw_hex']);assert sha(body)==ref['parent_body_sha256']=='69b03e9207174ab6f16e5d56817186ec446e5348ab0025255fc8a585d064b726'
raw=(W/'retained/window.bin').read_bytes();assert len(raw)==150 and raw==body[0x1D:0xB3] and sha(raw)==ref['window_sha256']
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ins=list(cs.disasm(raw,0x3977CD));assert sum(i.size for i in ins)==150
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins]
assert [(i.address,i.bytes.hex()) for i in ins if i.mnemonic=='addss']==[(0x397844,'f30f58d0'),(0x397850,'f30f58d1'),(0x397857,'f30f58d0')]
assert ins[-1].address==0x39785E and not any(i.mnemonic in ('call','ret','jmp') for i in ins)
assert len(r['tools']['binaries'])==2 and {x['name'] for x in r['tools']['binaries']}=={'capstone','unicorn'} and all(x['bytes']>0 and len(x['sha256'])==64 for x in r['tools']['binaries'])
assert [x['name'] for x in r['cases']]==['finite-cancellation-grouping-discriminator','ordinary-integer-agreement-control','ordinary-add-to-subtract-write-detector']
mut=bytearray(raw);mut[0x397850-0x3977CD+2]=0x5C
for n,(c,expected) in enumerate(zip(r['cases'],[0,0x41200000,0x40800000])):
 initial=c['initial'];after=c['after'];assert initial['rcx']=='0x40000000' and initial['rdx']=='0x40001000' and initial['rsp']=='0x60001800' and initial['mxcsr']=='0x1f80' and initial['xmm6']==initial['xmm7']=='0x0'
 assert initial['A']==struct.pack('<16f',*([1.0]*16)).hex() and initial['snapshot']=='a5'*64
 assert c['running_code_sha256']==sha(bytes(mut) if n==2 else raw) and c['mutated']==(n==2)
 assert c['failure'] is None and c['visited']==[hex(i.address) for i in ins] and after['stop_pc']=='0x397863' and after['rsp']==initial['rsp'] and after['rax']=='0x40000020'
 assert after['B']==initial['B'] and after['snapshot']==initial['A'] and after['A'][8:]==initial['A'][8:]
 assert len(c['writes'])==5 and c['reads'] and c['raw_writes']
 for w,p,pc in zip(c['writes'][:4],[0x60001800,0x60001810,0x60001820,0x60001830],[0x3977DD,0x3977EE,0x3977FD,0x397805]):
  assert w==dict(pc=hex(pc),address=hex(p),bytes=initial['A'][(p-0x60001800)*2:(p-0x60001800+16)*2])
 assert c['writes'][-1]==dict(pc='0x39785e',address='0x40000000',bytes=expected.to_bytes(4,'little').hex()) and c['output_bits']==expected.to_bytes(4,'little').hex()
 assert any(x['pc']=='0x397821' and x['address']=='0x40001004' and x['size']==4 for x in c['reads'])
assert r['cases'][0]['host_prediction']==dict(ordered=0,balanced=0x3F800000,real_number_sum=0x40000000)
assert r['cases'][1]['host_prediction']==dict(ordered=0x41200000,balanced=0x41200000,real_number_sum=0x41200000)
assert r['cases'][2]['output_bits']!=r['cases'][1]['output_bits'] and r['cases'][2]['running_code_sha256']!=ref['window_sha256']
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_ORIGINAL_PREFIX first output ordered0 vs balanced1/real2; ordinary10 agreement and labelledADD->SUB output4 detector; exact initial/state/stop/snapshot/write/source controls, no full invocation/live proof')
