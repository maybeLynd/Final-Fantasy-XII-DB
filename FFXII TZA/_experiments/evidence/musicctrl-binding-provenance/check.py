import copy,hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 expected={0x3EAB60:36,0x51ED10:153,0x379D20:23,0x17D000:129,0x17D4C0:387,0x22A0B0:978}
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);bodies={};x={}
 assert len(s['bodies'])==len(expected)
 for b in s['bodies']:
  a=int(b['entry'],16);data=bytes.fromhex(b['raw_hex']);assert b['size']==expected[a] and len(data)==expected[a] and sha(data)==b['sha256']
  assert (b['runtime_function']['begin'],b['runtime_function']['end'])==(hex(a),hex(a+len(data)))
  ins=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in cs.disasm(data,a)]
  assert ins==b['instructions'] and sum(len(bytes.fromhex(i['bytes'])) for i in ins)==len(data)
  bodies[a]=ins;x.update({int(i['pc'],16):i for i in ins})
 assert set(bodies)==set(expected)
 def ins(pc,op,args):assert (x[pc]['op'],x[pc]['args'])==(op,args),(hex(pc),x[pc])
 ins(0x3EAB64,'mov','edx, 0x20');ins(0x3EAB69,'lea','r8, [rip + 0x20]');assert 0x3EAB70+0x20==0x3EAB90
 ins(0x3EAB70,'lea','ecx, [rdx - 0x17]');assert 0x20-0x17==9
 ins(0x3EAB73,'call','0x51ed10');ins(0x3EAB78,'mov','qword ptr [rip + 0x2773551], rax');assert 0x3EAB7F+0x2773551==0x2B5E0D0
 assert not any(i['op'].startswith('j') or i['op'] in ('cmp','test') for i in bodies[0x3EAB60])
 ins(0x379D24,'call','0x3eac40');ins(0x379D29,'call','0x473d20');ins(0x379D32,'jmp','0x3eab60')
 ins(0x17D01F,'call','0x17d4c0');ins(0x17D5CC,'call','0x22a0b0');ins(0x22A433,'call','0x379d20')
 ins(0x17D074,'mov','byte ptr [rbx + 0x113c], 1')
 ready=[i for i in bodies[0x17D000] if '0x113c' in i['args']];assert len(ready)==1 and ready[0]['pc']=='0x17d074'
 # Positive control for conditional-flow detection: this entry does contain a separate allocation-null test.
 ins(0x17D033,'test','rax, rax');ins(0x17D036,'je','0x17d041')
 ins(0x51ED52,'call','0x32e400');ins(0x51ED57,'mov','edx, 9');ins(0x51ED5E,'lea','ecx, [rdx - 4]')
 ins(0x51ED61,'call','0x36c1d0');ins(0x51ED68,'call','0x36a190');ins(0x51ED6D,'mov','rbx, rax')
 ins(0x51ED70,'call','0x36c140');ins(0x51ED7D,'mov','r8, rbx');ins(0x51ED89,'call','0x32e620');ins(0x51ED93,'mov','rax, rbx')
 assert not any(i['op'].startswith('j') or i['op'] in ('cmp','test') for i in bodies[0x51ED10])
 for p in s['refs']:
  data=(HERE/p['retained']).read_bytes();assert sha(data)==p['sha256'] and len(data)==p['bytes']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 page=(HERE/'retained'/'00-the-music-control-file-and-the-bgm-stream.md').read_text()
 mc=(HERE/'retained'/'01-CONTRACT-music-control-file-and-bgm-stream.md').read_text()
 field=(HERE/'retained'/'02-CONTRACT-field-music-selection.md').read_text()
 assert 'process and never rebound or freed: its lifetime is the process.' in page
 assert 'ONCE PER PROCESS and never rebound or freed' in mc
 assert "The table's lifetime after binding" in field and 'UNKNOWN / NOT EXERCISED' in field
 return {'supported':[
  'Direct startup path17D000 ->17D4C0 ->22A0B0 ->379D20 tail3EAB60 ->51ED10 then global02B5E0D0=returned pointer.',
  'Binding entry unconditionally calls shared loader with kind9/index32/callback3EAB90; no local old-pointer/one-shot guard.',
  'Selected application entry sets ready113C last and never reads it; its null-allocation branch is not a ready/once gate.',
  'Shared loader selects heap5 using36C1D0(5,9), allocates through36A190, restores selection36C140, passes pointer to requester and returns allocated RBX, not requester return. Callee internals not freshly qualified.'],
  'unresolved':['Normal framework invocation count/per-instance versus per-process initialization and possible reentry/reinitialization.',
   'Heap5 block release/reset/teardown/alias paths and actual post-load pointer lifetime. One global writer count cannot establish these.'],
  'contradiction':'MC-1/page assert process lifetime/never freed while field-selection lifetime row explicitly says UNKNOWN/NOT EXERCISED; reconcile without guessing.',
  'not_claimed':'No ordinary rebind or free observed/proved; no repeated injected call, no new census, no live startup/callback readiness/pointer-lifetime test.',
  'next_cheapest_method':'Owner trace normal framework caller of17D150/17D000 and heap5 release/reset provenance offline first; only escalate remaining actual lifecycle question with prepared C trigger/controls/consumer.',
  'propagation':'PENDING independent review and FABLE/OPUS adjudication; local publication not semantic closure.',
  'limits':s['limits']}
def main():
 s=json.loads((HERE/'primary.json').read_text());out=derive(s);controls=[]
 for name,pc,args in [('wrong-kind-index',0x3EAB64,'edx, 0x21'),('ready-store-relabelled-as-test',0x17D074,'byte ptr [rbx + 0x113c], 0'),('request-result-relabelled-as-buffer',0x51ED93,'rax, rax')]:
  q=copy.deepcopy(s)
  for b in q['bodies']:
   for i in b['instructions']:
    if i['pc']==hex(pc):i['args']=args
  try:derive(q)
  except AssertionError:controls.append({'name':name,'rejected':True});continue
  raise AssertionError('INVALID_CONTROL '+name)
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS','positive_control':'Actual application-entry allocation-null TEST/JE detected separately from ready-store; exact bodies disassembled again from preserved bytes.',
  'controls':controls,'class':'Static artifact-corruption controls, not native mutations/normal invocation experiments'},indent=2)+'\n')
 print('PASS exact startup/binding/loader flow; local guard absent; frequency/lifetime explicitly unresolved.')
if __name__=='__main__':main()
