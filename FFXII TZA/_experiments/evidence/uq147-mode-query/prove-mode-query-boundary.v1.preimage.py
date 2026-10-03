"""Bounded original CFG/effect composition, not emulation or natural reachability."""
import copy,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def checked_status(s,pin):
 need(s.get('terminal') is True and s.get('exit')==0 and s.get('exception') is None and s.get('driver_sha256')==pin,'required upstream capture failed/incomplete')
def index(s):return {int(i['pc'],16):i for r in s['ranges'] for i in r['instructions']}
def ins(ix,pc,m,args):need(pc in ix and (ix[pc]['mnemonic'],ix[pc]['args'])==(m,args),'required instruction/transfer changed '+hex(pc))
def mem(ix,pc,**fields):
 z=ix[pc]['memory'];need(len(z)==1 and all(z[0].get(k)==v for k,v in fields.items()),'required memory effect/address changed '+hex(pc))
def closed(r,calls):
 ix={int(i['pc'],16):i for i in r['instructions']};end=int(r['end_exclusive'],16)
 need(bool(ix) and list(ix)[0]==int(r['start'],16),'empty/incomplete body')
 got=[]
 for pc,i in ix.items():
  nxt=pc+len(bytes.fromhex(i['bytes']))
  need(nxt in ix or nxt==end,'uncovered instruction boundary')
  if i['mnemonic']=='call':
   need(i['args'].startswith('0x'),'unresolved call');got.append(int(i['args'],16))
  elif i['mnemonic'].startswith('j'):
   need(i['args'].startswith('0x') and int(i['args'],16) in ix,'unresolved/outside branch')
  elif i['mnemonic']!='ret':need(nxt in ix,'fallthrough outside complete body')
 need(got==calls,'helper call chain changed')
 need(any(i['mnemonic']=='ret' for i in ix.values()),'no normal return')
 need(not any(m['role'] in ('w','rw') for i in ix.values() for m in i['memory']),'object write in closed query')
