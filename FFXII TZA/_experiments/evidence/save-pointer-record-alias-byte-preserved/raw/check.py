import hashlib,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((W/'retained/source.json').read_text());r=json.loads((W/'result.json').read_text())
assert r['source_sha256']==sha((W/'retained/source.json').read_bytes())
assert r['driver_sha256']==sha((W/'derive.py').read_bytes()) and r['contract_sha256']==sha((W/'retained/contract.md').read_bytes())
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii={}
for z in s['bodies']:
 raw=bytes.fromhex(z['raw_hex']);assert sha(raw)==z['sha256']
 ins=list(cs.disasm(raw,int(z['entry'],16)));assert sum(i.size for i in ins)==z['size'] and ins[-1].mnemonic=='ret'
 assert all(i.mnemonic!='call' for i in ins)
 ii.update({i.address:i for i in ins})
def mem(pc,k,base,index,disp,width):
 i=ii[pc];o=i.operands[k];assert o.type==capstone.CS_OP_MEM
 assert (i.reg_name(o.mem.base),i.reg_name(o.mem.index),o.mem.disp,o.size)==(base,index,disp,width)
 return i
store=mem(0x36D969,0,'r8',None,0,8)
load=mem(0x36D974,1,'rax',None,0,16)
assert store.mnemonic=='mov' and store.reg_name(store.operands[1].reg)=='rax'
assert load.mnemonic=='movups' and store.address<load.address
assert ii[0x36D953].address+ii[0x36D953].size+ii[0x36D953].operands[1].mem.disp==0x2EC0800
assert ii[0x36D95A].address+ii[0x36D95A].size+ii[0x36D95A].operands[1].mem.disp==0x2EC0A00
mem(0x36D977,0,'r9',None,-16,16)
mem(0x36D8FE,1,'r9','rax',0x2DA0A00,8)
mem(0x36D906,1,'r9','rcx',0x2DA0800,16)
mem(0x36D90F,0,'rax',None,0,16)
entry=bytes(range(0x10,0x20));changed=struct.pack('<Q',0x2EC0A00)+entry[8:]
assert len(r['cases'])==4
a,b,c,d=r['cases']
assert a['entry_hex']==entry.hex() and a['snapshot_hex']==changed.hex()==a['after_restore_hex'] and not a['entry_restored']
assert all(x['entry_restored'] and x['snapshot_hex']==entry.hex() for x in (b,c,d))
assert all(x['initial_depth']==0 and x['count']==1 and x['counter_disjoint'] and x['final_depth']==0 for x in r['cases'])
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  raw=(W/x['path']).read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
print('PASS_STATIC_CONDITIONAL: exact original pointer-store BEFORE target-load; count1 pointer-slot alias versus disjoint/value-self/load-first controls. No native/live execution.')
