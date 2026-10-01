"""Bounded shipping-resource/native registration sentinel and regression controls."""
import ast,copy,hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
NAME='PMeshInstanceSegmentContext'
def need(c,m):
 if not c:raise ValueError(m)
def parse(header,ns,lists):
 need(len(header)==84 and header[:4]==b'RYHP','original cluster header')
 hs,nssz,platform,nlists=struct.unpack_from('<4I',header,4)
 need(hs==84 and nssz==len(ns) and 0<nlists<128 and len(lists)==nlists*36,'complete header/namespace/lists')
 bom,size,nt,nc,nm,poolsize,u6,u7=struct.unpack_from('<8I',ns)
 need(bom==0x01020304 and size==nssz and nc>0 and u6==u7==0,'namespace identity')
 co=32+4*nt;mo=co+36*nc;po=mo+24*nm;need(po+poolsize==len(ns),'namespace exact extent')
 def string(off):
  need(0<=off<poolsize and (off==0 or ns[po+off-1]==0),'name start identity')
  end=ns.find(b'\0',po+off);need(end>=po+off and end<len(ns),'name terminator')
  b=ns[po+off:end];need(b and all(32<=c<127 for c in b),'ASCII name');return b.decode()
 classes=[];member_start=0
 for i in range(nc):
  words=struct.unpack_from('<9I',ns,co+i*36);need(0<=words[0]<=nc and words[0]!=i+1,'parent id')
  need(member_start+words[3]<=nm,'member extent')
  mem=[]
  for j in range(words[3]):
   a=mo+(member_start+j)*24;v=struct.unpack_from('<6I',ns,a)
   need(v[1]!=nt and (v[1]<nt or nt<v[1]<=nt+nc),'member reference')
   mem.append({'name':string(v[0]),'words':list(v),'namespace_offset':a})
  classes.append({'id':i+1,'name':string(words[2]),'words':list(words),'members':mem,'namespace_offset':co+i*36});member_start+=words[3]
 need(member_start==nm,'all members consumed')
 for c in classes:
  visited=set();cid=c['id']
  while cid:
   need(cid not in visited,'parent cycle');visited.add(cid);cid=classes[cid-1]['words'][0]
  c['parent']=classes[c['words'][0]-1]['name'] if c['words'][0] else None
 for c in classes:
  for m in c['members']:
   ref=m['words'][1]
   m['type_name']=string(struct.unpack_from('<I',ns,32+ref*4)[0]) if ref<nt else classes[ref-nt-1]['name']
 rows=[]
 for i in range(nlists):
  w=struct.unpack_from('<9I',lists,i*36);need(1<=w[0]<=nc and w[1]>0,'valid nonempty list')
  rows.append({'index':i,'class_id':w[0],'class':classes[w[0]-1]['name'],'count':w[1],'objects_size':w[2],'words':list(w),'entry_offset':hs+nssz+i*36})
 return {'classes':classes,'lists':rows,'n_types':nt,'n_classes':nc,'n_members':nm}
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
def native(ref):
 bodies={int(b['address'],16):b for b in ref['bodies']};ins={}
 for a,b in bodies.items():
  raw=bytes.fromhex(b['hex']);need(len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'],'native raw identity')
  rows=list(md.disasm(raw,a));need(rows and rows[-1].address+rows[-1].size==a+len(raw),'complete native decode')
  ins.update({x.address:x for x in rows})
 def at(a,m):need(ins[a].mnemonic==m,'native instruction '+hex(a));return ins[a]
 def direct(a,target):i=at(a,'call');need(i.operands[0].type==capstone.x86.X86_OP_IMM and i.operands[0].imm==target,'native direct target')
 def rip(a):i=at(a,'lea');o=i.operands[1];need(o.type==capstone.x86.X86_OP_MEM and o.mem.base==capstone.x86.X86_REG_RIP,'native RIP target');return i.address+i.size+o.mem.disp
 def stack_imm(a,offset,value):i=at(a,'mov');o,v=i.operands;need(o.type==capstone.x86.X86_OP_MEM and o.mem.base==capstone.x86.X86_REG_RSP and o.mem.disp==offset and v.imm==value,'native argument')
 need(rip(0x1614c4)==rip(0x5e6852)==0x2cb6d80,'same descriptor')
 direct(0x1614cb,0x5d9890);need(rip(0x1614d7)==0xd38540,'final descriptor table')
 slot=ref['final_descriptor_vtable'];need(slot['slot60_hex']==struct.pack('<Q',0x5cf0f0).hex(),'final descriptor slot60')
 need(ins[0x5cf0f0].mnemonic=='jmp' and ins[0x5cf0f0].operands[0].imm==0x5e67c0,'same final registration entry')
 need(at(0x5d98ca,'mov').operands[1].imm==0x48 and rip(0x5d98b6)==0x2e522f0,'instance extent/base descriptor')
 direct(0x5d98da,0x632d80)
 name=ref['strings'][NAME];need(rip(0x5d98d0)==int(name['address'],16) and bytes.fromhex(name['bytes_hex'])==(NAME+'\0').encode(),'native class name')
 member=ref['strings']['m_streamBindings'];need(rip(0x5e6848)==int(member['address'],16) and bytes.fromhex(member['bytes_hex'])==b'm_streamBindings\0','native field name')
 stack_imm(0x5e6840,0x20,0x38);direct(0x5e6860,0x632a10)
 need(rip(0x5e6859)==0x2ce3680,'member metadata record')
 # Wrapper push8+sub40 =48; [rsp+70] reads entry_rsp+28,
 # the fifth argument. It re-emits that at call_rsp+20 unchanged.
 need(at(0x632a15,'push').op_str=='rdi' and at(0x632a16,'sub').operands[1].imm==0x40,'wrapper stack delta')
 need(at(0x632a39,'mov').op_str=='eax, dword ptr [rsp + 0x70]' and at(0x632a3d,'mov').op_str=='dword ptr [rsp + 0x20], eax','fifth argument forwarding')
 direct(0x632a41,0x632960)
 # Base push3*8+sub30 =48; same fifth arg becomes member+48.
 need([at(a,'push').op_str for a in [0x632965,0x632966,0x632967]]==['rsi','rdi','r14'] and at(0x632969,'sub').operands[1].imm==0x30,'base stack delta')
 need(at(0x6329b9,'mov').op_str=='eax, dword ptr [rsp + 0x70]' and at(0x6329bd,'mov').op_str=='dword ptr [rsi + 0x48], eax','stored member offset')
 need(at(0x6329ee,'call').op_str=='qword ptr [rax + 0x40]','member attach path')
 need(ref['own_class_rtti_v_hits']==ref['own_class_rtti_u_hits']==0 and ref['positive_own_class_rtti_hits']>0,'own RTTI controlled absence')
 return {'name':NAME,'descriptor':'02CB6D80','instance_size':72,'base':'PMeshSegmentContext','base_size':40,'native_member':'m_streamBindings','native_offset':56,'native_offset_hex':'0x38','node':'02CE3680','guarded_callsite':'005E6860','wrapper':'00632A10','base_registration_callsite':'00632A41','claim':'A guarded original native member-registration path exists; direct-only counter zero does not mean no reflected member.'},ins
def main():
 source=json.loads((HERE/'source.json').read_text());meta=json.loads((HERE/'metadata.json').read_text());ref=json.loads((HERE/'reference.json').read_text())
 slices={n:(HERE/n).read_bytes() for n in ['header.bin','namespace.bin','listheaders.bin']}
 for n,b in slices.items():need(len(b)==source['slices'][n]['bytes'] and hashlib.sha256(b).hexdigest()==source['slices'][n]['sha256'],'source slice '+n)
 parsed=parse(slices['header.bin'],slices['namespace.bin'],slices['listheaders.bin']);result,ins=native(ref)
 cls=next(c for c in parsed['classes'] if c['name']==NAME);witness=[r for r in parsed['lists'] if r['class']==NAME]
 need(len(witness)==1 and witness[0]['count']==25 and cls['parent']=='PMeshSegmentContext','named authored list witness')
 file_member=next(m for m in cls['members'] if m['name']=='m_streamBindings')
 need(file_member['words'][2]==0,'file offset preserved separately from native38')
 need(any(r['class']=='PMesh' and r['count']==1 for r in parsed['lists']) and any(r['class']=='PAssetReference' and r['count']==83 for r in parsed['lists']),'parser positive original controls')
 selected=meta['selected_current_rows'];schema=[v for k,v in selected.items() if k.endswith('/phyre-field-schema.tsv')][0];need(schema==[],'snapshot schema lacks member')
 descriptor=[v for k,v in selected.items() if k.endswith('/phyre-class-descriptor-vtable.tsv')][0][0];need(descriptor['regcalls']=='0' and descriptor['in_schema']=='no','snapshot counter zero')
 # Execute the actual producer's frozen regcalls function, not its summary.
 generator=ROOT/'Database/Tools/analysis-kit/gfz-scripts/gen_phyre_descriptor_vtables.py'
 # Freeze this exact original function so later owner fixes do not erase the
 # historical counterexample. Source file SHA and definition lines are pinned.
 tree=ast.parse(meta['original_regcalls_source']);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='regcalls')
 env={'X86_OP_IMM':capstone.x86.X86_OP_IMM};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(generator),'exec'),env)
 class Image:
  def body(self,a):return [i for i in ins.values() if a<=i.address<a+next(x['bytes'] for x in ref['bodies'] if int(x['address'],16)==a)]
 old=env['regcalls'](Image(),0x5e67c0);positive=env['regcalls'](Image(),0x632a10)
 need(old==0 and positive==1,'actual instrument counterexample with scalar positive')
 qualified=sum(i.mnemonic=='call' and i.operands[0].type==capstone.x86.X86_OP_IMM and i.operands[0].imm in [0x632960,0x632a70,0x632a10] for i in Image().body(0x5e67c0))
 need(qualified==1,'smallest array-wrapper detector control')
 mutations=[]
 for label in ['bad-list-id','short-namespace','name-middle','wrong-native-offset','wrong-native-descriptor','wrong-final-slot']:
  h,n,l=slices['header.bin'],bytearray(slices['namespace.bin']),bytearray(slices['listheaders.bin']);r=copy.deepcopy(ref)
  if label=='bad-list-id':struct.pack_into('<I',l,witness[0]['index']*36,0)
  elif label=='short-namespace':n=n[:-1]
  elif label=='name-middle':struct.pack_into('<I',n,cls['namespace_offset']+8,cls['words'][2]+1)
  elif label=='wrong-final-slot':r['final_descriptor_vtable']['slot60_hex']='00'*8
  else:
   body=next(x for x in r['bodies'] if x['address']=='0x5e67c0');b=bytearray.fromhex(body['hex'])
   if label=='wrong-native-offset':b[0x5e6840-0x5e67c0+4]=0x28
   else:b[0x5e6852-0x5e67c0+3]^=1
   body.update(hex=b.hex(),sha256=hashlib.sha256(b).hexdigest())
  try:parse(h,n,l);native(r)
  except (ValueError,KeyError):mutations.append(label)
  else:raise ValueError('mutation survived '+label)
 output={'method':'A original shipping instructions and selected authored resource; no live or isolated execution',
 'native':result,'authored':{'source':source['entry'],'list':witness[0],'class':cls},
 'instrument':{'old_direct_counter':old,'old_scalar_positive':positive,'candidate_wrapper_aware_counter':qualified,'production_generator_changed':False,'definition':meta['generator_target_condition']},
 'controls':{'original_resource_positives':['PMesh count1','PAssetReference count83'],'corruptions_rejected':mutations},
 'limits':['One named sentinel; historical137 cohort/count not reclassified.','Native type/field width unproved here; file member offset0 is not native+38.','Guarded registration path is static, not proof it executed in the title/scene.','Authored25 objects do not establish normal scene reachability, initialized runtime pointers or lifetime.','EXP124173 default capture does not contain this class; no recapture or default-byte value inferred.']}
 (HERE/'observation.json').write_text(json.dumps(output,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_BOUNDED_STATIC_AND_AUTHORED','controls':output['controls'],'semantic_limits':output['limits']},indent=2)+'\n')
 print('PASS original member m_streamBindings+38;25 authored instances; actual old counter0 / scalar positive1 / qualified sentinel1;',len(mutations),'rejected controls')
if __name__=='__main__':main()
