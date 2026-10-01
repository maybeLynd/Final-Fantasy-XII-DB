import hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s,results):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);instructions={}
 assert [(int(b['entry'],16),b['size']) for b in s['bodies']]==[(0x1DB550,172),(0x22C940,43),(0x22C970,533),(0x22C930,11),(0x1DB640,21),(0x20F310,197),(0x1DB660,358)]
 for b in s['bodies']:
  raw=bytes.fromhex(b['raw_hex']);assert len(raw)==b['size'] and sha(raw)==b['sha256']
  ii=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in cs.disasm(raw,int(b['entry'],16))]
  assert ii==b['instructions'] and sum(len(bytes.fromhex(i['bytes'])) for i in ii)==len(raw)
  instructions.update({i['pc']:i for i in ii})
 def ins(pc,op,args):assert (instructions[pc]['op'],instructions[pc]['args'])==(op,args)
 ins('0x1db56c','xor','esi, esi');ins('0x1db5b9','mov','byte ptr [rsp + 0x20], sil')
 ins('0x1db5c0','lea','r8, [rip + 0x79]');assert 0x1DB5C7+0x79==0x1DB640
 ins('0x1db5e0','call','0x22c940');ins('0x22c944','mov','eax, dword ptr [rsp + 0x60]')
 ins('0x22c948','mov','dword ptr [rsp + 0x28], eax');ins('0x22c961','call','0x22c970')
 ins('0x22c9bb','mov','r13d, dword ptr [rsp + 0x98]');ins('0x22cb27','mov','r8d, r13d')
 ins('0x22cb30','call','r14');ins('0x1db643','test','r8d, r8d');ins('0x1db64c','setne','r8b')
 ins('0x1db650','jmp','0x1db660');ins('0x1db67d','movzx','r14d, r8b')
 ins('0x1db729','mov','byte ptr [rdx + rax], r14b')
 for p in s['refs']:
  b=(HERE/p['retained']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 assert set(s['stubs'])=={'0x1a1470','0x861eba','0x16d6a0'}
 expected=[('DIRECT-clean-control',0,0x50,0),('DIRECT-upper-byte',0x100,0x50,1),
  ('DIRECT-low-byte-overwritten',1,0x50,0),('DIRECT-high-bit',0x80000000,0x50,1),
  ('DIRECTHL-clean-control',0,0x51,0),('DIRECTHL-upper-byte',0x100,0x51,1)]
 assert len(results)==len(expected)>0
 rows=[];pcs=['0x1db5b9','0x1db5be','0x22c944','0x22c948','0x22c9bb','0x22c9c3','0x22cb27','0x22cb30',
  '0x1db640','0x1db643','0x1db64c','0x1db650','0x1db67d','0x1db729']
 fixture=s['fixture'];slot=fixture['flag_slot']
 for r,(name,seed,command,flag) in zip(results,expected,strict=True):
  assert (r['name'],r['seed_dword'],int(r['command'],16))==(name,seed,command)
  assert r['entry']=='0x1db550' and r['entry_rsp']==fixture['stack'] and r['flag_slot']==slot
  assert r['returned'] and not r['failure'] and not r['faults'] and r['nonvolatile_preserved'] and r['original_code_unchanged']
  assert int(r['final_rsp'],16)==int(r['entry_rsp'],16)+8 and 0<r['instruction_count']<5000
  assert len(r['steps'])==r['instruction_count'] and all(p in instructions or p in s['stubs'] for p in r['steps'])
  assert r['before']['slot_dword']==seed and r['after']['slot_dword']==(seed&0xFFFFFF00)
  assert r['before']['gate']==1 and r['before']['initial_object_counts']==[7,7]
  assert r['after']['packet_hex']==r['before']['packet_hex'] and r['after']['object_counts']==[1,1]
  assert r['after']['flags_hex']==bytes([flag,0xA5,0xA5,0xA5]).hex()
  assert r['after']['copy_hex']==r['before']['packet_hex'][8:]+('a5'*16)
  assert r['after']['stored_copy_pointer']==fixture['copy'] and r['after']['reset_installed_count']==0
  trace=r['trace'];assert [t['pc'] for t in trace]==pcs
  for t in trace:assert t['instruction']==instructions[t['pc']]
  bypc={t['pc']:t for t in trace}
  assert int(bypc['0x1db5b9']['rsp'],16)+0x20==int(slot,16)
  assert int(bypc['0x22c944']['rsp'],16)+0x60==int(slot,16)
  assert bypc['0x22c948']['rax']==hex(seed&0xFFFFFF00)
  assert bypc['0x22c9c3']['r13']==hex(seed&0xFFFFFF00)
  assert bypc['0x22cb30']['r8']==bypc['0x1db643']['r8']==hex(seed&0xFFFFFF00)
  assert bypc['0x22cb30']['rcx']==hex(int(fixture['packet'],16)+4) and bypc['0x22cb30']['rdx']==fixture['object']
  assert bypc['0x1db650']['r8']==hex((seed&0xFFFFFF00)|flag) and bypc['0x1db729']['r14']==hex(flag)
  mem=r['watched_memory_events'];assert len(mem)==3
  assert mem[0]=={'kind':'write','pc':'0x1db5b9','address':slot,'size':1,'value_hex':'00'}
  assert mem[1]=={'kind':'read','pc':'0x22c944','address':slot,'size':4,'value_hex':(seed&0xFFFFFF00).to_bytes(4,'little').hex()}
  assert mem[2]=={'kind':'write','pc':'0x1db729','address':fixture['flag_array'],'size':1,'value_hex':bytes([flag]).hex()}
  calls=r['stub_calls'];assert [c['pc'] for c in calls]==['0x1a1470','0x861eba','0x16d6a0']
  assert calls[0]['rdx']=='0x10' and (calls[1]['rcx'],calls[1]['rdx'],calls[1]['r8'])==(fixture['copy'],hex(int(fixture['packet'],16)+4),'0x10')
  assert calls[2]['rdx']==fixture['copy']
  rows.append({'case':name,'seed':hex(seed),'after_real_byte_store':hex(seed&0xFFFFFF00),'callback_dword':bypc['0x1db643']['r8'],
   'collected_flag':flag,'instructions':r['instruction_count'],'class':'Isolated shipping-code execution with controlled state and three native-effect stubs'})
 return {'method':'B — isolated original caller-to-collector execution','observations':rows,
  'established':'In this original call chain, a zero low flag byte does not imply a zero collected flag. The original wrapper/decoder forward all32 bits and adapter tests all32 before converting to byte0/1. Supplied nonzero upper bytes survive the real caller byte store and produce1; supplied low1 alone is overwritten and produces0.',
  'semantic_implication':'Preserve access widths and the argument-slot initialization precondition. Do not model this path as merely copying the byte written by GiVmax or as DIRECT versusDIRECTHL selecting its bool. A source-level bool/int label cannot erase the physical width difference.',
  'limits':'Controlled guest stack/object/one EOP packet; three disclosed stubs. Native allocator/copy/registration effects, actual upper stack values, normal reachability, scheduler, replay and visual outcomes are NOT established. No claim that original game output normally differs or crashes.',
  'cleanup':'Guest processes end/disposable memory discarded; no FF12/native attach/input/save/config/reference writes. Original guest code and source packet unchanged in each retained run; no fresh live restoration receipt.',
  'affected_consumers':['FABLE legacy VIF/GIF mechanism and callback description','OPUS exact wrapper/decoder/adapter/collector argument widths and preconditions'],
  'propagation':'PENDING independent review and owner incorporation'}
def main():
 s=json.loads((HERE/'source.json').read_text());results=json.loads((HERE/'raw-results.json').read_text());out=derive(s,results)
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_ISOLATED_ORIGINAL_CODE','cases':len(results),
  'native_or_live_cases':0,'baseline_and_low_overwrite_controls_retained':True,'disclosed_native_effect_stubs':3,
  'limits':'Raw/source reduction only; no rerun, independent review or full mutation campaign acceptance.'},indent=2)+'\n')
 print('PASS: original byte-store/dword-forward/nonzero-test/byte-result chain; all raw controls and stub limits checked.')
if __name__=='__main__':main()
