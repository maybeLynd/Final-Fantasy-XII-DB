"""Bounded original bytes and source qualification, not native/live execution."""
import ast,copy,hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def row_keys(raw):
 assert len(raw)==1312 and raw[:4]==b'st2e'
 assert struct.unpack_from('<I',raw,4)[0]==32 and struct.unpack_from('<H',raw,8)[0]==40
 assert struct.unpack_from('<I',raw,12)[0]==32
 rows=[raw[32+40*i:32+40*(i+1)] for i in range(32)]
 assert all(struct.unpack_from('<H',r)[0]==0x2800+i for i,r in enumerate(rows))
 return rows
def old_byte_only(raw):
 return all(raw[32+40*i]==i for i in range(32))
def decode_bank(bank):
 count=struct.unpack_from('<I',bank)[0];assert count==32
 offsets=struct.unpack_from('<33I',bank,4)
 assert offsets[0]==136 and all(a<b for a,b in zip(offsets,offsets[1:])) and offsets[-1]<=len(bank)
 def char(b):
  if 0x20<=b<=0x39:return chr(b+0x21)
  if 0x3A<=b<=0x53:return chr(b+0x27)
  if b==4:return ' '
  if b in (0xA3,0xA5):return '-'
  raise AssertionError('unexpected code in selected names '+hex(b))
 records=[]
 for i,(a,b) in enumerate(zip(offsets,offsets[1:])):
  block=bank[a:b];assert block[:2]==b'\0\0'
  end=block.index(0,2);assert all(x==0 for x in block[end:])
  records.append({'entry':i,'bank_offset':a,'raw_hex':block.hex(),'name':''.join(char(x) for x in block[2:end])})
 assert [records[i]['name'] for i in (0,3,6,31)]==['KO','Stop','Doom','X-Zone']
 return records