def derive(s,caller,selector):
 ix=index(s);c=index(caller);sel=index(selector)
 need(len(s['ranges'])==4,'helper count changed')
 for r,calls in zip(s['ranges'],[[0x3148f0],[0x2ef2b0],[0x2ef640],[]]):closed(r,calls)
 for pc,m,a in [
  (0x377c20,'sub','rsp, 0x28'),(0x377c24,'call','0x3148f0'),(0x377c30,'test','r8, r8'),(0x377c33,'je','0x377c5f'),(0x377c35,'cmp','eax, dword ptr [r8 + 4]'),(0x377c39,'jae','0x377c5f'),(0x377c3b,'movsxd','rcx, eax'),(0x377c3e,'lea','rax, [r8 + rcx*2]'),(0x377c42,'movzx','edx, byte ptr [rcx + rax + 9]'),(0x377c47,'lea','rax, [r8 + rcx*2]'),(0x377c4b,'movzx','ecx, byte ptr [rcx + rax + 8]'),(0x377c50,'shl','edx, 8'),(0x377c53,'add','edx, ecx'),(0x377c55,'shr','edx, 0xf'),(0x377c58,'mov','eax, edx'),(0x377c5a,'add','rsp, 0x28'),(0x377c5e,'ret',''),(0x377c5f,'mov','edx, 0xfff'),(0x377c64,'shr','edx, 0xf'),(0x377c67,'mov','eax, edx'),(0x377c69,'add','rsp, 0x28'),(0x377c6d,'ret',''),
  (0x3148f0,'sub','rsp, 0x28'),(0x3148f4,'call','0x2ef2b0'),(0x3148f9,'xor','ecx, ecx'),(0x3148fb,'mov','eax, dword ptr [rax + 0x1044]'),(0x314901,'test','eax, eax'),(0x314903,'cmovs','eax, ecx'),(0x314906,'add','rsp, 0x28'),(0x31490a,'ret',''),
  (0x2ef2b0,'sub','rsp, 0x28'),(0x2ef2b4,'call','0x2ef640'),(0x2ef2b9,'add','rax, 0x200'),(0x2ef2bf,'add','rsp, 0x28'),(0x2ef2c3,'ret',''),(0x2ef640,'ret','')]:
  if pc==0x2ef640:continue
  ins(ix,pc,m,a)
 need(len(ix)==37,'extra/uncovered helper instruction')
 ins(ix,0x2ef640,'lea','rax, [rip + 0x1e74c39]');ins(ix,0x2ef647,'ret','')
 mem(ix,0x2ef640,role='addr',rip_target='0x2164280',size=8)
 mem(ix,0x3148fb,role='r',base='rax',displacement=0x1044,size=4)
 mem(ix,0x377c29,role='r',rip_target='0x2add100',size=8)
 mem(ix,0x377c35,role='r',base='r8',displacement=4,size=4)
 for pc,d in [(0x377c42,9),(0x377c4b,8)]:mem(ix,pc,role='r',base='rcx',index='rax',scale=1,displacement=d,size=1)
 for pc in [0x377c3e,0x377c47]:mem(ix,pc,role='addr',base='r8',index='rcx',scale=2,displacement=0)
 mode=next(r for r in caller['ranges'] if r['start']=='0x30d9a0');closed(mode,[0x377c20])
 for pc,m,a in [(0x30d9b1,'test','cl, 8'),(0x30d9b4,'je','0x30d9c0'),(0x30d9c0,'test','cl, 4'),(0x30d9c3,'je','0x30d9cf'),(0x30d9cf,'call','0x377c20'),(0x30d9d4,'test','eax, eax'),(0x30d9d6,'je','0x30d9e2'),(0x30d9ef,'test','cl, 2'),(0x30d9f2,'je','0x30d9fe'),(0x30d9fe,'movzx','eax, cl'),(0x30da01,'and','eax, 1')]:ins(c,pc,m,a)
 for pc in [0x30d9a4,0x30d9e2]:mem(c,pc,role='r',rip_target='0x2ebf190',size=8)
 for pc in [0x30d9ab,0x30d9e9]:mem(c,pc,role='r',base='rax',displacement=0x5b04,size=4)
 # Connect only already-qualified selector and Dismiss early return paths.
 for pc,m,a in [(0x3138d8,'call','0x30d9a0'),(0x3138dd,'cmp','eax, 1'),(0x3138e0,'jne','0x31398d'),(0x3138e6,'lea','ecx, [rax + 2]'),(0x3138e9,'call','0x31b8c0'),(0x3138ee,'test','rax, rax'),(0x3138f1,'je','0x31398d'),(0x313903,'bt','rdx, 0xe'),(0x313908,'jae','0x313915'),(0x31390a,'movzx','ecx, word ptr [rax + 0xba0]'),(0x313911,'cmp','ecx, ebp'),(0x313913,'je','0x313988'),(0x313915,'cmp','word ptr [rax + 0x714], bp'),(0x31391c,'je','0x313988'),(0x3138fe,'mov','ebp, 0x113'),(0x313988,'mov','rbp, qword ptr [rsp + 0x48]'),(0x31398d,'add','rsp, 0x30'),(0x313991,'pop','rsi'),(0x313992,'ret','')]:ins(c,pc,m,a)
 for pc,d,size in [(0x3138f7,0,4),(0x31390a,0xba0,2),(0x313915,0x714,2)]:mem(c,pc,role='r',base='rax',displacement=d,size=size)
 mem(c,0x3138f9,role='w',base='rsp',displacement=0x48,size=8)
 # This reachable main-path write is a positive detector, excluded by all early returns.
 mem(c,0x313981,role='rw',base='rcx',displacement=0x5ad0,size=2)
 need(c[0x31395d]['mnemonic']=='call' and c[0x31395d]['args']=='0x311cf0','request positive detector missing')
 need(not any(m['role'] in ('w','rw') for i in sel.values() for m in i['memory']),'qualified selector object write changed')
 return dict(
  query='Closed377C20->3148F0->2EF2B0->2EF640 has no object writes/opaque calls on any normal local path. Stack CALL/RET/sub/add effects remain private-valid-stack premises.2EF640 forms reference address02164280; payload+200 then fieldDWORD+1044 means reference cell021654C4. Signednegative field id clamps0; otherwise signednonnegative id. Descriptor QWORD02ADD100 NULL or unsigned index>=DWORDdesc+4 returns0. Accepted index readsBYTEdesc+8+3*id andBYTEdesc+9+3*id, assembles16 bits and returns bit15.',
  mode='30D9A0 has no object writes/opaque calls after closing377C20. First modeDWORD read bit3->5/bit2->4; helpertrue->3; second modeDWORD read bit1->2/else bit0->0or1. The pointer/mode are read twice; no atomic/stability guarantee without noninterference.',
  conditional_counterexample='With both mode reads1 and closedfieldhelperfalse,3138D0(0) selects roster index3. Empty actor/unit returns immediately. For a nonNULL valid unit, (flagbit14 and pendingWORD+BA0==113) OR committedWORD+714==113 returns before311CF0 and before direct5AD0 write. The committed branch is reached if flagbit14clear or pending!=113. Only private saved-RBP/RSI stack operations occur on those paths; no battle mode/member/KO/object writes in the closed calls or selected path.',
  implication='A call to3138D0(0) alone does not universally guarantee a cleanup/state change. Under these conditional supplied-state premises, mode1 can survive that call. Same-call order from the predecessor does not by itself prove cleanup completed before23B040. No full constructor/interpreter/gameplay proof follows.',
  premises='Exact intact complete shipping code; readable static image fieldcell, battle pointer/mode, descriptor and accepted row if present, roster/actor/unit queried fields; normal ABI/private valid separated stack, normal returns, no interference or aliasing of stack stores into observed objects. Addresses are reference-image identities, not observed process pointers.',
  unresolved='Whether real initialized summon+KO state can reach any early-return case, whether recompute sees same unit/mode/status, preceding KO processing, lifetime/ownership/scheduling/presentation and wholeUQ147 remain OPEN.')
