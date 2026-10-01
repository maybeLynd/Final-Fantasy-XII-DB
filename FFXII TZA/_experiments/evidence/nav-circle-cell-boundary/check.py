"""Readonly source/path/value reduction of the one bounded predicate capture."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());source=json.loads((W/'source.json').read_text());assert raw['source']==source
assert source['driver_sha256']==sha((W/'prepare.py').read_bytes())
assert raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'capture-before-run.py').read_bytes())
ref=source['reference'];code=(R/'original237.bin').read_bytes();caller=(R/'caller679.bin').read_bytes()
assert len(code)==237 and sha(code)==ref['body_sha256'] and sha(caller)==ref['caller_sha256']
assert sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256'] and sha((R/'reg_tracking.py').read_bytes())==ref['policy_sha256']
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image()
assert sha(image)==ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and code==rd.img_rd(image,ss,0x4690B0,237) and caller==rd.img_rd(image,ss,0x392200,679)
sp=importlib.util.spec_from_file_location('roles',R/'reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;seq=list(cs.disasm(code,0x4690B0));ins={i.address:i for i in seq}
records=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in seq]
assert records==source['instructions'] and len(seq)==67 and sum(i.size for i in seq)==237 and not any(i.mnemonic=='call' for i in seq)
assert all(m['kind']=='r' and m['size']==4 and m['base'] in ['rcx','rdx'] and not m['index'] for x in records for m in x['memory'])
assert {m['disp'] for x in records for m in x['memory'] if m['base']=='rcx'}=={0,8,0x10,0x18}
assert {m['disp'] for x in records for m in x['memory'] if m['base']=='rdx'}=={0,8,0x10}
parent={i.address:i for i in cs.disasm(caller,0x392200)}
assert parent[0x3923CD].mnemonic=='call' and parent[0x3923CD].operands[0].imm==0x4690B0 and parent[0x3923D4].mnemonic=='je' and parent[0x3923D4].operands[0].imm==0x39242E
assert parent[0x392482].mnemonic=='call' and parent[0x392482].operands[0].imm==0x808C40
old=(R/'flow.py').read_text();prefix=old[:old.index('adm = table(ADM)')];ns={'__file__':str(Path.cwd()/'Database/Tools/work/ASTRA/uc1-band-ruling/review.py')};exec(compile(prefix,'unchanged bounded flow definitions','exec'),ns)
flow=ns['flow'](0x4690B0,237,code);assert flow['full_linear'] and not flow['problems'] and all(x[4] for x in flow['instructions']) and {tuple(x) for x in flow['exits']}=={('0x4690f0','ret'),('0x46919c','ret')}
assert ns['flow'](0x4690B0,236,code[:-1])['problems']
for pc in [0x469147,0x469165,0x469182]:assert ins[pc].mnemonic=='ja' and ins[pc].operands[0].imm==0x4690EB
assert ins[0x469199].mnemonic=='seta' and ins[0x46911E].mnemonic=='jae'
cases=raw['cases'];assert cases==json.loads((W/'in-progress-cases.json').read_text()) and len(cases)==10 and len({c['name'] for c in cases})==10
expected=[('positive-inside',1),('negative-distant',0),('edge-tangent',1),('corner-min-min-tangent',0),('corner-min-max-tangent',0),('corner-max-min-tangent',0),('corner-max-max-tangent',0),('corner-first-radius-next-up',1),('corner-first-radius-next-down',0),('corner-first-private-inclusive',1)]
f=lambda n:struct.unpack('<f',struct.pack('<I',n))[0]
b=lambda v:struct.unpack('<I',struct.pack('<f',v))[0]
observations=[]
for c,(name,want) in zip(cases,expected):
 assert c['name']==name and c['failure'] is None and c['initial']['mxcsr']=='0x1f80' and c['initial']['eflags']=='0x2'
 initial=c['initial'];assert (initial['rcx'],initial['rdx'],initial['rsp'],initial['sentinel'])==('0x40000100','0x40000200','0x60001808','0x60000200')
 rectangle=bytes.fromhex(initial['rectangle']);circle=bytes.fromhex(initial['circle']);stack=bytes.fromhex(initial['stack'])
 assert len(rectangle)==32 and len(circle)==24 and len(stack)==80 and struct.unpack_from('<Q',stack)[0]==0x60000200
 assert all(struct.unpack_from('<f',rectangle,o)[0]==v for o,v in [(0,0.),(8,0.),(0x10,10.),(0x18,10.)])
 assert [struct.unpack_from('<I',circle,o)[0] for o in [0,8,0x10]]==[int(c[k],16) for k in ['x_bits','z_bits','radius_bits']]
 assert all(rectangle[o:o+4]==b'\xa5'*4 for o in [4,12,20,28]) and all(circle[o:o+4]==b'\xa5'*4 for o in [4,12,20])
 running=bytearray(code)
 if c['mutated']:running[0x469147-0x4690B0]=0x73
 assert c['mutated']==(name==expected[-1][0]) and c['running_hex']==running.hex() and sha(running)==c['running_sha256'] and (sha(running)==ref['body_sha256'])!=c['mutated']
 si={i.address:i for i in cs.disasm(running,0x4690B0)}
 # A bounded arithmetic/path replay validates the raw instrument. The original-code
 # capture, not this host replay, is the evidence of shipping effects for these values.
 registers={f'xmm{j}':0xA5A5A5A5 for j in range(6)};eax=0xA5A5A5A5;cf,zf=0,0;pc=0x4690B0;visits=[];reads=[];comp=[]
 def value(i,o):
  if o.type==capstone.CS_OP_REG:return registers[i.reg_name(o.reg)]
  assert o.type==capstone.CS_OP_MEM
  base=i.reg_name(o.mem.base);buf,address=(rectangle,0x40000100) if base=='rcx' else (circle,0x40000200);data=buf[o.mem.disp:o.mem.disp+4]
  reads.append(dict(pc=hex(i.address),address=hex(address+o.mem.disp),size=4,bytes=data.hex()));return struct.unpack('<I',data)[0]
 for step in range(128):
  i=si[pc];visits.append(hex(pc));next_pc=pc+i.size;op=i.mnemonic;os=i.operands
  if op in ['movss','movaps']:registers[i.reg_name(os[0].reg)]=value(i,os[1])
  elif op in ['addss','subss','mulss']:
   dst=i.reg_name(os[0].reg);x,y=f(registers[dst]),f(value(i,os[1]));registers[dst]=b(x+y if op=='addss' else x-y if op=='subss' else x*y)
  elif op=='comiss':
   vals=[]
   for o in os:
    v=value(i,o);vals.append(f'{v:08x}' if o.type==capstone.CS_OP_REG else struct.pack('<I',v).hex())
   comp.append(dict(pc=hex(pc),args=i.op_str,operands=vals));x,y=[f(int(v,16)) if o.type==capstone.CS_OP_REG else struct.unpack('<f',bytes.fromhex(v))[0] for v,o in zip(vals,os)];cf,zf=int(x<y),int(x==y)
  elif op in ['jb','ja','jae']:
   if (cf if op=='jb' else not cf and not zf if op=='ja' else not cf):next_pc=os[0].imm
  elif op=='mov':assert i.op_str=='eax, 1';eax=1
  elif op=='xor':assert i.op_str=='eax, eax';eax=0;cf,zf=0,1
  elif op=='seta':assert i.op_str=='al';eax=(eax&~255)|int(not cf and not zf)
  elif op=='ret':
   reads.append(dict(pc=hex(pc),address='0x60001808',size=8,bytes=stack[:8].hex()));break
  else:raise AssertionError(('Unexpected replay instruction',op))
  pc=next_pc
 else:raise AssertionError('Incomplete replay cannot pass')
 assert visits==c['visits'] and reads==c['reads'] and comp==[{k:x[k] for k in ['pc','args','operands']} for x in c['comparisons']]
 assert eax==c['after']['eax']==want and c['after']['rax']==hex(eax) and not c['writes'] and c['after']['stop_pc']=='0x60000200' and c['after']['rsp']=='0x60001810'
 assert all(c['after'][k]==initial[k] for k in ['rectangle','circle','stack']) and int(c['after']['mxcsr'],16)&~0x3F==0x1F80
 observations.append(dict(name=name,x_bits=c['x_bits'],z_bits=c['z_bits'],radius_bits=c['radius_bits'],eax=eax,return_site=visits[-1],instructions=len(visits),read_events=len(reads),mutated=c['mutated'],comparisons=comp))
assert observations[2]['comparisons'][0]['operands']==['c0a00000','c0a00000']
for item,pc in zip(observations[3:7],[0x469144,0x469162,0x46917F,0x469196]):
 assert next(x for x in item['comparisons'] if x['pc']==hex(pc))['operands']==['41c80000','41c80000']
assert observations[7]['comparisons'][-1]['operands']==['41c80003','41c80000'] and observations[8]['comparisons'][3]['operands']==['41c7fffe','41c80000']
for x in raw['tools']['providers']:assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
assert sha(Path(sys.executable).read_bytes())==raw['tools']['python_sha256']
result=dict(method=raw['method'],reference=ref,observations=observations,interpretation='Source has two inclusive expanded-edge bands followed by four strict radius-squared greater-than corner-distance-squared tests. In finite injected0..10/radius5 cases, exact side tangency accepts, exact3-4-5 corner tangency rejects at every corner; radius next-up accepts first corner, next-down rejects. Private first JA->JAE accepts the same first-corner tangent and is refused as original. Native shape state/MXCSR/normal reachability not proved; floating-point instruction order must be retained rather than substituted by generic inclusive geometry.',limits=raw['limits'],cleanup=raw['cleanup'])
if (W/'result.json').exists():assert json.loads((W/'result.json').read_text())==result
else:(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
if (W/'manifest.json').exists():
 for x in json.loads((W/'manifest.json').read_text())['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_CIRCLE_CELL55 original237B/67 reachable/fullRET/source-layout/defaultsharedreads/complete10paths/immutablearguments/edge inclusive/four strictcorner tangencies/adjacent radii/privateJA-JAE detector; no live state proof')
