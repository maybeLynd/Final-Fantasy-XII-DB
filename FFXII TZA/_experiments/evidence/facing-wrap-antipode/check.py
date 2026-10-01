import hashlib,json,struct
from fractions import Fraction
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest();r=json.loads((W/'result.json').read_text());ref=r['reference'];raw=(W/'retained/source.bin').read_bytes()
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and ref['entry']=='0x26c090' and ref['bytes']==len(raw)==129 and ref['source_sha256']==sha(raw)
assert r['driver_sha256']==sha((W/'derive.py').read_bytes()) and ref['reader_sha256']==sha((W/'retained/shipping-reader.py').read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
assert r['constants']=={'0x1cebc50':'db0f4940','0x915620':'db0f49c0','0x1cebc78':'db0fc940'}
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(raw,0x26C090));assert sum(i.size for i in ins)==129
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins]
ii={i.address:i for i in ins}
expected={0x26C096:'0f2fd8',0x26C09C:'720a',0x26C09E:'f30f1025aafba701',0x26C0A6:'eb08',0x26C0A8:'f30f102570956a00',0x26C0B4:'f30f58dc',0x26C0BE:'f30f5e05b2fba701',0x26C0C6:'f30f2cc0',0x26C0CE:'0f5bc9',0x26C0D1:'f30f590d9ffba701',0x26C0D9:'f30f5cd9',0x26C0DD:'f30f5cdc',0x26C0F9:'f30f115934'}
for pc,b in expected.items():assert ii[pc].bytes.hex()==b
assert ii[0x26C09C].operands[0].imm==0x26C0A8 and ii[0x26C0A6].operands[0].imm==0x26C0B0
for pc,a in [(0x26C09E,0x1CEBC50),(0x26C0A8,0x915620),(0x26C0BE,0x1CEBC78),(0x26C0D1,0x1CEBC78)]:assert ii[pc].operands[-1].size==4 and pc+ii[pc].size+ii[pc].operands[-1].mem.disp==a
mut=bytearray(raw);mut[0x26C0A8-0x26C090+4:0x26C0A8-0x26C090+8]=struct.pack('<i',0x1CEBC50-(0x26C0A8+8))
assert bytes(mut)==(W/'retained/changed-bias-source.bin').read_bytes() and r['detector']['code_hex']==bytes(mut).hex() and r['detector']['source_rejected']
mi=next(i for i in cs.disasm(mut,0x26C090) if i.address==0x26C0A8);assert mi.address+mi.size+mi.operands[-1].mem.disp==0x1CEBC50 and mi.bytes.hex()!=expected[mi.address]
f=lambda h:Fraction(struct.unpack('<f',bytes.fromhex(h)[::-1])[0]);P=f('40490FDB');assert f('C0490FDB')==-P and f('40C90FDB')==2*P
ops=['addss heading+bias','divss biased/2pi','cvttss2si','cvtdq2ps integer','mulss integer*2pi','subss biased-product','subss remainder-bias']
def check_calculation(c,changed=False):
 x=f(c['input_bits']);bias=P if x>=0 or changed else -P;assert f(c['bias_bits'])==bias
 t=x+bias;q=t/(2*P);n=int(q);expected=[t,q,n,Fraction(n),n*2*P,t-n*2*P,t-n*2*P-bias]
 assert [s['operation'] for s in c['stages']]==ops
 for s,v in zip(c['stages'],expected):
  if s['operation']=='cvttss2si':assert s['integer']==v
  else:assert f(s['bits'])==v and Fraction(s['exact_numerator'],s['exact_denominator'])==v and s['exactly_representable'] is True
 assert f(c['output_bits'])==expected[-1]
assert len(r['cases'])==3
for c,inp,a,b in zip(r['cases'],['40490FDB','C0490FDB','00000000'],['C0490FDB','40490FDB','00000000'],['40490FDB','C0490FDB','00000000']):
 assert c['first']['input_bits']==inp and c['first']['output_bits']==c['second']['input_bits']==a and c['second']['output_bits']==b and c['idempotent']==(a==b)
 check_calculation(c['first']);check_calculation(c['second'])
for key in ('negative_first','negative_second'):
 c=r['detector'][key];check_calculation(c,True);assert c['input_bits']==c['output_bits']=='C0490FDB'
assert 'idempotent, so harmless' in (W/'retained/contract.md').read_text() and 'wrap is idempotent' in (W/'retained/contract.md').read_text()
assert r['tools']['capstone_dll']['bytes']>0 and len(r['tools']['capstone_dll']['sha256'])==64
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_SOURCE_COUNTEREXAMPLE exact signed-pi two-cycle, zero fixed, private bias-source rejected and source-calculation detector fixed; no new original-code/native/emulator/live runs or broad sweep')
