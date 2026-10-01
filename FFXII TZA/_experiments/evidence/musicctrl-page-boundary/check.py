import copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aeF4efbc95a2ffc388cadb36493d5d1d89721f8'.lower()
 assert len(s['bodies'])==2
 x={int(i['pc'],16):i for b in s['bodies'] for i in b['instructions']}
 for b in s['bodies']:
  data=bytes.fromhex(b['raw_hex']);assert sha(data)==b['sha256'] and len(data)==b['size']
  at=int(b['entry'],16)
  for i in b['instructions']:
   ib=bytes.fromhex(i['bytes']);assert int(i['pc'],16)==at
   assert data[at-int(b['entry'],16):at-int(b['entry'],16)+len(ib)]==ib;at+=len(ib)
  assert at==int(b['entry'],16)+b['size']
 def ins(pc,op,args):assert (x[pc]['op'],x[pc]['args'])==(op,args),(hex(pc),x[pc])
 ins(0x3EAB9A,'mov','eax, dword ptr [r8 + 4]');ins(0x3EAB9E,'add','eax, 0x7f')
 ins(0x3EABA1,'cdq','');ins(0x3EABA2,'and','edx, 0x7f');ins(0x3EABA5,'add','eax, edx')
 ins(0x3EABA7,'sar','eax, 7');ins(0x3EABAA,'movsxd','rdx, eax')
 ins(0x3EABAD,'test','eax, eax');ins(0x3EABAF,'jle','0x3eabd6')
 ins(0x3EABB1,'mov','eax, 8');ins(0x3EABB6,'mov','ecx, dword ptr [rax + r8]')
 ins(0x3EABBC,'je','0x3eabcc');ins(0x3EABBE,'add','ecx, r9d');ins(0x3EABC1,'mov','dword ptr [rax + r8], ecx')
 ins(0x3EABCC,'add','rax, 4');ins(0x3EABD0,'sub','rdx, 1');ins(0x3EABD4,'jne','0x3eabb6')
 ins(0x3EAA88,'cmp','dword ptr [r8 + 4], ebx');ins(0x3EAA8C,'jl','0x3eaaf6')
 ins(0x3EAA8E,'mov','eax, ebx');ins(0x3EAA90,'cdq','');ins(0x3EAA91,'and','edx, 0x7f')
 ins(0x3EAA94,'add','eax, edx');ins(0x3EAA96,'sar','eax, 7');ins(0x3EAA99,'movsxd','rcx, eax')
 ins(0x3EAA9C,'movsxd','rax, dword ptr [r8 + rcx*4 + 8]')
 ins(0x3EAAA1,'test','eax, eax');ins(0x3EAAA3,'je','0x3eaaf6');ins(0x3EAAA5,'movzx','ecx, byte ptr [rax]')
 for p in s['refs']:
  b=(HERE/p['retained']).read_bytes();assert sha(b)==p['sha256'] and len(b)==p['bytes']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 driver=(HERE/'retained'/'03-check.py').read_text()
 assert 'gm.w(TAB + 8 + pi * 4, dw(pp))' in driver and 'pp = PAGE + pi * 0x1000' in driver
 assert 'NOT EXERCISED' in driver and 'the loader that fills 0x2B5E0D0' in driver
 r=json.loads((HERE/'retained'/'04-result.json').read_text());cases={c['name']:c for c in r['cases']}
 assert cases['arg-eq-bound']['ok'] and cases['arg-eq-bound']['obs']['ret']==7
 assert cases['arg-over-bound']['ok'] and cases['arg-over-bound']['obs']['ret']==-1
 assert cases['page1']['ok'] and cases['page1']['obs']['ret']==18
 assert cases['page-null']['ok'] and cases['page-null']['obs']['ret']==-1
 assert all(c['trace']=='m V' and not c['faults'] for c in [cases[n] for n in ['arg-eq-bound','arg-over-bound','page1','page-null']])
 # Small nonnegative domain: no overflow/sign bias; original expression becomes floor((n+127)/128).
 witnesses=[]
 for n in [0,127,128,129,1311]:
  count=(n+127)//128;last_page=n//128
  witnesses.append({'inclusive_max':n,'callback_visited_pages':list(range(count)),'reader_final_page_index':last_page,
   'covers_final_page':last_page<count,'inclusive_page_words':last_page+1})
 assert [w['covers_final_page'] for w in witnesses]==[False,True,False,True,True]
 assert witnesses[-1]['callback_visited_pages']==list(range(11)) and witnesses[-1]['reader_final_page_index']==10
 return {'class':'STATIC ORIGINAL PRODUCER/CONSUMER DERIVATION + RETAINED READER OBSERVATIONS',
  'witnesses':witnesses,'boundary':'At max128 callback visits slot0 only, while reader admits field128 and selects slot1. A nonzero file-relative slot1 is not rebased and is interpreted as an absolute sign-extended address.',
  'zero_offset':'If omitted tail slot is zero, reader returns-1; this does not make every such table fault.',
  'shipped_control':'max1311 ->11 rebased slots, final reader index10. Current shipped291-run census remains intact.',
  'fixture_limit':'EXP099 plants absolute page pointers and excludes loader; reader cases/mutations do not cover callback production of final page pointers.',
  'limits':s['limits'],'propagation':'PENDING independent acceptance and FABLE/OPUS owner incorporation'}
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
 reject('max-becomes-exclusive',0x3EAA8C,'jle','0x3eaaf6')
 reject('callback-rounding-now-includes-boundary',0x3EAB9E,'add','eax, 0x80')
 reject('callback-visit-count-changed',0x3EABD0,'sub','rdx, 2')
 reject('reader-page-stride-changed',0x3EAA96,'sar','eax, 6')
 reject('reader-rebases-offset-before-use',0x3EAAA5,'add','rax, r8')
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS','controls':controls,'evidence':'Static boundary calculations and retained finite reader results; no fresh native cases/mutations'},indent=2)+'\n')
 print('PASS exact original seam, shipped/adjacent static witnesses, retained reader controls, five corrupted-derivation controls. No execution repeated.')
if __name__=='__main__':main()
