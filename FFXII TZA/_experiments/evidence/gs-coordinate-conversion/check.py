import hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()

def derive(s,rows):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 assert s['stubs']==[] and s['shipping_scale_hex']==struct.pack('<f',0.0625).hex()
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;im={}
 expected_extents={0x210230:227,0x20EA50:266,0x202B70:31,0x217060:235}
 assert {int(b['entry'],16):b['size'] for b in s['bodies']}==expected_extents
 for b in s['bodies']:
  raw=bytes.fromhex(b['raw_hex']);assert len(raw)==b['size'] and sha(raw)==b['sha256']
  a=int(b['entry'],16);ii=list(cs.disasm(raw,a));assert sum(i.size for i in ii)==len(raw)
  assert b['pe_function'][:2]==[hex(a),hex(a+len(raw))]
  assert [{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]==b['instructions']
  im.update({hex(i.address):i for i in ii})
 def ins(pc,op,args):
  i=im[pc];assert (i.mnemonic,i.op_str)==(op,args),(pc,i.mnemonic,i.op_str)
 def target(pc):
  i=im[pc];ops=[o for o in i.operands if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RIP]
  assert len(ops)==1;return i.address+i.size+ops[0].mem.disp
 for name,b in s['bindings'].items():assert target(b['site'])==int(b['address'],16),(name,b)
 assert target('0x210285')==target('0x2102a7')==0x8F30EC
 ins('0x210236','cmp','byte ptr [rip + 0x1dc33d4], 0');ins('0x21024b','je','0x210269')
 ins('0x210267','jmp','0x2102d5');ins('0x2102bd','comiss','xmm1, xmm0');ins('0x2102c0','ja','0x2102c5')
 ins('0x2102c2','movaps','xmm0, xmm1');ins('0x2102cd','comiss','xmm0, xmm1');ins('0x2102d0','ja','0x2102d5')
 ins('0x2102d2','movaps','xmm0, xmm1');ins('0x2102e3','call','0x20ea50')
 ins('0x20ead3','call','0x202b70');ins('0x202b7e','call','0x217060')
 ins('0x2170a6','addss','xmm2, xmm0');ins('0x2170b2','addss','xmm2, xmm1');ins('0x2170be','addss','xmm2, xmm0')
 ins('0x20ea80','mov','dword ptr [rcx + 0xc], 0x3f800000')
 ins('0x20eadc','divss','xmm0, dword ptr [rbx + 0xc]');ins('0x20eaea','divss','xmm1, dword ptr [rbx + 0xc]')
 ins('0x20eaf9','divss','xmm0, dword ptr [rbx + 0xc]');ins('0x20eb08','divss','xmm1, xmm1')
 for k in ['consumer']:
  b=s[k];raw=(HERE/b['retained']).read_bytes();assert len(raw)==b['bytes'] and sha(raw)==b['sha256']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 expected=[('packed-identity-control',[1.,2.,64.,1.]),('same-float-bytes-as-packed',[0.,0.,1000.,1.]),
  ('same-float-bytes-direct',[1.,2.,3.,1.]),('packed-upper-bound',[1.,2.,1000.,1.]),
  ('packed-lower-bound',[1.,2.,10.,1.]),('direct-outside-packed-bound',[1.,2.,2000.,1.]),
  ('matrix-and-homogeneous-divide',[6.,13.,21.,1.]),('single-precision-order',[1.5,1.,1.,1.])]
 assert len(rows)==len(expected)>0
 assert rows[1]['input_hex']==rows[2]['input_hex'] and rows[1]['coordinate_flag']==0 and rows[2]['coordinate_flag']==1
 normal=[];dst=int(s['fixture']['destination'],16)
 for r,(name,xyz) in zip(rows,expected,strict=True):
  assert r['name']==name and r['final_pc']==s['fixture']['return'] and r['final_rsp']==hex(int(s['fixture']['stack'],16)+8)
  assert not r['faults'] and not r['failure'] and 0<r['instruction_count']<5000 and len(r['steps'])==r['instruction_count']
  assert r['input_unchanged'] and r['bindings_unchanged'] and r['code_unchanged']
  assert r['final_nonvolatile']==s['fixture']['nonvolatile_seeds']
  assert int(r['final_mxcsr'],16)&~63==int(s['fixture']['mxcsr'],16) # status flags alone may change.
  assert r['return_al']==1 # AL only; upper return bits have another history.
  for t in r['steps']:
   i=im[t['pc']];assert (t['bytes'],t['op'],t['args'])==(i.bytes.hex(),i.mnemonic,i.op_str)
  calls=[t for t in r['steps'] if t['op']=='call']
  assert [t['pc'] for t in calls]==['0x2102e3','0x20ead3','0x202b7e']
  assert all(int(t['rsp'],16)%16==0 for t in calls)
  assert [b['pc'] for b in r['boundaries']]==['0x20ea50','0x202b70','0x217060','0x20ead8']
  uv=[0.75,1.] if r['uv_select'] else [0.25,0.5]
  expected40=struct.pack('<10f',*xyz,8.,64.,128.,255.,*uv)
  assert r['output_hex']==expected40.hex()+'a5'*8
  assert r['output_first_ten_floats']==list(struct.unpack('<10f',expected40))
  entered={t['pc'] for t in r['steps']}
  if r['coordinate_flag']==0:
   assert {'0x210269','0x2102bd','0x2102cd'}<=entered
   assert {'0x21024d','0x210251','0x21025c'}.isdisjoint(entered)
   z=max(r['lower'],min(r['upper'],(int.from_bytes(bytes.fromhex(r['input_hex'])[8:16],'little')>>4)&0xFFFFFF))
   q=int.from_bytes(bytes.fromhex(r['input_hex'])[:8],'little');pre=[(q&0xFFFF)/16.,((q>>32)&0xFFFF)/16.,z,1.]
  else:
   assert {'0x21024d','0x210251','0x21025c','0x210267'}<=entered
   assert {'0x210269','0x2102bd','0x2102cd'}.isdisjoint(entered)
   pre=list(struct.unpack('<3f',bytes.fromhex(r['input_hex'])[:12]))+[1.]
  temp=struct.pack('<4f',0.,pre[2],pre[1],pre[0]).hex()
  assert r['boundaries'][0]['temporary_coordinate_hex']==temp
  assert r['boundaries'][1]['destination_hex'][:32]==struct.pack('<4f',*pre).hex()
  assert r['boundaries'][2]['destination_hex'][:32]==struct.pack('<4f',*pre).hex()
  transformed=[12.,26.,42.,2.] if name=='matrix-and-homogeneous-divide' else xyz
  assert r['boundaries'][3]['destination_hex'][:32]==struct.pack('<4f',*transformed).hex()
  output_writes=[e for e in r['events'] if e['kind']=='write' and dst<=int(e['address'],16)<dst+48]
  covered={a for e in output_writes for a in range(int(e['address'],16),int(e['address'],16)+e['size'])}
  assert covered==set(range(dst,dst+40))
  for k,b in r['starting_bindings'].items():
   if k=='matrix':assert b==struct.pack('<16f',*r['matrix']).hex()
   if k in ['required','phase']:assert b==struct.pack('<I',3).hex()
  normal.append({'case':name,'format':r['coordinate_flag'],'input_hex':r['input_hex'],
   'vector_before_matrix':pre,'vector_before_division':transformed,'output_xyzw':xyz,
   'colour_components':[8.,64.,128.,255.],'uv':uv,'unwritten_tail_hex':'a5'*8,
   'AL':r['return_al'],'instruction_count':r['instruction_count']})
 # Distinguishing finite rounding control: original Y+X, then Z, then W.
 f=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
 assert f(f(f(-16777216.+16777216.)+1.)+0.5)==1.5
 assert f(f(f(16777216.+1.)-16777216.)+0.5)==0.5
 return {'method':s['method'],'observations':normal,
  'established':['Packed X/Y u16 scale by shipping 1/16; packed Z bits4..27 are upper-then-lower bounded before the matrix. Nonzero format byte instead reads three floats and bypasses both depth comparisons.',
   'Writer supplies W=1, then actual matrix leaf and wrapper transform four components. Writer divides transformed XYZ by transformed W and writes W/W. Tested finite nonzero-W cases produce W=1; exceptional/zero W is untested.',
   'Matrix leaf performs separate SSE f32 multiplies and adds: Y contribution plus X, then Z, then W. Finite cancellation control yields1.5; an X+Z-first algebraic rearrangement yields0.5.',
   'Four source bytes become unnormalised float components at+10/+14/+18/+1C; UV byte selects two distinct float pairs at+20/+24. Output+28..+2F stays A5 under all eight nonalias fixtures.',
   'Full four-function chain executed at normal entries without stubs, preserving Windows nonvolatile registers; supplied equal counters remain unchanged and AL=1.'],
  'semantic_implication':'Extend GS vertex representation with format-dependent depth path, pre-transform bounds, ordered f32 matrix/division, exact component/UV writes. Do not treat a48-byte stride as proof that these functions initialise every byte.',
  'limits':s['limits']+' Tail sample is not padding, lifetime or full vertex ABI proof. Floating-point MXCSR fixed1F80; exceptional numbers, reversed bounds and aliasing untested. Colour semantic channel names not inferred from byte order alone.',
  'cleanup':'Disposable guest objects only; hooks removed after each run, code/input/globals unchanged. No FF12/native attachment/input/PC control/save/config/reference writes or new live-restoration receipt.',
  'affected_consumers':['FABLE GS vertex-kick2.1b','OPUS coordinate/layout/ABI/float-order qualifications'],
  'propagation':'PENDING independent review and owner incorporation'}

if __name__=='__main__':
 s=json.loads((HERE/'source.json').read_text());r=json.loads((HERE/'raw-results.json').read_text());o=derive(s,r)
 (HERE/'observation.json').write_text(json.dumps(o,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_ISOLATED_ORIGINAL_CODE','cases':len(r),
  'complete_shipping_functions':4,'native_or_live_cases':0,'stubs':0,'interior_entries':0,
  'limits':'Bounded finite controlled composition; not native rendering, original initialization, exhaustive FP domain, independent acceptance or full mutation campaign.'},indent=2)+'\n')
 print('PASS original full coordinate/transform/division chain; finite controls and limits retained.')