def main():
 out=P/sys.argv[1];need(not out.exists(),'fresh result required')
 cap_pin='05173bedcdc789bdfa04524460d77967f95ad31aefe04d453ff2186f68c32008'
 status_path=P/(sys.argv[2] if len(sys.argv)>2 else 'capture-mode-query-01.status.json')
 checked_status(json.loads(status_path.read_text()),cap_pin)
 need(sha(P/'capture-mode-query-boundary.py')==cap_pin,'capture producer changed')
 paths=[('source-mode-query-01.json','2218c4f027e33a8d878c65301004911e83076848de74303c2b44de3824473651'),('source-boundary-01.json','7ff80975a29c048ec08a1915669cf1d62ffd1eb5d6878503e0330a059e0f2b25'),('source-selector-01.json','d788aa2956d6c8c47e9d630e0e9321861d61541b3c6648fdd81c16ecbbf8d9ba')]
 sources=[]
 for name,pin in paths:
  need(sha(P/name)==pin,'source preimage changed '+name);x=json.loads((P/name).read_text());need(x.get('wrapper_complete') is True,'incomplete source');sources.append(x)
 for tag,pin in [('capture-boundary-01','b84224cf1d15ad3ea2d96356d8d68e26c8064358886682cbf7383ffdbf8f738e'),('capture-selector-01','4dde5e091a8c95718fc21f2003718552bc7c241faf7e2dcabd61205b7ae70737')]:checked_status(json.loads((P/(tag+'.status.json')).read_text()),pin)
 s,c,sel=sources
 for b,lo,hi in zip(s['physical_bodies'],[0x377c20,0x3148f0,0x2ef2b0,0x2ef640],[0x377c6e,0x31490b,0x2ef2c4,0x2ef648]):need((int(b['entry'],16),int(b['end_exclusive'],16))==(lo,hi),'physical extent changed')
 need(len(s['physical_bodies'])==4 and [len(b['records']) for b in s['physical_bodies']]==[1,1,1,0],'root/declared leaf identity changed')
 vfile=W/'validate-title-source-annotations.py';need(sha(vfile)=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed validator changed')
 spec=importlib.util.spec_from_file_location('reviewed_roles',vfile);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 annotations=[v.validate(x) for x in sources];facts=derive(s,c,sel);controls=[]
 for cid,which,pc,field,value,diagnostic in [('closed-helper-call-changed',0,0x3148f4,'args','0x311cf0','helper call chain changed'),('fieldcell-offset-changed',0,0x3148fb,'mem-displacement',0x1048,'required memory effect/address changed'),('image-base-changed',0,0x2ef640,'mem-rip_target','0x2164480','required memory effect/address changed'),('committed-action-offset-changed',1,0x313915,'mem-displacement',0x718,'required memory effect/address changed'),('early-return-branch-changed',1,0x31391c,'args','0x31391e','required instruction/transfer changed')]:
  z=copy.deepcopy(sources);i=index(z[which])[pc]
  if field.startswith('mem-'):i['memory'][0][field[4:]]=value
  else:i[field]=value
  try:derive(*z)
  except ValueError as e:need(diagnostic in str(e),'wrong control detector');controls.append(dict(id=cid,diagnostic=str(e),method='Synthetic source-record semantic control, not executed FF12 instructions'))
  else:raise ValueError('counterexample detector failed '+cid)
 result=dict(producer_complete=True,method='A exact complete original CFG/effect and guarded-path composition; no emulator/native/game execution',driver_sha256=sha(Path(__file__)),source_pins=[dict(path=n,sha256=h) for n,h in paths],annotation_prerequisites=annotations,physical_bodies=s['physical_bodies'],facts=facts,controls=controls,acceptance='Producer-valid partial boundary only; independent review/canonical consumption pending. No naturally initialized KO closure.')
 with out.open('x') as f:json.dump(result,f,indent=2)
 print('Closed read-only mode query; conditional Dismiss early returns refute unconditional cleanup guarantee. Natural UQ147 remains OPEN.')
if __name__=='__main__':main()