def qualify_code(code,source):
 identity=source['function_boundary'];assert len(code)==identity['code_bytes'] and sha(code)==identity['code_sha256']
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
 full=list(md.disasm(code,0x31C5D0));assert sum(i.size for i in full)==len(code) and full[-1].address==0x31E597 and full[-1].mnemonic=='ret'
 by={i.address:i for i in full};boundaries=set(by)|{0x31E598}
 def expect(a,op,args):
  i=by[a];assert (i.mnemonic,i.op_str)==(op,args),(hex(a),i.mnemonic,i.op_str)
 for a,op,args in [(0x31E1D4,'movzx','ecx, word ptr [rax]'),(0x31E1DE,'shr','rcx, 0xb'),
 (0x31E20E,'movzx','edx, word ptr [rax]'),(0x31E211,'and','edx, 0x7ff'),
 (0x31E248,'movzx','eax, byte ptr [rbp + 2]'),(0x31E24C,'mov','byte ptr [rbx + 0x24], al'),
 (0x31E1CA,'movzx','edx, word ptr [rcx + 8]'),(0x31E1CE,'imul','edx, dword ptr [rbx + 4]'),(0x31E1D2,'add','eax, edx'),
 (0x31E17F,'movzx','ebp, word ptr [rdx + 8]'),(0x31E183,'imul','ebp, dword ptr [rbx + 4]'),(0x31E187,'add','ebp, eax')]:expect(a,op,args)
 def rip(a):
  i=by[a];m=next(o.mem for o in i.operands if o.type==capstone.x86.X86_OP_MEM and o.mem.base==capstone.x86.X86_REG_RIP)
  return i.address+i.size+m.disp
 for a in (0x31E169,0x31E178,0x31E1B4,0x31E1C3,0x31E1EB,0x31E1FD):assert rip(a)==0x2EBF118
 for a in (0x31E1AB,0x31E1D7):assert rip(a)==0x2EBF170
 for w in source['code_windows']:
  start,end=int(w['start'],16),int(w['end_exclusive'],16)
  assert start in boundaries and end in boundaries
  data=code[start-0x31C5D0:end-0x31C5D0]
  assert data.hex()==w['hex'] and sha(data)==w['sha256']
  actual=[{'address':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in full if start<=i.address<end]
  assert actual==w['instructions']
 return {'result':'STATIC_PHYSICAL_ACCESS_QUALIFIED','name_reads':['0x31e1d4','0x31e20e'],
 'name_width':2,'bank_shift':11,'entry_mask':'0x7ff','registry':'0x2ebf118','text_registry':'0x2ebf170',
 'separate_effect_byte_read':'0x31e248','separate_effect_byte_write':'0x31e24c','copied_to_query_offset':'0x24'},boundaries
def main():
 raw=(HERE/'status-table.bin').read_bytes();bank=(HERE/'bank5.bin').read_bytes();directory=(HERE/'directory.bin').read_bytes()
 source=json.loads((HERE/'source.json').read_text());code=(HERE/'query-function-code.bin').read_bytes()
 assert sha(raw)==source['prior_table_sha256'] and sha(bank)==source['bank5_sha256'] and sha(directory)==source['directory_sha256']
 assert struct.unpack_from('<I',directory,0xF8)[0]==source['text_section_offset']
 rows=row_keys(raw);names=decode_bank(bank);native,boundaries=qualify_code(code,source)
 records=[{'row':i,'name_key':hex(struct.unpack_from('<H',r)[0]),'bank':5,'bank_entry':i,
 'name':names[i]['name'],'separate_byte02':r[2],'first_dword':hex(struct.unpack_from('<I',r)[0])} for i,r in enumerate(rows)]
 assert len({r['separate_byte02'] for r in records})>1
 assert not all(struct.unpack_from('<I',r)[0]==0x001B2800+i for i,r in enumerate(rows))
 cases=[]
 def reject(name,f):
  try:f()
  except (AssertionError,struct.error,ValueError):cases.append({'name':name,'rejected':True})
  else:raise AssertionError('unrejected corruption '+name)
 bad=bytearray(raw);bad[32+3*40+1]=0x29
 assert old_byte_only(bad)
 before=(HERE/'preflight-check-before.py').read_text()
 history=json.loads((HERE/'preflight-before-provenance.json').read_text())
 for name,receipt in history['files'].items():
  data=(HERE/name).read_bytes();assert len(data)==receipt['bytes'] and sha(data)==receipt['sha256']
 tree=ast.parse(before);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='reduce')
 ns={'struct':struct,'SLOTS':[0x11,0x12,*range(0x14,0x20)]}
 exec(compile(ast.Module(body=[node],type_ignores=[]),'<retained-original-preflight-reducer>','exec'),ns)
 prior=json.loads((HERE/'preflight-source-before.json').read_text())
 original_directory=(HERE/'preflight-directory-before.bin').read_bytes()
 assert ns['reduce'](bytes(bad),original_directory,prior)['non_ff']==42
 reject('high byte changed; old first-byte predicate still accepts',lambda:row_keys(bytes(bad)))
 varied=bytearray(raw);varied[32+3*40+2]=0x55
 assert row_keys(bytes(varied))[3][:2]==rows[3][:2]
 # Counterfactual byte mutation is a separation control, not a valid shipping row.
 reject('four-byte fixed-prefix hypothesis',lambda:require(all(struct.unpack_from('<I',r)[0]==0x001B2800+i for i,r in enumerate(rows))))
 reject('cited start31E1C0 inside original instruction',lambda:require(0x31E1C0 in boundaries))
 reject('cited end31C7FE inside original instruction',lambda:require(0x31C7FE in boundaries))
 b=bytearray(bank);struct.pack_into('<I',b,4,135)
 reject('plausible shifted string table origin',lambda:decode_bank(bytes(b)))
 wrong=copy.deepcopy(source);wrong['code_windows'][0]['instructions'][0]['args']='wrong receiver'
 reject('normalized transcript does not match original bytes',lambda:qualify_code(code,wrong))
 changed=bytearray(code);changed[0x31E248-0x31C5D0+1]=0xB7
 adjusted=copy.deepcopy(source);adjusted['function_boundary']['code_sha256']=sha(changed)
 reject('effect read widened to word despite repinned code',lambda:qualify_code(bytes(changed),adjusted))
 observation={'result':'A_ROW_KEY_AND_BYTE_BOUNDARY_QUALIFIED; PENDING_INDEPENDENT_REVIEW',
 'question':'StatusDefinitionRecord +0 two-byte name key versus standalone byte ID/fixed four-byte prefix',
 'records':records,'decoded_bank5_records':names,'native':native,
 'falsified':['standalone byte identity control validates complete name field','fixed001B2800+row first dword','31E1C0 is a valid instruction boundary'],
 'remaining':['meaning of sparse slots11/12/14..1F','normal live reader occurrence and resource binding/lifetime','semantic effect index target','owner canonical propagation'],
 'limits':'Static original code and authored US representation/name correspondence only. No native execution, live initialization, UI presentation, ordinary reachability or universal no-reader proof.',
 'cleanup':'No process/native input APIs, instrumentation, game/save/config/reference writes.'}
 (HERE/'observation.json').write_text(json.dumps(observation,indent=2)+'\n')
 receipt={'result':'PASS_BOUNDED_A_QUALIFICATION','rejecting_controls':cases,'cases':len(cases),
 'positive_controls':['all32 complete two-byte keys','bank5 count/offsets/full terminated names','original status-row read widths and registry identities','counterfactual+2 variation leaves+0 u16 unchanged'],
 'old_byte_only_high_byte_corruption_accepted':True,
 'retained_actual_original_reduce_high_byte_corruption_accepted':True,
 'native_execution':False,'live_execution':False}
 (HERE/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print('PASS',len(cases),'controls;32 name keys; direct original u16 name/u8 effect accesses; NO LIVE')
def require(x):assert x
if __name__=='__main__':main()
