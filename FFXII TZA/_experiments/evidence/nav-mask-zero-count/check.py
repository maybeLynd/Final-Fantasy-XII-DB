import hashlib,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
r=json.loads((W/'result.json').read_text());ref=r['reference'];assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert r['driver_sha256']==sha((W/'derive.py').read_bytes()) and ref['reader_sha256']==sha((W/'retained/shipping-reader.py').read_bytes())
raw=(W/'retained/body.bin').read_bytes();assert len(raw)==292 and sha(raw)==ref['body_sha256'] and ref['pe_function'][:2]==['0x3912e0','0x391404']
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(raw,0x3912E0)};assert sum(i.size for i in ii.values())==292
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii.values()]
for test,jns,zero,jmp,upper,cmp,cmov,end,reg in [(0x39131A,0x39131C,0x39131E,0x391320,0x391322,0x391326,0x391328,0x39132B,'esi'),(0x391332,0x391334,0x391336,0x391338,0x39133A,0x39133D,0x39133F,0x391342,'ebx'),(0x391342,0x391344,0x391346,0x391348,0x39134A,0x39134E,0x391350,0x391353,'edi'),(0x391353,0x391355,0x391357,0x391359,0x39135B,0x39135E,0x391360,0x391363,'ebp')]:
 assert (ii[test].mnemonic,ii[test].op_str)==('test',reg+', '+reg)
 assert ii[jns].mnemonic=='jns' and ii[jns].operands[0].imm==upper
 assert (ii[zero].mnemonic,ii[zero].op_str)==('xor',reg+', '+reg)
 assert ii[jmp].mnemonic=='jmp' and ii[jmp].operands[0].imm==end
 assert ii[upper].mnemonic=='lea' and ii[upper].reg_name(ii[upper].operands[0].reg)=='eax' and ii[upper].operands[1].mem.disp==-1
 assert (ii[cmp].mnemonic,ii[cmp].op_str)==('cmp',reg+', eax') and (ii[cmov].mnemonic,ii[cmov].op_str)==('cmovg',reg+', eax')
for pc,dest in [(0x3912F9,0x2AEE0B8),(0x391302,0x2AEE0B0),(0x391313,0x2AEE060),(0x39132B,0x2AEE064),(0x391380,0x2AEE0A8)]:
 i=ii[pc];assert i.address+i.size+i.operands[1].mem.disp==dest
assert ii[0x39130E].mnemonic=='call' and ii[0x39130E].operands[0].imm==0x861EC0
assert [(ii[x].mnemonic,ii[x].op_str) for x in (0x391363,0x391374,0x39138A,0x39138E,0x391391,0x391394)]==[('cmp','ebx, ebp'),('cmp','esi, edi'),('imul','r8d, ebx'),('add','r8d, r10d'),('movsxd','rcx, r8d'),('cmp','byte ptr [rcx + rax], 0')]
assert len(r['cases'])==15
for x in r['cases']:
 i,c=x['input'],x['count'];assert x['original_conditional']==(0 if i<0 else min(i,c-1)) and x['naive_min_max']==min(max(i,0),c-1) and x['opposite_order_max_min']==max(min(i,c-1),0)
 if c>0:assert 0<=x['original_conditional']<c
assert [x['first_signed_cell_index'] for x in r['rectangles']]==[0,-1,0,None]
for x in r['rectangles']:
 coords=[0 if i<0 else min(i,x['cols']-1) for i in x['inputs']];assert coords==x['clamped']
 enter=coords[1]<=coords[3] and coords[0]<=coords[2];assert enter==x['rectangle_loop_enters'] and x['first_signed_cell_index']==(coords[0]+coords[1]*x['cols'] if enter else None)
assert r['source_mutation_rejected'] and len(r['producer_controls'])==2
for c in r['producer_controls']:
 assert c['checker_sha256']==sha((W/'retained/conv_check.py').read_bytes()) and c['page_sha256']==sha((W/'retained/contract.md').read_bytes()) and c['checker_exit']==0 and 'PASS  X3' in c['stdout'] and 'FAILS 0' in c['stdout']
assert r['producer_controls'][0]['patch'] is None and r['producer_controls'][0]['input_sha256']==ref['exe_sha256']
assert r['producer_controls'][1]['patch']['before']=='eb09' and r['producer_controls'][1]['patch']['after']=='9090' and r['producer_controls'][1]['input_sha256']!=ref['exe_sha256']
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_STATIC_PIECEWISE original4negative-bypass/upper-signed clamps, count0/positive source cases/loop-read consequences, actualX3blindness and source-mutant rejection; no original-code/live execution')
