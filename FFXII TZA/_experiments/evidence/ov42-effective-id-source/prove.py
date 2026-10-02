"""Original effective-ID output/owner preconditions, no natural-state assertion."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
CPIN='b27ee5a03712f3d9bbfcf429fe3277e38de86f236f3ea593ec4aabd479c5e0ab'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def receipt(tag,driver):
 s=json.loads((P/(tag+'.status.json')).read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise ValueError('required invocation failed '+tag)
def derive(source,owner,caller,G):
 ix={int(i['pc'],16):i for x in [source,owner,caller] for r in x['ranges'] for i in r['instructions']}
 def need(pc,m,args):
  if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('effective-ID operation changed '+hex(pc))
 for op in [
  (0x38709b,'mov','rdi, rcx'),(0x38709e,'test','rcx, rcx'),(0x3870a1,'je','0x3870bf'),(0x3870a3,'movzx','eax, byte ptr [rcx + 5]'),(0x3870a7,'test','eax, eax'),(0x3870a9,'jne','0x3870bf'),
  (0x3870ab,'movzx','ebx, byte ptr [rcx + 4]'),(0x3870b6,'shl','rbx, 6'),(0x3870ba,'add','rbx, rax'),(0x3870bd,'jmp','0x3870e9'),
  (0x3870bf,'call','0x31b860'),(0x3870c4,'mov','qword ptr [rip + 0x2b380bd], rax'),(0x3870cb,'test','rax, rax'),(0x3870ce,'je','0x3870e7'),(0x3870d0,'movzx','ebx, byte ptr [rax + 0xea9]'),(0x3870de,'shl','rbx, 6'),(0x3870e2,'add','rbx, rax'),(0x3870e7,'xor','ebx, ebx'),
  (0x3870e9,'mov','rcx, rdi'),(0x3870ec,'call','0x31b860'),(0x3870f6,'test','rax, rax'),(0x3870f9,'je','0x387118'),(0x3870fb,'test','rbx, rbx'),(0x3870fe,'je','0x387118'),(0x387100,'mov','ecx, 0x9f'),(0x387105,'cmp','word ptr [rax + 0x714], cx'),(0x38710c,'jne','0x387118'),(0x38710e,'movzx','eax, word ptr [rbx + 0x10]'),(0x387118,'movzx','eax, word ptr [rax + 0x714]'),
  (0x31b866,'mov','rdi, rcx'),(0x31b869,'test','rcx, rcx'),(0x31b86c,'jne','0x31b876'),(0x31b86e,'xor','eax, eax'),(0x31b875,'ret',''),(0x31b87b,'xor','ebx, ebx'),(0x31b87d,'call','0x236850'),(0x31b882,'test','eax, eax'),(0x31b884,'jle','0x31b8a6'),(0x31b886,'mov','ecx, ebx'),(0x31b888,'call','0x236820'),(0x31b88d,'test','rax, rax'),(0x31b890,'je','0x31b89b'),(0x31b892,'cmp','qword ptr [rax + 0x698], rdi'),(0x31b899,'je','0x31b8a8'),(0x31b89b,'inc','ebx'),(0x31b89d,'call','0x236850'),(0x31b8a2,'cmp','ebx, eax'),(0x31b8a4,'jl','0x31b886'),(0x31b8a6,'xor','eax, eax'),
  (0x304dfd,'mov','rcx, qword ptr [rdi + 0x698]'),(0x304e12,'call','0x387090'),(0x304e17,'mov','edx, dword ptr [rdi + 8]'),(0x304e1a,'movzx','r8d, ax'),(0x304e1e,'mov','r9d, ebx'),(0x304e21,'mov','rcx, r12'),(0x304e24,'call','0x30cfb0')
 ]:need(*op)
 for pc,target in [(0x3870af,'0x208d480'),(0x3870d7,'0x208de80'),(0x3870c4,'0x2ebf188')]:
  if ix[pc]['memory'][0]['rip_target']!=target:raise ValueError('getter table/side-effect identity changed')
 g=G.graph(ix,0x387090,0x387125);og=G.graph(ix,0x31b860,0x31b8b3)
 if g['calls']!=[(0x3870bf,'0x31b860'),(0x3870ec,'0x31b860')] or g['returns']!=[0x387117,0x387124]:raise ValueError('getter effect/exit boundary changed')
 if og['calls']!=[(0x31b87d,'0x236850'),(0x31b888,'0x236820'),(0x31b89d,'0x236850')]:raise ValueError('owner registry boundary changed')
 results=[]
 for table in [False,True]:
  for special in [False,True]:
   fixed={0x3870f9:False,0x3870fe:not table,0x38710c:not special}
   q=G.graph(ix,0x387090,0x387125,fixed=fixed)
   chosen=0x38710e if table and special else 0x387118;ret=0x387117 if table and special else 0x387124
   if q['returns']!=[ret] or not G.dominates(q,chosen,ret):raise ValueError('conditional return source not proved')
   results.append(dict(second_owner='valid nonNULL O2',table_pointer=table,owner_word_is_9F=special,load=hex(chosen),return_pc=hex(ret)))
 null=G.graph(ix,0x387090,0x387125,fixed={0x3870a1:True,0x3870ce:True,0x3870f9:True})
 null_owner=G.graph(ix,0x31b860,0x31b8b3,fixed={0x31b86c:False})
 if null_owner['calls'] or null_owner['returns']!=[0x31b875] or not G.dominates(null_owner,0x31b86e,0x31b875) or not G.dominates(null,0x387118,0x387124):raise ValueError('NULL query/second owner dereference implication changed')
 # The six original operations immediately after the getter return carry AX to
 # R8D and acquire without another call. The retained prefix is an interior
 # fragment; do not invent its entry state or full caller control-flow.
 chain=[pc for pc in sorted(ix) if 0x304e17<=pc<=0x304e24]
 if chain!=[0x304e17,0x304e1a,0x304e1e,0x304e21,0x304e24]:raise ValueError('intervening caller carrier operation changed')
 return dict(conditional_returns=results,
  direct='Given a valid second resolved owner O2, return zero-extends WORD(O2+714) unless it equals9F and RBX table pointer is nonzero. There is no local bound on the direct word; supplied511..534 are non9F and flow unchanged.',
  special='Only O2word9F with nonzero valid table pointer returns zero-extended WORD(table+10). RBX=0 returns9F directly. Table contents/domain/initialization are not established.',
  table_selection='NonNULL query with BYTE(query+5)==0:208D480+BYTE(query+4)*64, no first resolver call. Otherwise first resolver O1 is written to2EBF188; O1nonNULL selects208DE80+BYTE(O1+EA9)*64, O1NULL yieldsRBX0. Mandatory second resolver O2 controls final714 read; O1 andO2 need not be assumed identical.',
  owner_relation='31B860 NULL query returns0 before registry callbacks. NonNULL query scans count236850/index236820, returns matching unit whoseQWORD698 equalsquery or0; count is re-read, state/ABI/valid access/termination premises remain separate.',
  null_boundary='Second owner NULL branches to387118, which reads WORD at0+714, not a sentinel return. NULL query makes both original31B860 calls return0 without registry callbacks, so this source path predicts the low-address714 read. No native execution/observed fault or naturalNULL-caller occurrence.',
  caller_transfer='Exact retained304DFD argument=query atunit698; getter304E12 returnAX zeroextends toR8D304E1A; no intervening call before30CFB0 at304E24. Interior caller fragment, not natural entry/receiver identity proof.',
  acceptance='Local getter does not exclude511..534 on direct non9F valid-owner path. Upstream unitWORD714 writer/admission is the next discriminator; existing slot allocator does not add an ID bound.',
  limits='Stable backed caller/owner/table/frame accesses, normal native ABI/returns and preserved callee-saved carriers are premises. No natural owner identity/lifetime, current table contents/size, full pipeline reachability/accepted command, actual scene timing or wholeOV42 conclusion.')
def main():
 for tag,d in [('capture-01','capture.py'),('owner-01','capture-owner.py'),('feasibility-01','feasibility.py')]:receipt(tag,d)
 f=json.loads((P/'feasibility-01.json').read_text())
 if f.get('complete') is not True or f['driver_sha256']!=sha(P/'feasibility.py') or f['source_sha256']!=sha(P/'source-01.json'):raise ValueError('required feasibility result missing/stale')
 for n,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
  if sha(P/n)!=pin:raise ValueError('reviewed dependency changed')
 source=json.loads((P/'source-01.json').read_text());owner=json.loads((P/'source-owner-01.json').read_text());caller=json.loads((P/'retained-callers-01.json').read_text())
 for x,d in [(source,'capture.py'),(owner,'capture-owner.py')]:
  if x.get('wrapper_complete') is not True or x['invocation_driver_sha256']!=sha(P/d) or x['driver_sha256']!=sha(P/'capture-index-path.py'):raise ValueError('actual capture invocation changed')
 c=json.loads((P/'retained-caller-identity-01.json').read_text())
 if sha(P/'retained-callers-01.json')!=CPIN or c['sha256']!=CPIN or c['commit']!='0ada5145281822af82186ab4f5ee9ec12d46cd81':raise ValueError('retained caller identity changed')
 V=load('roles','validate-title-source-annotations.py');G=load('cfg','prove_owner_reload_order.py');annotations=[V.validate(x) for x in [source,owner,caller]]
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN or any(x['exe_sha256']!=PIN for x in [source,owner,caller]):raise ValueError('wrong original EXE')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 for x,expected in [(source,[(0x387090,0x387125)]),(owner,[(0x31b860,0x31b8b3)]),(caller,[(0x304d70,0x304e29),(0x30eea0,0x30ef05)])]:
  if [(int(r['start'],16),int(r['end_exclusive'],16)) for r in x['ranges']]!=expected:raise ValueError('source population/truncation changed')
  for r in x['ranges']:
   a,b=int(r['start'],16),int(r['end_exclusive'],16)
   if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise ValueError('source bytes differ from original EXE')
 facts=derive(source,owner,caller,G);out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise ValueError('immutable result exists')
 result=dict(producer_complete=True,method='A STATIC_ONLY original getter/resolver and retained caller transfer',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=n,sha256=sha(P/n)) for n in ['source-01.json','source-owner-01.json','retained-callers-01.json']],annotation_prerequisites=annotations,facts=facts,limits=[facts['limits'],'NULL read is source prediction, not observed fault; inputs/owner returns are conditions, not invented natural game state.'],cleanup='Finite offline tools/handles only; no PC/game/native/emulator/save/config/reference/peer changes.')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED direct non9F ownerWORD transfer, conditional substitution and required owner precondition; natural writers remainOPEN')
if __name__=='__main__':main()
