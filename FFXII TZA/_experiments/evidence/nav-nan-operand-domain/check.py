"""Read-only original/source/value/path reduction; does not rerun guests."""
import hashlib,importlib.util,json,math,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());code=(R/'original237.bin').read_bytes();ref=raw['reference'];assert len(code)==237 and sha(code)==ref['body_sha256']
assert raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
assert raw['parent_runner_sha256']==sha((R/'parent-capture.py').read_bytes()) and raw['runner_sha256']==sha((R/'runner.py').read_bytes())
assert sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256']
sp=importlib.util.spec_from_file_location('reader',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)==ref['exe_sha256'] and code==rd.img_rd(image,ss,0x4690B0,237)
row_data=(R/'affected-field-row.txt').read_bytes() if '--fault-physical-row-hash' in sys.argv else (R/'affected-field-row.txt').read_text().encode()
assert 'a NaN fails every test' in (R/'affected-field-row.txt').read_text() and sha(row_data)==raw['consumer']['affected_row_sha256'], 'Normalized row identity mismatch'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;seq=list(cs.disasm(code,0x4690B0));si={i.address:i for i in seq};assert len(seq)==67 and sum(i.size for i in seq)==237 and not any(i.mnemonic=='call' for i in seq)
assert si[0x4690C7].mnemonic=='jb' and si[0x4690F4].mnemonic=='jb' and si[0x469147].mnemonic==si[0x469165].mnemonic==si[0x469182].mnemonic=='ja' and si[0x469199].mnemonic=='seta'
f=lambda u:struct.unpack('<f',struct.pack('<I',u))[0];bits=lambda v:struct.unpack('<I',struct.pack('<f',v))[0]
cases=raw['cases'];assert len(cases)==5 and cases==json.loads((W/'in-progress-cases.json').read_text())
names=['finite-opposite-corner-positive','finite-opposite-corner-tangent-negative','minA-qnan-opposite-corner','centerA-qnan','radius-qnan'];wants=[1,0,1,0,0];observations=[]
for c,name,want in zip(cases,names,wants):
 assert c['name']==name and c['failure'] is None and c['running_hex']==code.hex() and c['running_sha256']==sha(code) and c['mutated'] is False
 initial=c['initial'];assert initial['mxcsr']=='0x1f80' and initial['eflags']=='0x2' and (initial['rcx'],initial['rdx'],initial['rsp'],initial['sentinel'])==('0x40000100','0x40000200','0x60001808','0x60000200')
 rect=bytes.fromhex(initial['rectangle']);circle=bytes.fromhex(initial['circle']);stack=bytes.fromhex(initial['stack']);assert len(rect)==32 and len(circle)==24 and len(stack)==80 and struct.unpack_from('<Q',stack)[0]==0x60000200
 assert [f'{struct.unpack_from("<I",rect,o)[0]:08x}' for o in [0,8,16,24]]==c['rectangle_bits']
 assert all(rect[o:o+4]==b'\xa5'*4 for o in [4,12,20,28]) and all(circle[o:o+4]==b'\xa5'*4 for o in [4,12,20])
 assert [struct.unpack_from('<I',circle,o)[0] for o in [0,8,16]]==[int(c[k],16) for k in ['x_bits','z_bits','radius_bits']]
 regs={f'xmm{i}':0xA5A5A5A5 for i in range(6)};eax=0xA5A5A5A5;cf,zf,pf=0,0,0;pc=0x4690B0;visits=[];reads=[];comparisons=[];branches=[]
 def value(i,o):
  if o.type==capstone.CS_OP_REG:return regs[i.reg_name(o.reg)]
  assert o.type==capstone.CS_OP_MEM
  base=i.reg_name(o.mem.base);buf,a=(rect,0x40000100) if base=='rcx' else (circle,0x40000200);data=buf[o.mem.disp:o.mem.disp+4];reads.append(dict(pc=hex(i.address),address=hex(a+o.mem.disp),size=4,bytes=data.hex()));return struct.unpack('<I',data)[0]
 for step in range(128):
  i=si[pc];visits.append(hex(pc));op=i.mnemonic;os=i.operands;next_pc=pc+i.size
  if op in ['movss','movaps']:regs[i.reg_name(os[0].reg)]=value(i,os[1])
  elif op in ['addss','subss','mulss']:
   dst=i.reg_name(os[0].reg);x,y=f(regs[dst]),f(value(i,os[1]));regs[dst]=bits(x+y if op=='addss' else x-y if op=='subss' else x*y)
  elif op=='comiss':
   vals=[value(i,o) for o in os];comparisons.append(dict(pc=hex(pc),args=i.op_str,operands=[f'{v:08x}' if o.type==capstone.CS_OP_REG else struct.pack('<I',v).hex() for v,o in zip(vals,os)]));x,y=map(f,vals)
   cf,zf,pf=(1,1,1) if math.isnan(x) or math.isnan(y) else (int(x<y),int(x==y),0)
  elif op in ['jb','ja','jae']:
   branches.append(dict(pc=hex(pc),flag_mask=cf|(pf<<2)|(zf<<6)))
   if (cf if op=='jb' else not cf and not zf if op=='ja' else not cf):next_pc=os[0].imm
  elif op=='mov':assert i.op_str=='eax, 1';eax=1
  elif op=='xor':assert i.op_str=='eax, eax';eax=0;cf,zf,pf=0,1,1
  elif op=='seta':
   branches.append(dict(pc=hex(pc),flag_mask=cf|(pf<<2)|(zf<<6)));eax=(eax&~255)|int(not cf and not zf)
  elif op=='ret':reads.append(dict(pc=hex(pc),address='0x60001808',size=8,bytes=stack[:8].hex()));break
  else:raise AssertionError(op)
  pc=next_pc
 else:raise AssertionError('Incomplete replay cannot pass')
 if '--fault-universal-nan-reject' in sys.argv and any(math.isnan(f(struct.unpack_from('<I',b,o)[0])) for b,offs in [(rect,[0,8,16,24]),(circle,[0,8,16])] for o in offs):eax=0
 assert eax==c['after']['eax']==want, 'Universal NaN rejection contradicts original operand-specific path'
 assert visits==c['visits'] and reads==c['reads'] and comparisons==[{k:x[k] for k in ['pc','args','operands']} for x in c['comparisons']]
 assert branches==[dict(pc=x['pc'],flag_mask=int(x['eflags'],16)&0x45) for x in c['branch_flags']]
 assert not c['writes'] and all(c['after'][k]==initial[k] for k in ['rectangle','circle','stack']) and c['after']['stop_pc']=='0x60000200' and c['after']['rsp']=='0x60001810' and int(c['after']['mxcsr'],16)&~0x3F==0x1F80
 observations.append(dict(name=name,result=eax,path=visits,branch_flags=branches,comparisons=comparisons,limits='Guest comparison completion/results and matching source-path replay, not native status/exception proof'))
