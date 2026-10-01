import hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 assert [(b['entry'],b['size']) for b in s['bodies']]==[('0x300530',880),('0x239820',27)]
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);im={}
 for b in s['bodies']:
  r=bytes.fromhex(b['raw_hex']);assert len(r)==b['size'] and sha(r)==b['sha256']
  ii=list(cs.disasm(r,int(b['entry'],16)));assert sum(i.size for i in ii)==len(r) and ii[-1].mnemonic=='ret'
  rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]
  assert rows==b['instructions'];im.update({x['pc']:x for x in rows})
 def ins(pc,op,args):assert (im[pc]['op'],im[pc]['args'])==(op,args),(pc,im[pc])
 ins('0x239826','mov','ebx, edx');ins('0x239828','call','0x31b760')
 ins('0x23982d','test','rax, rax');ins('0x239830','je','0x239835');ins('0x239832','mov','dword ptr [rax + 0x48], ebx')
 assert all(i['op'] not in ['cmp','cmovl','cmovg','cmovge','cmovle'] for i in s['bodies'][1]['instructions'])
 # Complete producer/consumer chain: returned owning unit's floor is spilled then read by clamp.
 ins('0x30055e','call','0x31b860');ins('0x30056d','mov','ecx, dword ptr [rax + 0x48]')
 ins('0x300570','mov','dword ptr [rsp + 0xb0], ecx');ins('0x300579','mov','dword ptr [rsp + 0xb0], edi')
 ins('0x30063b','mov','edx, dword ptr [rsi + 0x48]');ins('0x30063e','add','r14d, edx')
 ins('0x300641','mov','eax, dword ptr [rsp + 0xb0]');ins('0x30064c','cmp','r14d, eax')
 ins('0x30064f','jge','0x300656');ins('0x300651','mov','r14d, eax');ins('0x300654','jmp','0x3006a7')
 ins('0x300679','mov','eax, dword ptr [rsi + 0x24]');ins('0x300684','cmp','r14d, eax');ins('0x300687','jle','0x3006a7')
 ins('0x30069a','mov','r14d, dword ptr [rsi + 0x24]');ins('0x3006a2','jae','0x3006a7')
 ins('0x300749','mov','dword ptr [rsi + 0x48], r14d')
 # After local clamp no in-body assignment to R14 before that store. Callees are excluded.
 between=[i for pc,i in im.items() if 0x3006A7<=int(pc,16)<0x300749]
 assert all(not i['args'].startswith(('r14,','r14d,','r14w,','r14b,')) for i in between)
 refs={p['path']:p for p in s['references']}
 for p in s['references']:
  b=(HERE/p['retained']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256']
 old=json.loads((HERE/'retained'/'bodies.json').read_text());main=next(x for x in old['real_bodies_executed'] if x['va']=='0x300530')
 assert main['sha256']==s['bodies'][0]['sha256']
 results=json.loads((HERE/'retained'/'result.json').read_text());controls=[]
 for name,hp in [('floor-under',20),('floor-exact',20),('floor-above',21),('cap-clamp',200),('cap-under',199)]:
  r=next(x for x in results['results'] if x['name']==name);assert r['ok'] and r['snap']['hp']==hp
  controls.append({'case':name,'retained_HP':hp,'method':'Existing EXP093 isolated original-code with disclosed deep stubs; not rerun here.'})
 contract=(HERE/'retained'/'CONTRACT-hp-write-and-lethal-transition.md').read_text()
 page=(HERE/'retained'/'the-hp-write-and-the-lethal-transition.md').read_text()
 assert 'floor <= hp <= cap' in contract and 'Nothing else is required' in contract
 assert 'HP cannot fall below the unit' in page and 'cannot rise above the cap' in page
 witnesses=[]
 for name,old,delta,floor,cap,expect in [('ordered-lower-control',50,-40,20,50,20),
  ('ordered-upper-control',50,100,20,50,50),('inconsistent-lower-path',50,0,80,50,80),
  ('inconsistent-upper-path',50,100,80,50,50)]:
  candidate=old+delta;assert -2**31<=candidate<2**31
  if candidate<floor:
   out=floor;pcs=['0x30063b','0x30063e','0x300641','0x30064c','0x30064f','0x300651','0x300654','0x3006a7']
  else:
   out=min(candidate,cap);pcs=['0x30063b','0x30063e','0x300641','0x30064c','0x30064f','0x300656','0x300659','0x30065f','0x300662','0x300665','0x30066c','0x300679','0x30067c','0x300680','0x300684','0x300687']
   if candidate>cap:pcs+=['0x300689','0x30068c','0x30069a','0x30069e','0x3006a2']
   pcs+=['0x3006a7']
  assert out==expect and all(pc in im for pc in pcs)
  witnesses.append({'case':name,'old':old,'delta':delta,'floor':floor,'cap':cap,'status_layers':0,
   'candidate':candidate,'local_clamp_result':out,'satisfies_two_sided_bound':floor<=out<=cap,
   'symbolic_original_branch_pcs':pcs,'execution_class':'A symbolic branch illustration; not an executed trace'})
 assert [x['satisfies_two_sided_bound'] for x in witnesses]==[True,True,False,False]
 return {'method':s['method'],'historical_positive_controls':controls,'symbolic_witnesses':witnesses,
  'established':['Original lower branch selects floor and jumps over cap selection/test; the other branch may select cap without rechecking floor. For statuses0 and admitted local write, floor<=cap is necessary for universal two-sided bound.',
   'Floor setter passes supplied EDX unchanged through EBX into returned unit+48 if lookup succeeds; this27B body has no cap comparison/clamp. Caller/authored restrictions and actual reachable inconsistent states are separate.',
   'The contract and mechanism universally state both HP bounds. Neither that text nor numeric clamping provides a proof that floor and effective cap are ordered at every store.'],
  'formula':'candidate = signed32(delta + old); local result = (candidate < floor) ? floor : min(candidate, effectiveCap), with signed comparisons. Symbolic witnesses deliberately avoid wrap and use statuses0 so effectiveCap=maxHP.',
  'semantic_implication':'Qualify the invariant and postconditions by ordered bounds and by the particular store/callee scope. Preserve original branch order; do not add a second floor/cap clamp to repair the original behavior.',
  'limits':s['limits']+' No ordinary bug/crash, KO/revive/death event, final post-recompute HP or exhaustive wrap/status domain conclusion. Existing EXP093 positive cases remain valid; this is a new boundary outside their listed coverage.',
  'affected_claims':['OPUS CONTRACT-hp-write-and-lethal-transition.md §4 universal floor<=HP<=cap, preconditions and corrected second-store-bound gloss',
   'FABLE Current-HP/the-hp-write-and-the-lethal-transition.md player summary HP cannot violate bounds, and only-bottom-value gloss'],
  'cleanup':'Read-only shipping image/artifacts; no game/PC/native/input/save/config/reference writes or fresh live cleanup receipt.',
  'propagation':'PENDING owner qualification and independent review. Existing experiments and mutations unchanged.'}

if __name__=='__main__':
 s=json.loads((HERE/'source.json').read_text());out=derive(s)
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_STATIC_ONLY','historical_artifact_controls':5,
  'symbolic_witnesses':4,'new_original_code_or_live_cases':0,'limits':'Exact instructions prove branch structure; symbolic outputs are not fresh execution. No downstream or ordinary runtime occurrence accepted.'},indent=2)+'\n')
 print('PASS static HP bound precondition; historical controls retained, no runtime promotion.')
