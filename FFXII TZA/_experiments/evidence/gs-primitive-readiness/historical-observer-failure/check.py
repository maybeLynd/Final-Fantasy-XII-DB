import hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s,groups):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;x={}
 for b in s['bodies']:
  raw=bytes.fromhex(b['raw_hex']);assert len(raw)==b['size'] and sha(raw)==b['sha256']
  ii=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in cs.disasm(raw,int(b['entry'],16))]
  assert ii==b['instructions'];x.update({i['pc']:i for i in ii})
 def ins(pc,op,args):assert (x[pc]['op'],x[pc]['args'])==(op,args),(pc,x[pc])
 def target(pc,index=0):
  i=next(cs.disasm(bytes.fromhex(x[pc]['bytes']),int(pc,16)))
  operands=[o for o in i.operands if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RIP]
  return i.address+i.size+operands[index].mem.disp
 ins('0x20feee','call','0x20fba0');ins('0x20fef3','xor','eax, eax')
 ins('0x20fef5','mov','dword ptr [rip + 0x1d73679], eax');assert target('0x20fef5')==0x1F83574
 ins('0x20fefb','mov','dword ptr [rip + 0x1d73667], eax');assert target('0x20fefb')==0x1F83568
 ins('0x20f6b5','mov','ecx, dword ptr [rip + 0x1d73eb9]');assert target('0x20f6b5')==0x1F83574
 ins('0x20f6c1','inc','ecx');ins('0x20f6c3','cmp','ecx, dword ptr [rip + 0x1d73ea7]');assert target('0x20f6c3')==0x1F83570
 ins('0x20f6c9','cmovg','ecx, dword ptr [rip + 0x1d73ea0]');assert target('0x20f6c9')==0x1F83570
 ins('0x20f6d0','mov','dword ptr [rip + 0x1d73e9e], ecx');assert target('0x20f6d0')==0x1F83574
 ins('0x2102e8','mov','rax, qword ptr [rbx + 8]');ins('0x2102ec','shr','rax, 0x2f');ins('0x2102f0','and','eax, 1')
 ins('0x2102f3','jne','0x21030b');ins('0x2102f5','mov','eax, dword ptr [rip + 0x1d73275]');assert target('0x2102f5')==0x1F83570
 ins('0x2102fb','cmp','dword ptr [rip + 0x1d73273], eax');assert target('0x2102fb')==0x1F83574
 ins('0x210301','jne','0x21030b');ins('0x210303','mov','al, 1');ins('0x21030b','xor','al, al')
 ins('0x20f70d','test','al, al');ins('0x20f70f','je','0x20fa6f')
 ins('0x20f715','mov','eax, dword ptr [rip + 0x1d73e51]');assert target('0x20f715')==0x1F8356C
 ins('0x20f71b','mov','dword ptr [rip + 0x1d73e53], eax');assert target('0x20f71b')==0x1F83574
 p=s['consumer'];raw=(HERE/p['retained']).read_bytes();assert len(raw)==p['bytes'] and sha(raw)==p['sha256']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256'] and s['stubs']==[]
 assert s['fields']=={'primitive':'0x1f83560','fan':'0x1f83561','vertex_count':'0x1f83568','carry':'0x1f8356c','required':'0x1f83570','phase':'0x1f83574','aux78':'0x1f83578'}
 expected=[('triangle-list-control',3,3,0,[0,0,1,0,0,1]),('line-list',1,2,0,[0,1,0,1,0,1]),
  ('line-strip',2,2,1,[0,1,1,1,1,1]),('triangle-strip',4,3,2,[0,0,1,1,1,1]),
  ('point',0,1,0,[1]*6),('triangle-fan',5,3,2,[0,0,1,1,1,1]),('sprite',6,2,0,[0,1,0,1,0,1]),
  ('triangle-list-ADC-control',3,3,0,[0,0,0,1,0,0])]
 assert len(groups)==len(expected)>0;rows=[]
 def validate(r):
  assert r['accepted_boundary'] and not r['failure'] and not r['faults'] and 0<r['instruction_count']<2000
  assert len(r['steps'])==r['instruction_count']
  for step in r['steps']:assert step['op']==x[step['pc']]
 for g,(name,mode,required,carry,als) in zip(groups,expected,strict=True):
  assert (g['name'],g['mode'])==(name,mode) and g['original_code_unchanged']
  validate(g['init']);initial=g['init']['after']
  assert initial['primitive']==mode and initial['required']==required and initial['carry']==carry
  assert initial['phase']==initial['vertex_count']==0 and initial['fan']==(mode==5)
  assert any(step['pc']=='0x20fef5' for step in g['init']['steps'])
  assert any(step['pc']=='0x20fefb' for step in g['init']['steps'])
  assert g['starting_fields']['phase']!=0 and initial['phase']==0
  assert len(g['vertices'])==6 and [v['gate']['al'] for v in g['vertices']]==als
  phase=0;transitions=[]
  for i,v in enumerate(g['vertices']):
   p,r,c=v['phase'],v['gate'],v['consumer']
   for stage in [p,r,c]:validate(stage)
   assert v['candidate']==i+1 and v['adc']==g['adcs'][i]
   assert p['entry']=='0x20f6b5' and p['final_pc']=='0x20f6d6' and p['before']['phase']==phase
   grown=min(phase+1,required);assert p['after']['phase']==grown
   assert r['entry']=='0x2102e8' and r['final_pc']=='0x62000000'
   assert all(0x2102E8<=int(st['pc'],16)<0x210313 for st in r['steps'])
   assert r['final_rsp']==hex(int(s['fixture']['stack'],16)+8) and r['final_rbx']==s['fixture']['saved_rbx']
   assert r['before']==r['after']==p['after'] and r['al']==int(not v['adc'] and grown==required)
   assert any(e['pc']=='0x2102e8' and e['kind']=='read' and e['size']==8 and e['value_hex']==(v['adc']<<47).to_bytes(8,'little').hex() for e in r['events'])
   phase=carry if r['al'] else grown
   assert c['entry']=='0x20f70d' and c['final_pc']==('0x20f721' if r['al'] else '0x20fa6f')
   assert c['after']['phase']==phase and c['before']==r['after']
   assert c['after']['vertex_count']==0 # Omitted real vertex increment/conversion is explicit.
   transitions.append({'candidate':i+1,'adc':v['adc'],'phase_before':p['before']['phase'],'phase_after_increment':grown,'al':r['al'],'phase_after_consumer':phase})
  rows.append({'case':name,'primitive_mode':mode,'required':required,'carry':carry,'fan':initial['fan'],'AL_pattern':als,'transitions':transitions})
 return {'method':'B isolated shipping integer controller with explicit interior boundary/omitted effects',
  'observations':rows,'established':['Actual PRIM setter calls20FBA0 but then zeroesphase andvertexcount; helper-only initialization would omit this reset.',
   'XYZ2 prefix incrementsphase and signed-CMOVG saturates it at required (valid tested small values).',
   'Postwriter suffix returns AL true only for clear inputqword+8 bit47 and phase==required. Consumer tests AL, resettingphase tocarry only on true.',
   'List/strip patterns differ throughcarry0 versus1/2; fan sharestriangle-strip readiness but hasfanflag1. Sprite sharesline-list readiness but laterindexeffects differ.',
   'ADC suppression leavesphase atrequired; a subsequent clear-bit candidate can pass and reset. No coordinate-dependent test appears in the executed suffix.'],
  'semantic_implication':'Qualify current list/strip return hypothesis with original initialization, saturatedphase/equality, ADC and carry-reset mechanics. Preserve byte-return consumption, signed comparison, and full setter boundary.',
  'limits':s['entry_limits']+' Supplied integer state/source bits. Actual geometry write/exceptions/counteraliasing, full packet/index/GPU effects, normal callers and frequency remain untested. Fan/sprite topology names inherited from existing page, no new visual proof.',
  'cleanup':'Fresh disposable guests; original code unchanged; no FF12/native attach/input/instrument/save/config/reference writes or new live cleanup receipt.',
  'affected_consumers':['FABLE legacyGS2.1b list/strip return gate','OPUS original counter/ADC/AL widths and initializer ordering'],
  'propagation':'PENDING independent review and owner incorporation'}
def main():
 s=json.loads((HERE/'source.json').read_text());g=json.loads((HERE/'raw-results.json').read_text());out=derive(s,g)
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_ISOLATED_COMPONENTS','groups':len(g),
  'native_or_live_cases':0,'no_effect_stubs':True,'controlled_interior_entries':True,
  'limits':'Original integer components/omitted geometry boundary only. No complete renderer parity, independent review or full mutation campaign acceptance.'},indent=2)+'\n')
 print('PASS original initializer/phase/ADC/AL/carry transitions; explicit omitted geometry boundary preserved.')
if __name__=='__main__':main()