assert cases[2]['rectangle_bits']==['7fc00000','00000000','41200000','41200000'] and cases[2]['radius_bits']=='40c00000'
assert cases[3]['x_bits']=='7fc00000' and cases[4]['radius_bits']=='7fc00000'
bad=observations[2];assert bad['comparisons'][-1]['pc']=='0x469196' and bad['comparisons'][-1]['operands']==['42100000','41c80000'] and bad['branch_flags'][-1]==dict(pc='0x469199',flag_mask=0)
assert {x['pc']:x['flag_mask'] for x in bad['branch_flags']}['0x4690c7']==0x45 and {x['pc']:x['flag_mask'] for x in bad['branch_flags']}['0x4690f4']==0x45
for p in raw['tools']['providers']:assert sha(Path(p['path']).read_bytes())==p['sha256']
result=dict(method=raw['method'],reference=ref,raw_sha256=sha((W/'raw.json').read_bytes()),observations=observations,interpretation='A quiet NaN in rectangle minA rejects both bands and minA-based corners, but finite maxA/maxB corner remains: original final comparison36>25 and SETA return1 for center13,14/r6. Same finite r6 control1/r5tangent0; NaNcenterA and NaNradius controls0. Thus blanket any-NaN rejection is false for this operand domain; completed unordered comparison failure applies only tests involving the NaN, not every alternative.',required_change='OPUS actual model/coverage and field consumer distinguish NaNcenter/radius from malformed individual rectangle bound; add this specific control and completed/masked compare qualifier. FABLE inspect only own actual affected scope; preserve valid finite/corner/contact source findings. No countlabel-only fix or broad retraction.',limits=raw['limits'],cleanup=raw['cleanup'])
out=W/'result.json'
if out.exists():assert json.loads(out.read_text())==result
else:out.write_text(json.dumps(result,indent=2)+'\n')
if (W/'manifest.json').exists():
 for m in json.loads((W/'manifest.json').read_text())['members']:
  data=(W/m['path']).read_bytes();assert len(data)==m['bytes'] and sha(data)==m['sha256']
print('PASS59 source/full5paths/RET/argument immutability/ordered and unordered branch flags; minA-NaN counterexample1, center/radius0; no native status claim',flush=True)
