import copy,hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def qualify(rows,source):
 assert source['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 assert len(rows)==4
 by={int(r['descriptor_count_u32'],16):r for r in rows};assert set(by)=={0,8,0xFFFFFFF9,0xFFFFFFF8}
 for count,r in by.items():
  assert r['faults']==[] and r['error'] is None and 0<r['instruction_callbacks']<6000
  seq=[e['sequence'] for e in r['events']]
  assert all(0<s<=r['instruction_callbacks'] for s in seq) and all(a<b for a,b in zip(seq,seq[1:]))
  assert int(r['initial_rsp'],16)&15==8
  args=[e for e in r['events'] if e['pc']=='0x630a0000'];assert len(args)==1
  arg=args[0];assert arg['value']==0 and int(arg['rsp'],16)&15==8
  assert arg['byte_count']==((count+7)&0xFFFFFFFF)>>3
  before=bytes.fromhex(r['before_hex']);after=bytes.fromhex(r['after_hex']);assert len(before)==len(after)==78
  assert before[:16]==b'\xC3'*16 and before[16:62]==b'\xA5'*46 and before[62:]==b'\x3C'*16
  if count==0xFFFFFFF8:
   assert r['planned_boundary_stop'] and r['end']==arg['pc'] and after==before and not r['scripted_bridge_trace']
   assert not any(e['pc'] in ('0x2f8ffc','0x2f8fff') for e in r['events'])
  else:
   assert not r['planned_boundary_stop'] and r['end']=='0x62000000' and r['rax']=='0x0'
   expected=bytearray(before)
   if count==8:expected[16]=0
   assert after==bytes(expected)
   tests=[e for e in r['events'] if e['pc']=='0x2f8ffc'];assert len(tests)==1 and tests[0]['sequence']>arg['sequence']
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
 instructions={}
 for body in source['code']:
  raw=bytes.fromhex(body['hex']);assert len(raw)==body['bytes'] and sha(raw)==body['sha256']
  ins=list(md.disasm(raw,int(body['entry'],16)));assert sum(i.size for i in ins)==len(raw)
  actual=[{'address':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins];assert actual==body['instructions']
  instructions.update({i.address:(i.mnemonic,i.op_str) for i in ins})
 assert instructions[0x2F8FD3]==('lea','r8d, [rax + 7]')
 assert instructions[0x2F8FD9]==('shr','r8, 3')
 assert instructions[0x2F8FE0]==('call','0x861ec0')
 assert instructions[0x2F8FFF]==('jle','0x2f90a3')
 assert instructions[0x323BCD]==('lea','r8, [rsp + 0x20]')
 assert instructions[0x323BCB]==('xor','ecx, ecx')
 clears=[(0x323BD4,8,'qword ptr [rsp + 0x20], rcx'),(0x323BD9,8,'qword ptr [rsp + 0x28], rcx'),
 (0x323BE2,8,'qword ptr [rsp + 0x30], rcx'),(0x323BE7,8,'qword ptr [rsp + 0x38], rcx'),
 (0x323BEC,8,'qword ptr [rsp + 0x40], rcx'),(0x323BF1,4,'dword ptr [rsp + 0x48], ecx'),(0x323BF5,2,'word ptr [rsp + 0x4c], cx')]
 assert sum(n for a,n,args in clears)==46
 for a,n,args in clears:assert instructions[a]==('mov',args)
 assert instructions[0x323BFC]==('call','0x2f8fa0')
 return by
def main():
 source=json.loads((HERE/'source.json').read_text());rows=json.loads((HERE/'raw-results.json').read_text());by=qualify(rows,source)
 driver=(HERE/'retained-driver.txt').read_bytes();assert sha(driver)==source['driver_sha256']
 dq=json.loads((HERE/'driver-qualification.json').read_text());assert dq['normalized_equal'] and dq['AST_equal'] and dq['prior_new_native_results']==0
 assert sha(driver.replace(b'\r\n',b'\n'))==source['driver_git_sha256']
 controls=[]
 def reject(name,f):
  try:f()
  except AssertionError:controls.append({'name':name,'rejected':True})
  else:raise AssertionError('control not rejected '+name)
 reject('zero count guarantees entire46-byte output clear',lambda:need(bytes.fromhex(by[0]['after_hex'])[16:62]==b'\0'*46))
 reject('signed loop skip suppresses previous oversized clear request',lambda:need(next(e['byte_count'] for e in by[0xFFFFFFF8]['events'] if e['pc']=='0x630a0000')==0))
 reject('boundary capture is a completed oversized native clear',lambda:need(by[0xFFFFFFF8]['end']=='0x62000000'))
 bad=copy.deepcopy(rows);bad[0]['events'][-1]['sequence']=0
 reject('callback/order proof lost',lambda:qualify(bad,source))
 bad=copy.deepcopy(rows);bad[0]['initial_rsp']='0x61080000'
 reject('misaligned Win64 function-entry precondition',lambda:qualify(bad,source))
 bad=copy.deepcopy(rows);bad[1]['after_hex']=bad[1]['before_hex']
 reject('positive scripted-bridge one-byte change missing',lambda:qualify(bad,source))
 bad=copy.deepcopy(source);bad['exe_sha256']='0'*64
 reject('wrong reference identity',lambda:qualify(rows,bad))
 observation={'result':'B_BOUNDED_CLEAR_ARGUMENT_AND_WARM_OUTPUT; PENDING_REVIEW',
 'question':'Physical clearing versus logical empty mask / caller preclear / signed loop gate',
 'established':{'count0':'original call argument0; warm46 physical output remains unchanged under disclosed bridge; return0',
 'count8_positive':'original argument1, bridge clears exactly first output byte; return0/canaries intact',
 'countFFFFFFF9':'32-bit wrap gives clear argument0, signed loop skipped; warm bytes unchanged; return0',
 'countFFFFFFF8':'original clear argument536870911 before loop gate; captured/stopped before bridge; no large clear attempted',
 'caller_preclear':'original PREREQ writes46 zero bytes in its own temporary BEFORE builder call (A), a distinct initialization guarantee'},
 'interpretation':'Do not infer a physical46-byte output guarantee from a zero-sized logical mask. The PREREQ zero mask is supplied by caller. Signed loop rejection is after the clear-size call and cannot guarantee that call was skipped.',
 'limits':'Supplied guest descriptors/rows/output, no real initialization/reachability; memset bridge scripted, no native CRT effect proof. Oversized case is argument/order only; no completed clear/corruption/fault claim. PREREQ preclear is static, not newly executed. No57/35 campaign replay.',
 'affected':['OPUS licence contract section13 builder/caller initialization wording','malformed-count ABI precondition; underlying EXP140 original requested edge remains answered'],
 'cleanup':'No live FF12/process/control/native OS input/instrument/save/config/reference writes. Guest sessions bounded and ended.'}
 (HERE/'observation.json').write_text(json.dumps(observation,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'result':'PASS_SCOPED_B_AND_A_CONTROLS','native_cases':4,'completed_small_cases':3,'planned_entry_boundary_cases':1,
 'rejecting_controls':controls,'controls':len(controls),'big_clear_executed':False,'live_game':False,'independent_acceptance':False},indent=2)+'\n')
 print('PASS4 bounded cases (3 small returns/1 planned boundary);',len(controls),'controls; no large/native CRT/live claim')
def need(x):assert x
if __name__=='__main__':main()
