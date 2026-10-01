import copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and len(s['bodies'])==3
 x={int(i['pc'],16):i for b in s['bodies'] for i in b['instructions']}
 for b in s['bodies']:
  data=bytes.fromhex(b['raw_hex']);assert sha(data)==b['sha256'] and len(data)==b['size']
  at=int(b['entry'],16)
  for i in b['instructions']:
   raw=bytes.fromhex(i['bytes']);assert int(i['pc'],16)==at and data[at-int(b['entry'],16):at-int(b['entry'],16)+len(raw)]==raw;at+=len(raw)
  assert at==int(b['entry'],16)+b['size']
 getter=s['bodies'][0]['instructions'];assert len(getter)==10 and getter[-1]['op']=='ret'
 def ins(pc,op,args):assert (x[pc]['op'],x[pc]['args'])==(op,args),(hex(pc),x[pc])
 ins(0x265270,'test','byte ptr [rip + 0x1e33ba9], 1');assert 0x265277+0x1E33BA9==0x2098E20
 ins(0x265277,'je','0x265289');ins(0x265279,'mov','rax, qword ptr [rip + 0x1e33bd8]');assert 0x265280+0x1E33BD8==0x2098E58
 ins(0x265280,'test','rax, rax');ins(0x265283,'je','0x265289');ins(0x265285,'movzx','eax, word ptr [rax]')
 ins(0x265289,'xor','eax, eax')
 assert not any(i['op']=='call' for i in getter)
 # Aligned from initializer entry, not a guessed interior fragment.
 assert 0x266EDC not in x and 0x266EE0 in x and s['bodies'][2]['scope'].startswith('initializer prefix')
 ins(0x266EE0,'lea','rbx, [rip + 0x1e31f39]');assert 0x266EE7+0x1E31F39==0x2098E20
 ins(0x266EF0,'lea','rcx, [rbx - 0x10]');ins(0x266EF4,'xor','edx, edx')
 ins(0x266EF6,'mov','r8d, 0x288');ins(0x266EFC,'call','0x861ec0')
 ins(0x266F01,'and','byte ptr [rbx], 0xfe');ins(0x266F2D,'lea','rbx, [rbx + 0x288]')
 ins(0x266F34,'cmp','edi, 5');ins(0x266F37,'jl','0x266ef0')
 ins(0x3EAA78,'call','0x265270');ins(0x3EAA84,'movzx','r11d, ax')
 ins(0x3EAAFF,'movzx','r9d, byte ptr [rax + 3]');ins(0x3EAB2C,'cmp','r11d, ecx');ins(0x3EAB2F,'jle','0x3eab42')
 for p in s['refs']:
  data=(HERE/p['retained']).read_bytes();assert sha(data)==p['sha256'] and len(data)==p['bytes']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 t=(HERE/'retained'/'type-row.txt').read_bytes();assert sha(t)==s['type_source']['selected_row_sha256']
 assert t.startswith(b'ActorManagerSlot\t0x288\t') and b'0x02098E10 + slot * 0x288' in t
 driver=(HERE/'retained'/'02-check.py').read_text()
 for fragment in ['G_LIVE   = 0x2098E20','G_VARPTR = 0x2098E58','gm.w(G_LIVE, bytes([case.get("live", 1)]))','gm.w(G_VARPTR, qw(0 if case.get("var_null") else VARB))']:
  assert fragment in driver
 assert 'A("dead-actor",  "m V", 7, arg=5, pages=P0, live=0, progress=50)' in driver
 result=json.loads((HERE/'retained'/'03-result.json').read_text());by={c['name']:c for c in result['cases']}
 for name in ['base','dead-actor','varblock-null']:
  c=by[name];assert c['ok'] and c['obs']['ret']==7 and c['trace']=='m V' and not c['faults']
 return {'physical_identity':{'flag':hex(0x2098E20),'manager_array_base':hex(0x2098E10),'flag_offset':hex(0x10),
  'var_pointer':hex(0x2098E58),'var_pointer_offset':hex(0x48),'stride':hex(0x288),'count':5},
  'actually_tested':'Supplied manager-slot0 bit0 clear / null supplied variable bank yields getter0 and default ladder result7 in retained EXP099.',
  'not_established':'No normal combat death, health transition, actor input/trigger, audible/default-track consequence or death->manager-gate causality is in those observations.',
  'original_producer':'The initializer prefix clears bit0 across manager slots independently of any inspected actor-health transition; frequency/caller effects are not asserted.',
  'consumer_narrowing':'Replace unqualified default-track-for-dead-actor implication with the observed manager-gate/null-bank condition; leave actual death consequence pending separate evidence if claimed.',
  'retained_validity':'Original gate/threshold cases and mutations retained. No22/20 replay, no retraction of actual supplied-state returns.',
  'limits':s['limits'],'propagation':'PENDING owner repair/independent acceptance'}
def main():
 s=json.loads((HERE/'primary.json').read_text());out=derive(s);controls=[]
 def reject(name,pc,op,args):
  q=copy.deepcopy(s)
  for b in q['bodies']:
   for i in b['instructions']:
    if i['pc']==hex(pc):i['op']=op;i['args']=args
  try:derive(q)
  except (AssertionError,KeyError,ValueError):controls.append({'name':name,'rejected':True});return
  raise AssertionError('INVALID_CONTROL '+name)
 reject('wrong-gate-mask',0x265270,'test','byte ptr [rip + 0x1e33ba9], 2')
 reject('actor-pointer-substituted-for-fixed-global',0x265279,'mov','rax, qword ptr [rcx + 0x48]')
 reject('wrong-manager-object-size',0x266EF6,'mov','r8d, 0x740')
 reject('gate-off-no-longer-yields-zero',0x265289,'mov','eax, 50')
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS','controls':controls,'class':'Original static identity/flow and retained finite fixture; no new execution/death test'},indent=2)+'\n')
 print('PASS original manager identity, retained supplied gates/default returns and four corrupted-derivation controls; no death test claimed.')
if __name__=='__main__':main()
