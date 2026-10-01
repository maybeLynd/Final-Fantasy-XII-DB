"""Readonly independent reduction of original instruction effects and controls."""
import hashlib,importlib.util,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());source=json.loads((W/'source.json').read_text());assert raw['source']==source
ref=source['reference'];assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert source['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
assert sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256'] and sha((R/'reg_tracking.py').read_bytes())==ref['policy_sha256']
for x in source['tools']['providers']:assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)==ref['exe_sha256']
sp=importlib.util.spec_from_file_location('roles',R/'reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
body=(R/'parent679.bin').read_bytes();code=(R/'write-window88.bin').read_bytes();START,END=0x3923D6,0x39242E
assert body==rd.img_rd(d,ss,0x392200,679) and sha(body)==ref['parent_sha256'] and code==body[START-0x392200:END-0x392200] and len(code)==88 and sha(code)==ref['window_sha256']
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;seq=list(cs.disasm(code,START));parent={i.address:i for i in cs.disasm(body,0x392200)}
records=[]
for i in seq:
 records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
assert records==source['instructions'] and sum(i.size for i in seq)==88 and not any(i.mnemonic.startswith('j') or i.mnemonic in ['call','ret'] for i in seq)
assert parent[0x3923CD].operands[0].imm==0x4690B0 and parent[0x3923D2].op_str=='eax, eax' and parent[0x3923D4].mnemonic=='je' and parent[0x3923D4].operands[0].imm==END
for pc,j,target in [(0x3923D6,1,0x2AEE060),(0x3923F4,1,0x2AEE0A0),(0x3923FD,1,0x2AEE0B8),(0x392416,1,0x2AEE060),(0x392424,1,0x2AEE0A8)]:
 i=parent[pc];o=i.operands[j];assert o.type==capstone.CS_OP_MEM and i.address+i.size+o.mem.disp==target
for pc,args in [(0x3923DC,'eax, r12d'),(0x3923DF,''),(0x3923E3,'edx, 7'),(0x3923E6,'eax, edx'),(0x3923EB,'eax, 7'),(0x3923EE,'eax, edx'),(0x3923F0,'r8d, 3'),(0x39240F,'ecx, eax')]:assert parent[pc].op_str==args
assert parent[0x3923DF].mnemonic=='cdq' and parent[0x3923F0].mnemonic=='sar' and parent[0x39240F].mnemonic=='bts'
assert parent[0x392412].mnemonic=='mov' and parent[0x392412].operands[0].size==1 and roles.op_kind(parent[0x392412],parent[0x392412].operands[0],0)=='w'
assert parent[0x39242B].mnemonic=='inc' and parent[0x39242B].operands[0].size==1 and roles.op_kind(parent[0x39242B],parent[0x39242B].operands[0],0)=='rw'
ext=source['extents'];assert len(ext)==3 and ext[0]['entry']=='0x392200' and ext[-1]['end']=='0x3924a7'
refs={(x['entry'],x['end'],x['unwind']):x for x in ext};root=(ext[0]['entry'],ext[0]['end'],ext[0]['unwind']);last=0x392200
for x in ext:
 rec=rd.img_rd(d,ss,rd.IMG_LO+int(x['directory_rva'],16)+x['record_offset'],12);assert rec.hex()==x['record_hex'];a,e,u=struct.unpack('<III',rec)
 assert [hex(v+rd.IMG_LO) for v in [a,e,u]]==[x['entry'],x['end'],x['unwind']]
 ub=bytes.fromhex(x['unwind_hex']);assert rd.img_rd(d,ss,int(x['unwind'],16),len(ub))==ub and ub[0]>>3==x['flags']
 assert int(x['entry'],16)==last;last=int(x['end'],16);cur=x;seen=set()
 while cur['flags']==4:
  key=(cur['entry'],cur['end'],cur['unwind']);assert key not in seen;seen.add(key)
  u=bytes.fromhex(cur['unwind_hex']);off=4+((u[2]+1)//2)*4;chain=tuple(hex(v+rd.IMG_LO) for v in struct.unpack_from('<III',u,off));assert chain==tuple(cur['chain']);cur=refs[chain]
 assert (cur['entry'],cur['end'],cur['unwind'])==root
assert last==0x3924A7
cases=raw['cases'];assert len(cases)==8 and len({x['name'] for x in cases})==8 and cases==json.loads((W/'in-progress-cases.json').read_text())
expected_inputs=[(0,0,0,False),(287,0,0,False),(288,0,0,False),(288,1,0,False),(-1,0,0,False),(-8,0,0,False),(0,0,255,False),(0,0,255,True)]
observations=[]
for c,(id_,col,occ,mutated) in zip(cases,expected_inputs):
 a=c['initial'];assert (a['id'],a['col'],a['occupancy'],c['mutated'])==(id_,col,occ,mutated) and a['row']==0
 assert a['layout']==dict(width=2,stride=36,records_base='0x40000100',records_bytes=72,occupancy_base='0x40000148',occupancy_bytes=2,scratch_bytes=36)
 running=bytearray(code)
 if mutated:running[0x39242B-START:0x39242B-START+3]=b'\x90'*3
 assert c['running_hex']==bytes(running).hex() and sha(running)==c['running_sha256']
 assert (sha(running)==ref['window_sha256'])!=mutated
 assert c['failure'] is None and c['after']['stop_pc']==hex(END) and c['after']['r12d']==hex(id_&0xFFFFFFFF)
 assert c['visits']==[hex(i.address) for i in cs.disasm(running,START)] and 0<len(c['visits'])<128
 lo=int(a['focus_address'],16);before=bytes.fromhex(a['focus_bytes']);after=bytes.fromhex(c['after']['focus_bytes']);assert lo==0x400000F0 and len(before)==len(after)==142
 expected=bytearray(before);q=(abs(id_)//8)*(-1 if id_<0 else 1);rem=id_-q*8;address=0x40000100+col*36+q
 first=expected[address-lo]|((1<<(rem&31))&0xFF);expected[address-lo]=first
 writes=[dict(pc='0x392412',address=hex(address),size=1,bytes=f'{first:02x}')]
 if not mutated:
  p=0x40000148+col;value=(expected[p-lo]+1)&0xFF;expected[p-lo]=value;writes.append(dict(pc='0x39242b',address=hex(p),size=1,bytes=f'{value:02x}'))
 assert after==expected and c['post_write_bytes']==writes
 assert len(c['raw_writes'])==len(writes) and c['reads']
 for rw,w in zip(c['raw_writes'],writes):assert (rw['pc'],rw['address'],rw['size'])==(w['pc'],w['address'],w['size']) and (rw['provider_value']&255)==int(w['bytes'],16)
 changed=[dict(address=hex(lo+j),before=f'{x:02x}',after=f'{y:02x}') for j,(x,y) in enumerate(zip(before,after)) if x!=y];assert changed==c['after']['changed']
 expected_region='bitset-record0' if 0x40000100<=address<0x40000124 else 'bitset-record1' if 0x40000124<=address<0x40000148 else 'occupancy0' if address==0x40000148 else 'prefix-guard'
 observations.append(dict(name=c['name'],injected_id=id_,col=col,signed_quotient=q,signed_remainder=rem,bitmap_write_address=hex(address),bitmap_write_region=expected_region,bitmap_after=f'{first:02x}',occupancy_after=f'{after[0x40000148+col-lo]:02x}',write_events=len(writes),changed=changed,mutated=mutated))
assert observations[1]['bitmap_after']=='80' and observations[2]['bitmap_write_region']=='bitset-record1' and observations[3]['bitmap_write_region']=='occupancy0'
assert observations[4]['bitmap_after']=='00' and observations[4]['write_events']==2 and observations[5]['bitmap_write_region']=='prefix-guard' and observations[5]['bitmap_after']=='a5'
assert observations[6]['occupancy_after']=='00' and observations[7]['occupancy_after']=='ff' and observations[7]['write_events']==1
result=dict(method=raw['method'],reference=ref,observations=observations,interpretation='Under injected accepted-overlap entry and valid two-cell layout, shipping88B uses signed ID quotient/remainder and BTS register low-bit index, stores only CL, then increments occupancy modulo256. ID288 writes next record or occupancy depending cell; negative1 leaves low bitmap byte unchanged yet increments occupancy, negative8 writes preceding byte. No ID rejection within this executed fragment. Private NOP-INC detected as one write/no counter increment and rejected as original. These are isolated effects, not native geometry acceptance/normal reachability/race/live failure.',limits=raw['limits'],cleanup=raw['cleanup'])
labels=R/'label-correction'
if not labels.exists():labels=W/'label-correction'
if labels.exists():
 diag=json.loads((labels/'diagnostic.json').read_text());old=json.loads((labels/'result-before.json').read_text())
 assert diag['raw_sha256']==sha((W/'raw.json').read_bytes()) and diag['status']=='PRE_PUBLICATION_REGION_LABEL_CORRECTION'
 for o in old['observations']:o['bitmap_write_region']=o['bitmap_write_region'].replace('pointer-record','bitset-record')
 assert old==result,'Only the mistaken region labels were corrected; raw cases and other normalized claims must be preserved'
if (W/'result.json').exists():assert json.loads((W/'result.json').read_text())==result
else:(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for x in source['tools']['providers']:assert sha(Path(x['path']).read_bytes())==x['sha256']
if (W/'manifest.json').exists():
 for x in json.loads((W/'manifest.json').read_text())['members']:
  b=(W/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
print('PASS_MARK_WRITE exactshipping88B/parent679B/PEchains/defaultstore-RMW/completepaths/two ordered bytewrites/IDsigned-and-boundary/occupancywrap/NOP observercontrol; no native geometry/live safety claim')
