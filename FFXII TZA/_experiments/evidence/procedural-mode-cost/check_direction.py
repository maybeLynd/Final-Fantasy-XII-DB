import hashlib,json
from pathlib import Path
import capstone
from operand_direction import memory_role
W=Path(__file__).resolve().parent
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
# Real shipping wrapper store/load/LEA, not a synthetic test invented for count.
old=json.loads((W/'retained/matrix-buffer-alias-source.json').read_text())
body=next(x for x in old['bodies'] if x['entry']=='0x202b70')
ii={i.address:i for i in cs.disasm(bytes.fromhex(body['raw_hex']),0x202B70)}
store=ii[0x202B86];load=ii[0x202B83];lea=ii[0x202B79]
assert store.bytes.hex()=='0f1103' and memory_role(store,0)=='write'
assert load.bytes.hex()=='0f1000' and memory_role(load,1)=='read'
assert lea.bytes.hex()=='488d4c2420' and memory_role(lea,1)=='address'
assert not(store.operands[0].access&capstone.CS_AC_WRITE) # actual old classifier would miss this write
fix=json.loads((W/'matrix-buffer-alias-access-correction.json').read_text())
assert fix['parent_source_sha256']==hashlib.sha256((W/'retained/matrix-buffer-alias-source.json').read_bytes()).hexdigest()
assert {x['pc']:x['corrected'] for x in fix['changes']}=={'0x202b79':'address','0x202b86':'write'}
expected=[]
for b in old['bodies']:
 assert hashlib.sha256(bytes.fromhex(b['raw_hex'])).hexdigest()==b['sha256']
 for i in cs.disasm(bytes.fromhex(b['raw_hex']),int(b['entry'],16)):
  for k,o in enumerate(i.operands):
   if o.type==capstone.CS_OP_MEM:
    expected.append(dict(pc=hex(i.address),op=i.mnemonic,operand=k,base=cs.reg_name(o.mem.base),index=cs.reg_name(o.mem.index),disp=o.mem.disp,width=o.size,access=memory_role(i,k),capstone_access_flag=o.access,bytes=i.bytes.hex()))
assert expected==fix['memory_operands'] and expected
current=json.loads((W/'source.json').read_text())
assert next(x for x in current['rip_references'] if x['pc']=='0x3d8f56')['access']=='write'
assert next(x for x in current['rip_references'] if x['pc']=='0x3d8fd5')['access']=='write'
assert next(x for x in current['rip_references'] if x['pc']=='0x3d8e6c')['access']=='address'
# A source form outside this exact helper vocabulary must not inherit READ.
unsupported=next(cs.disasm(bytes.fromhex('ff00'),0)) # INC [RAX]
try:memory_role(unsupported,0)
except ValueError:pass
else:raise AssertionError('unsupported memory form must fail closed')
print('PASS actual packed-store regression + load/LEA controls; unsupported form rejects. A metadata only, no original execution.',flush=True)
