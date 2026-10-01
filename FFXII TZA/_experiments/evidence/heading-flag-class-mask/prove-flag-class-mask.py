"""Selected original bit-store invariant; retained-source Method A only.

No instruction/native/game execution. Catalogue-only snippet limits remain.
This derives bit positions from verified original immediates, not a live alias.
"""
import hashlib,importlib.util,itertools,json,pathlib,sys
import capstone
from capstone.x86_const import X86_OP_MEM
W=pathlib.Path(__file__).resolve().parent
REL='Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
ROOT=next((p for p in W.parents if (p/REL).is_file()),None)
ASH='5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if len(sys.argv)!=3:raise ValueError('retained_source_directory fresh_result')
 src,out=map(pathlib.Path,sys.argv[1:])
 if out.exists():raise ValueError('immutable result exists')
 if ROOT is None or sha(ROOT/REL)!=ASH:raise ValueError('reviewed role adapter unavailable/changed')
 s=importlib.util.spec_from_file_location('reviewed_roles',ROOT/REL);roles=importlib.util.module_from_spec(s);s.loader.exec_module(roles)
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 controls=[]
 for h,want in [('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:
  i=next(cs.disasm(bytes.fromhex(h),0x1000));mem=[roles.op_kind(i,o,k) for k,o in enumerate(i.operands) if o.type==X86_OP_MEM]
  if mem!=[want]:raise ValueError('actual role control failed')
  controls.append(dict(bytes=h,role=want))
 identity=json.loads((src/'identity.json').read_text())
 if identity['exe']['sha256']!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong retained binary')
 status=json.loads((src/'checks-effects-terminal.json').read_text())
 positives=[r for r in status if r.get('case')=='positive']
 if len(positives)!=1 or positives[0].get('returncode')!=0 or positives[0].get('terminal') is not True or positives[0].get('checker_sha256')!=sha(src/'check-effects.py'):
  raise ValueError('retained producer prerequisite failed/missing')
 if json.loads(positives[0]['stdout']).get('status')!='STATIC_EFFECT_BOUNDARIES_VALID_NOT_CLASS_CLOSURE':raise ValueError('retained scope/positive incomplete')
 raw=json.loads((src/'raw-object-state.json').read_text());pos=json.loads((src/'raw-position-effects.json').read_text())
 def verify(f):
  p=src/f['code_file'];b=p.read_bytes()
  if sha(p)!=f['code_sha256'] or len(b)!=f['bytes'] or f['decoded_bytes']!=len(b):raise ValueError('source/code bytes incomplete')
  ins=list(cs.disasm(b,int(f['entry'],16)))
  if len(ins)!=len(f['instructions']) or sum(i.size for i in ins)!=len(b):raise ValueError('zero/incomplete retained decode')
  for i,r in zip(ins,f['instructions']):
   if (hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)!=(r['pc'],r['bytes'],r['mnemonic'],r['args']):raise ValueError('retained bytes/annotation mismatch')
   memory=[dict(kind=roles.op_kind(i,o,k),bytes=o.size) for k,o in enumerate(i.operands) if o.type==X86_OP_MEM]
   if memory!=r['memory'] or sorted(roles.written(i))!=r['written']:raise ValueError('actual retained memory-role mismatch')
  return ins
 gate=next((f for f in pos['callees'] if f['entry']=='0x2e6000'),None)
 if gate is None:raise ValueError('missing class gate input')
 g=verify(gate);gi={i.address:i for i in g}
 if gate['code_sha256']!='5a7d9409df564f82d637984ba721f80788cca1a808684e11f7330e334dacce5b' or [(gi[pc].mnemonic,gi[pc].op_str) for pc in [0x2e6022,0x2e6026,0x2e6028]]!=[('movzx','eax, byte ptr [rcx + 3]'),('and','al, 0xe0'),('cmp','al, 0x60')]:raise ValueError('original actor byte3/E0 gate changed')
 expected={0x3e33e0:dict(sha='5a40dce04a9c9be0283cf0ae5393b65c0b65e7439c5e7a2d9b850354f29a8d1e',shift=23,mask=0x800000,dirty=2),
           0x3e3440:dict(sha='dd71e7695c2f0b548c79bca647681c0beb33149b99718f3ef4820368f4fd5c62',shift=24,mask=0x1000000,dirty=4)}
 results=[]
 for address,c in expected.items():
  f=next((f for f in raw['callees'] if f['entry']==hex(address)),None)
  if f is None:raise ValueError('missing selected flag snippet')
  ins=verify(f)
  if f['extent_status']!='UNPROVED_CATALOGUE_ONLY' or f['fragments'] or f['unwind_union'] is not None:raise ValueError('retained extent qualification changed')
  start=1 if address==0x3e33e0 else 0;reg='eax' if start else 'edx'
  if start and (ins[0].mnemonic,ins[0].op_str)!=('movzx','eax, dx'):raise ValueError('original input width changed')
  op=[(i.mnemonic,i.op_str) for i in ins[start:]]
  if op!=[('shl',reg+', '+hex(c['shift'])),('xor',reg+', dword ptr [rcx]'),('and',reg+', '+hex(c['mask'])),('xor',reg+', dword ptr [rcx]'),('or',reg+', '+str(c['dirty'])),('mov','dword ptr [rcx], '+reg),('ret','')]:raise ValueError('original shift/mask/store sequence changed')
  if f['code_sha256']!=c['sha']:raise ValueError('shipping snippet identity changed')
  # Bitwise-only operations have independent output bits. Arbitrary shifted
  # input bit is a superset of all legal MOVZX/SHL values, sufficient for this
  # preservation invariant, not an exact floating/arithmetic execution model.
  touched=set();cases=0
  for bit in range(32):
   for v,d0,d1 in itertools.product([0,1],repeat=3):
    o=(((v^d0)&((c['mask']>>bit)&1))^d1)|((c['dirty']>>bit)&1)
    cases+=1
    if o!=d1:touched.add(bit)
  if cases!=256 or touched!={k for k in range(32) if ((c['mask']|c['dirty'])>>k)&1}:raise ValueError('bit invariant incomplete')
  placements=[]
  # F<=A+3<F+4 iff F=A+q, q0..3, for nonwrapping byte addresses.
  for q in range(4):
   cm=0xe0<<(8*(3-q));changed=(c['mask']|c['dirty'])&cm
   placements.append(dict(flag_minus_actor=q,class_mask_in_flag_word=hex(cm),potential_changed_class_bits=hex(changed),preserves_second_read_class_bits=(changed==0)))
  results.append(dict(entry=hex(address),original_extent_status=f['extent_status'],input_shift=c['shift'],update_mask=hex(c['mask']),dirty_mask=hex(c['dirty']),may_change_bits=sorted(touched),boolean_cases=cases,placements=placements))
 if [q['flag_minus_actor'] for q in results[0]['placements'] if not q['preserves_second_read_class_bits']]!=[1] or not all(q['preserves_second_read_class_bits'] for q in results[1]['placements']):raise ValueError('unexpected class geometry')
 pins=[dict(path=n,sha256=sha(src/n)) for n in ['raw-object-state.json','raw-position-effects.json','identity.json','checks-effects-terminal.json','check-effects.py','retained/object-state/003E33E0.bin','retained/object-state/003E3440.bin','retained/position-effects/002E6000.bin']]
 result=dict(status='PRODUCER_PROVED_CONDITIONAL_FLAG_CLASS_BIT_INVARIANT_INDEPENDENT_PENDING',producer_complete=True,
  method='A retained shipping bytes, per-bit Boolean invariant and nonwrapping address geometry; no execution',
  checker_sha256=sha(pathlib.Path(__file__)),exe_sha256=identity['exe']['sha256'],input_pins=pins,adapter_sha256=ASH,actual_role_controls=controls,
  question='Which flag-word overlaps can change actor byte3 highE0 class bits?',snippets=results,
  counterexample=dict(method='Algebraic original-source consequence, not native or observed alias',entry='0x3e33e0',flag_minus_actor=1,input_dx=1,first_read=0,second_read=0,computed_store='0x800002',actor_class_byte_before=0,actor_class_byte_after=128),
  established=['3E3440 computed store preserves actor byte3 highE0 bits from its second DWORD read at all four possible covering placements, without an alignment premise. Bits24/2 cannot meet class-byte high5..7 bits.',
   '3E33E0 computed store may change those class bits only at exact F=actor+1, through updatebit23->actorbyte3 bit7. All other covering placements preserve them from second read. Disjointness is sufficient but stronger than this exact mask condition.',
   'If flag and actor bases are both4-aligned, exact F=actor+1 is excluded. This is a conditional geometric consequence, not proof of actual alignment/nonaliasing or initialized allocator state.',
   'The two original DWORD reads remain independent d0/d1. Bits outside mask|dirty copy d1 even if d0 differs. Comparing with an earlier actor class or memory just before store requires separate no-interference/synchronization premises.'],
  limitations=['Original21B/19B catalogue-only snippets retain their scope labels; no fabricated full-function unwind/caller coverage','Computed store invariant is not actual memory preservation across intervening writers, native initialization, natural alias or lifetime','Other render/native callbacks, other stores and full CON-172 class-stability remain OPEN','512 Boolean cases exhaust bit-local triples for two snippets; not512 game samples/native experiments and not an exact model of omitted operations'],
  affected_claims=['FABLE/OPUS CON-172 selected rendering flag-store overlap preconditions'],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
  cleanup='Canonical selected inputs read/copies only; shared adapter invoked; own bounded Python terminal, no game/PC/native/instrument/save/config/reference/peer mutation')
 out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED exact flag/class mask geometry; initialized alignment and full class stability OPEN')
if __name__=='__main__':main()
