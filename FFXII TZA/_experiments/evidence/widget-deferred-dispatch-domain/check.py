"""Read-only source, branch, provenance and actual producer-invocation checks."""
import hashlib,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();r=json.loads((W/'result.json').read_text());ref=r['reference'];code=(R/'source.bin').read_bytes();entry=0x244DD0
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and ref['entry']==hex(entry) and ref['bytes']==len(code)==301 and sha(code)==ref['body_sha256']=='24c646adcf49060e7fc09e19b0c2ae75077a9c7e0ea7d2c2a09daad9d139b454'
assert r['driver_sha256']==sha((W/'derive.py').read_bytes()) and sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256']=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
old=json.loads((R/'prior-body.json').read_text());assert b''.join(bytes.fromhex(x['bytes']) for x in old['instructions'])==code and old['sha256']==sha(code)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,entry));ii={i.address:i for i in ins};assert sum(i.size for i in ins)==301
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins]
for a,h in {0x244DD3:'0f8423010000',0x244E1D:'750d',0x244E1F:'83637cf1',0x244E23:'834b7c01',0x244E27:'e9b3000000',0x244E2F:'c1e11c',0x244E32:'c1f91c',0x244E37:'740e',0x244E39:'83e902',0x244E3C:'7424',0x244E3E:'83f901',0x244E41:'0f85b0000000',0x244E62:'0fbae210',0x244E66:'7305',0x244E6A:'894b70',0x244E73:'03c0',0x244E75:'2b4370',0x244E78:'2b4374',0x244E7B:'894374',0x244E7E:'eb57',0x244ED7:'83637cf4',0x244EDB:'834b7c04',0x244EDF:'834b7c30',0x244EE9:'740c',0x244EF5:'ffd0'}.items():assert ii[a].bytes.hex()==h,(hex(a),'exact original source obligation')
for a,d in [(0x244DD3,0x244EFC),(0x244E1D,0x244E2C),(0x244E27,0x244EDF),(0x244E37,0x244E47),(0x244E3C,0x244E62),(0x244E41,0x244EF7),(0x244E66,0x244E6D),(0x244E7E,0x244ED7),(0x244EE9,0x244EF7)]:assert ii[a].operands[0].imm==d
assert ii[0x244E1A].op_str=='dl, 1' and ii[0x244E17].op_str=='edx, dword ptr [rbx + 0x40]' and ii[0x244E2C].op_str=='ecx, dword ptr [rbx + 0x7c]'
assert ii[0x244E35].op_str=='ecx, ecx' and ii[0x244E3E].op_str=='ecx, 1'
assert ii[0x244E6D].address+ii[0x244E6D].size+ii[0x244E6D].operands[1].mem.disp==0x208F570
assert struct.unpack('<QQQ',(R/'notification-record.bin').read_bytes())==(15,0,0) and ii[0x244EEB].address+ii[0x244EEB].size+ii[0x244EEB].operands[1].mem.disp==0x1E0C0F8
extent=json.loads((R/'extent-proof.json').read_text());assert extent['ranges']==ref['pe_ranges']
def complete_extent(rows):
 assert rows and rows[0]['start']=='0x244dd0' and rows[-1]['end_exclusive']=='0x244efd','Whole301B must not be truncated to root123B'
 last=entry;root=[rows[0]['start'],rows[0]['end_exclusive'],rows[0]['unwind']]
 for j,x in enumerate(rows):
  assert int(x['start'],16)==last;last=int(x['end_exclusive'],16);data=bytes.fromhex(x['raw_hex']);count=data[2];length=4+((count*2+3)//4)*4;assert data[0]&7==1 and data[0]>>3==x['flags']
  if j:assert x['flags']==4 and x['chain']==root and len(data)==length+12 and [hex(v+0x120000) for v in struct.unpack_from('<III',data,length)]==root
  else:assert x['flags']==0 and x['chain'] is None and len(data)==length
 assert last-entry==301
complete_extent(extent['ranges']);extent_rejected=False
try:complete_extent(extent['ranges'][:1])
except AssertionError:extent_rejected=True
assert extent_rejected and len(extent['ranges'])==5
failure=json.loads((R/'initial-failure.json').read_text());assert failure['result']=='INVALID_PREFLIGHT, no semantic result published, no native/game tests' and failure['observed_first_length']==123 and failure['driver_sha256']==sha((R/'initial-failed-derive.py').read_bytes())
modes=r['active_gate_modes'];assert len(modes)==16
for n,c in enumerate(modes):
 assert c['flags40']=='00000001' and c['flags7c']==f'{n:08X}' and c['signed_low_nibble']==(n if n<8 else n-16)
 tail=n in (0,2,3);assert c['shared_tail_reached']==tail and c['indirect_call_site_reached']==tail and c['arm']==('schedule' if n in (0,3) else 'rebase' if n==2 else 'early-return')
 assert c['flags7c_after_local']==('00000034' if tail else f'{n:08X}')
clear=r['controls']['mode2_bit16_clear'];set_=r['controls']['mode2_bit16_set'];special=r['controls']['bit0_clear'];null=r['controls']['null_handler']
assert not clear['zeroed70'] and clear['conditional_duration70']==10 and clear['conditional_deadline74']==170
assert set_['zeroed70'] and set_['conditional_duration70']==0 and set_['conditional_deadline74']==180
assert special['flags40']=='00000000' and special['flags7c']=='00000002' and special['flags7c_after_local']=='00000031' and special['conditional_duration70']==10 and special['conditional_deadline74']==20 and special['indirect_call_site_reached']
assert null['shared_tail_reached'] and not null['indirect_call_site_reached']
assert len(r['mutants'])==2
for m in r['mutants']:
 raw=bytes.fromhex(m['mutant_body_hex']);assert len(raw)==301 and m['original_binding_rejected'] and m['baseline']!=m['private_source_calculation']
 changed=[i for i,(a,b) in enumerate(zip(code,raw)) if a!=b];assert len(changed)==1
 if m['name']=='reversed-bit16-zero-branch':assert changed==[0x244E66-entry] and code[changed[0]]==0x73 and raw[changed[0]]==0x72 and m['baseline']['zeroed70'] and not m['private_source_calculation']['zeroed70']
 else:assert m['name']=='inverted-default-return' and changed==[0x244E42-entry] and raw[changed[0]]==0x84 and not m['baseline']['shared_tail_reached'] and m['private_source_calculation']['shared_tail_reached']
controls=r['producer_controls'];assert [x['case'] for x in controls]==['canonical-baseline','unchanged-image-guard-negative','private-mutant-certified-identity']
producer=(R/'producer.py').read_bytes();projection=(R/'producer-field-projection.tsv').read_bytes();assert projection and all(x.split(b'\t')[0] in (b'Widget',b'MapScreenContainer') for x in projection.splitlines());assert sha(projection)==json.loads((R/'field-preimage.json').read_text())['projection_sha256']
for c in controls:assert c['source_sha256']==sha(producer) and c['reference_original_sha256']==ref['exe_sha256'] and c['reads'][0]['sha256']==c['reference_sha256'] and 'open restored' in c['cleanup']
assert controls[0]['exit']==0 and controls[0]['source_sha256']==controls[0]['invoked_source_sha256'] and controls[0]['reference_sha256']==ref['exe_sha256']
assert controls[1]['exit']==2 and 'REFUSED' in controls[1]['stdout'] and len(controls[1]['reads'])==1 and controls[1]['invoked_source_sha256']==sha(producer)
assert controls[2]['exit']==0 and controls[2]['reference_sha256']==controls[1]['reference_sha256']!=ref['exe_sha256'] and controls[2]['source_change']
private=producer.replace(ref['exe_sha256'].encode(),controls[2]['reference_sha256'].encode());assert sha(private)==controls[2]['invoked_source_sha256'] and producer.count(ref['exe_sha256'].encode())==1
for c in (controls[0],controls[2]):assert 'PASS  C' in c['stdout'] and 'PASS  H' in c['stdout'] and 'PASS  G' in c['stdout'] and 'PASS  S' in c['stdout'] and 'FAILS 0' in c['stdout'] and len(c['reads'])==2 and c['reads'][1]['sha256']==sha(projection)
for n,p in [('widget-contract.md',r['consumer_preimages'][0]),('layout-entry.md',r['consumer_preimages'][1]),('producer.py',r['consumer_preimages'][2])]:assert sha((R/n).read_bytes())==p['sha256']
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  d=(W/x['path']).read_bytes();assert len(d)==x['bytes'] and sha(d)==x['sha256']
print('PASS_SOURCE_DEFERRED_DISPATCH bit16SET zeroes; bit0-clear state1 notification tail; active modes0/2/3 only. Original extent spans5 chained ranges, root-only extent rejected. Actual producer guard correct; G polarity obligation absent. No original/native/live execution.')
