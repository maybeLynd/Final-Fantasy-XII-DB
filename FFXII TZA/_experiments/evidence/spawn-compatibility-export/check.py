"""Method A: verify the shipping exporter and its complete unrolled copy extent."""
from pathlib import Path
import hashlib, json
W = Path('Database/Tools/work/ASTRA')
E = Path('Database/FFXII TZA/_experiments/evidence/spawn-compatibility-export')
ns = {}
exec((E/'primary.py').read_text().split('for a in (')[0], ns)
sha = lambda b: hashlib.sha256(b).hexdigest()
j = json.loads((E/'primary.json').read_text())
assert j['exe_sha256'] == ns['sha'] and len(j['bodies']) == 1
b = j['bodies'][0]; a = int(b['address'], 16)
assert a == 0x234ED0 and b['bytes'] == 489
raw = ns['raw'][ns['off'](a-ns['ib']):ns['off'](a-ns['ib'])+b['bytes']]
assert sha(raw) == b['sha256'] == '46ce76ee451bd778e2ac3782e52c397a1556df03e5450ff760620256b68cf57b'
fresh = list(ns['md'].disasm(raw,a))
assert sum(i.size for i in fresh) == len(raw)
assert [(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str) for i in fresh] == [(i['address'],i['bytes'],i['mnemonic'],i['operands']) for i in b['instructions']]
ins = {i.address:i for i in fresh}
assert [(i.mnemonic,i.op_str) for i in fresh if i.mnemonic.startswith('j')] == [('jl','0x234ee0')]
assert not any(i.mnemonic == 'call' for i in fresh)
assert (fresh[-1].address,fresh[-1].mnemonic) == (0x2350B8,'ret')
for address, value in {
 0x234ED0:('xor','eax, eax'),0x234ED2:('mov','r9d, 0x7374'),0x234ED8:('mov','r10d, eax'),
 0x234EE7:('lea','rax, [rax + 0x8e8]'),0x235056:('add','r9, 0x14'),0x23505D:('add','r10, 0xf'),
 0x2350AB:('cmp','r9, 0x7414'),0x2350B2:('jl','0x234ee0'),
}.items(): assert (ins[address].mnemonic,ins[address].op_str) == value
loads = [i for i in fresh if i.mnemonic == 'movsxd']
assert [i.op_str for i in loads] == ['rcx, dword ptr [r9 + r8 - 4]','rcx, dword ptr [r9 + r8]','rcx, dword ptr [r9 + r8 + 4]','rcx, dword ptr [r9 + r8 + 8]','rcx, dword ptr [r9 + r8 + 0xc]']
assert [x['rip_targets'][0]['address'] for x in b['instructions'] if 'rip_targets' in x] == ['0x2ebf190']*5
assert len([i for i in fresh if i.mnemonic == 'imul' and i.op_str == 'rdx, rcx, 0x34']) == 5
mem = ns['capstone'].x86.X86_OP_MEM
src=[]; dst=[]
for i in fresh:
 for n,op in enumerate(i.operands):
  if op.type != mem: continue
  m=op.mem
  if m.base == ns['capstone'].x86.X86_REG_RDX and m.index == ns['capstone'].x86.X86_REG_R8:
   assert n == 1; src.append((m.disp,op.size))
  if m.base == ns['capstone'].x86.X86_REG_RAX and m.index == ns['capstone'].x86.X86_REG_R8:
   assert n == 0; dst.append((m.disp,op.size))
assert src == [(0x5B10+k*0x9C+d,w) for k in range(5) for d,w in [(0,16),(16,16),(32,16),(48,4)]]
assert dst == [(-0x858+k*0x1C8+d,w) for k in range(5) for d,w in [(0,16),(16,16),(32,16),(48,4)]]
assert (0x7414-0x7374)//0x14 == 8
assert 5*8 == 40 and 40*0x34 == 0x820
rows=[]
for i in range(40):
 group,k=divmod(i,5)
 assert (group+1)*0x8E8+dst[k*4][0] == 0x90+i*0x1C8
 for sel in (0,1,2):
  assert src[k*4][0]+(group*15+sel)*0x34 == 0x5B10+(3*i+sel)*0x34
 rows.append(dict(index=i,selector_offset=0x7370+i*4,destination=[0x90+i*0x1C8,0xC4+i*0x1C8],source_bank0=0x5B10+i*0x9C))
reused=[]
for name,expected in [('helpers.json',[(0x235AF0,705)]),('capture.json',[(0x5844A0,223),(0x229B40,469)])]:
 p=E.parent/'spawn-old-save-boundary'/name; old=json.loads(p.read_text())
 for address,size in expected:
  ob=next(x for x in old['bodies'] if int(x['address'],16)==address)
  off=ns['off'](address-ns['ib']); assert ob['bytes']==size and sha(ns['raw'][off:off+size])==ob['sha256']
 reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),bodies=[hex(x[0]) for x in expected]))
fieldmap=Path('Database/FFXII TZA/11-Party/Battle-State-Block/the-battle-state-block-field-map.md')
assert 'the selected-bank index per member' in fieldmap.read_text()
out=dict(status='PASS',method='A: complete shipping source; arithmetic address normalization is analysis, not an execution test',exe_sha256=ns['sha'],body_sha256=b['sha256'],body_bytes=b['bytes'],original_execution_cases=0,copy_groups=8,records=rows,bytes_copied=0x820,reused_sources=reused,selected_bank_semantic_source=dict(path=fieldmap.as_posix(),sha256=sha(fieldmap.read_bytes())),limits=['No calls or selector/null bounds guards in this complete body. Stable initialized binding and valid selectors are caller preconditions.','Signed 32-bit selection is neither clamped nor validated. Arbitrary indices can alias other records; formula is not a promise of snapshot copies under overlapping injected states.','No live game, original-code execution, save decode or native initialization observed. Historical old-save-boundary interval key counters denotes this selected-bank array; retain receipt history.'])
(E/'check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:489 shipping bytes; all five copy lanes, eight iterations, signed selection and reused importer/writers verified. Method A only.')
