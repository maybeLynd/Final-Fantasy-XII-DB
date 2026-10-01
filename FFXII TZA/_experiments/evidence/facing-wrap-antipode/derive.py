import datetime,hashlib,importlib.util,json,struct,sys
from fractions import Fraction
from pathlib import Path
import capstone
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
ok,detail=team.board_status(team.BOARD);assert ok,detail;b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-FACING-WRAP-ANTIPODE');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not (W/'result.json').exists(),'Retained result immutable'
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
spec=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader);image,ss=reader.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
raw=reader.img_rd(image,ss,0x26C090,129);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(raw,0x26C090));assert sum(i.size for i in ins)==129
constants={hex(p):reader.img_rd(image,ss,p,4).hex() for p in (0x1CEBC50,0x915620,0x1CEBC78)}
assert constants=={'0x1cebc50':'db0f4940','0x915620':'db0f49c0','0x1cebc78':'db0fc940'}
def binding(code):
 ii={i.address:i for i in cs.disasm(code,0x26C090)}
 expected={0x26C096:'0f2fd8',0x26C09C:'720a',0x26C09E:'f30f1025aafba701',0x26C0A6:'eb08',0x26C0A8:'f30f102570956a00',0x26C0B4:'f30f58dc',0x26C0BE:'f30f5e05b2fba701',0x26C0C6:'f30f2cc0',0x26C0CE:'0f5bc9',0x26C0D1:'f30f590d9ffba701',0x26C0D9:'f30f5cd9',0x26C0DD:'f30f5cdc',0x26C0F9:'f30f115934'}
 for p,v in expected.items():assert ii[p].bytes.hex()==v,(hex(p),'original source binding')
 assert ii[0x26C09C].operands[0].imm==0x26C0A8 and ii[0x26C0A6].operands[0].imm==0x26C0B0
 for p,a in [(0x26C09E,0x1CEBC50),(0x26C0A8,0x915620),(0x26C0BE,0x1CEBC78),(0x26C0D1,0x1CEBC78)]:
  i=ii[p];assert i.operands[-1].size==4 and i.address+i.size+i.operands[-1].mem.disp==a
binding(raw)
mut=bytearray(raw);off=0x26C0A8-0x26C090;mut[off+4:off+8]=struct.pack('<i',0x1CEBC50-(0x26C0A8+8));rejection=None
try:binding(bytes(mut))
except AssertionError as e:rejection=str(e)
assert rejection
f=lambda bits:struct.unpack('<f',struct.pack('<I',bits))[0]
bits=lambda v:struct.unpack('<I',struct.pack('<f',v))[0]
f32=lambda v:f(bits(v))
def calc(xbits,changed=False):
 x=f(xbits);bias=f(0x40490FDB if x>=0 or changed else 0xC0490FDB)
 stages=[]
 def step(name,v,exact):
  rounded=f32(v);fv=Fraction(rounded);stages.append(dict(operation=name,bits=f'{bits(rounded):08X}',exact_numerator=exact.numerator,exact_denominator=exact.denominator,exactly_representable=(fv==exact)));return rounded
 t=step('addss heading+bias',x+bias,Fraction(x)+Fraction(bias))
 q=step('divss biased/2pi',t/f(0x40C90FDB),Fraction(t)/Fraction(f(0x40C90FDB)))
 n=int(q);stages.append(dict(operation='cvttss2si',integer=n))
 nf=step('cvtdq2ps integer',n,Fraction(n))
 prod=step('mulss integer*2pi',nf*f(0x40C90FDB),Fraction(nf)*Fraction(f(0x40C90FDB)))
 rem=step('subss biased-product',t-prod,Fraction(t)-Fraction(prod))
 out=step('subss remainder-bias',rem-bias,Fraction(rem)-Fraction(bias))
 assert all(s.get('exactly_representable',True) for s in stages)
 return dict(input_bits=f'{xbits:08X}',bias_bits=f'{bits(bias):08X}',stages=stages,output_bits=f'{bits(out):08X}',scope='Source/host exact arithmetic under stated nearest masked environment, NOT original execution')
cases=[]
for name,x in [('positive-antipode',0x40490FDB),('negative-antipode',0xC0490FDB),('positive-zero-control',0)]:
 a=calc(x);z=calc(int(a['output_bits'],16));cases.append(dict(name=name,first=a,second=z,idempotent=(a['output_bits']==z['output_bits'])))
assert [c['idempotent'] for c in cases]==[False,False,True]
assert [(c['first']['output_bits'],c['second']['output_bits']) for c in cases]==[('C0490FDB','40490FDB'),('40490FDB','C0490FDB'),('00000000','00000000')]
detector=dict(intervention='Private source negative bias RIP target replaced by positive-pi target; host calculation only',code_hex=bytes(mut).hex(),source_rejected=rejection,negative_first=calc(0xC0490FDB,True),negative_second=calc(0xC0490FDB,True));assert detector['negative_first']['output_bits']==detector['negative_second']['output_bits']=='C0490FDB'
R=W/'retained';R.mkdir(exist_ok=False);(R/'source.bin').write_bytes(raw);(R/'changed-bias-source.bin').write_bytes(mut);(R/'shipping-reader.py').write_bytes(rp.read_bytes())
for name,p in [('contract.md','Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-facing-and-steering.md'),('question-ledger.md','Database/FFXII TZA/_index/OPEN-QUESTIONS.md'),('differential.py','Reconstruction/Tests/Differential/diff_angle_wrap.py')]:
 path=Path(p);assert path.exists(),p;(R/name).write_bytes(path.read_bytes())
dll=Path(capstone._cs._name);tools=dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll=dict(path=str(dll),bytes=dll.stat().st_size,sha256=sha(dll.read_bytes())))
result=dict(method='A shipping source+exact selected arithmetic; zero FF12/original-code/native/emulator/live tests',reference=dict(exe_sha256=sha(image),entry='0x26c090',bytes=len(raw),source_sha256=sha(raw),reader_sha256=sha(rp.read_bytes())),constants=constants,instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins],cases=cases,detector=detector,tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),limits='Selected endpoints/+zero only; exact arithmetic assumptions stated, not general input/MXCSR/native exceptions/normalcaller/presentation/turn consequence proof. Source calculation not new execution or new DY1 sweep. Current consumer inputs retained unchanged, independent acceptance pending.',cleanup='Read-only reference/peer consumers; no game/process/control/save/config writes')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('DERIVED source endpointtwo-cycle vs zero fixed control; changednegativebias detector narrows idempotence, no original/native/live execution.',flush=True)
