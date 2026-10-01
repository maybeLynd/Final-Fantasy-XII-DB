import datetime,hashlib,importlib.util,json,struct,sys
from fractions import Fraction
from pathlib import Path
import capstone
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
ok,detail=team.board_status(team.BOARD);assert ok,detail;b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-WIDGET-TIMED-DURATION-SELECTION');assert t['status']=='ACTIVE' and t['agent']=='ASTRA';assert not (W/'result.json').exists()
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(sp);sp.loader.exec_module(reader);image,ss=reader.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ENTRY,END=0x244E9C,0x244EDF;code=reader.img_rd(image,ss,ENTRY,END-ENTRY);assert len(code)==67
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,ENTRY));assert sum(i.size for i in ins)==67
def bind(raw):
 ii={i.address:i for i in cs.disasm(raw,ENTRY)}
 expected={0x244E9C:'0fb77902',0x244EA0:'e8ebcdf3ff',0x244EA5:'33c9',0x244EA7:'83f801',0x244EAA:'8b437c',0x244EAD:'0f44f9',0x244EB0:'0fbae00b',0x244EB4:'730c',0x244EB6:'8bf8',0x244EB8:'0fbaf70b',0x244EBC:'897b7c',0x244EBF:'c1ef16',0x244EC2:'6bcf3c',0x244EC5:'b8d34d6210',0x244ECF:'f7e1',0x244ED1:'c1ea06',0x244ED4:'895370',0x244ED7:'83637cf4',0x244EDB:'834b7c04'}
 for p,v in expected.items():assert ii[p].bytes.hex()==v,(hex(p),'selected original source binding')
 assert ii[0x244EB4].operands[0].imm==0x244EC2 and ii[0x244EA0].operands[0].imm==0x181C90 and ii[0x244E9C].operands[-1].size==2
bind(code)
mut=bytearray(code);mut[0x244EBF-ENTRY+2]=0x15;rejected=None
try:bind(bytes(mut))
except AssertionError as e:rejected=str(e)
assert rejected
C=0x10624DD3;SHIFT=38;maximum=65535*60;error=Fraction(maximum*(C*1000-(1<<SHIFT)),1000*(1<<SHIFT));assert C*1000-(1<<SHIFT)==56 and 0<=error<Fraction(1,50)
def calc(name,record,returned,flags,shift=22):
 assert 0<=record<=65535 and 0<=flags<=0xFFFFFFFF
 selected=0 if returned==1 else record;cleared=flags
 if flags&0x800:cleared=flags&~0x800;selected=cleared>>shift
 product=selected*60;frames=(product*C)>>SHIFT
 return dict(name=name,record_ms=record,callee_return=returned,flags_before=f'{flags:08X}',selected_ms=selected,override=bool(flags&0x800),flags_after_override=f'{cleared:08X}',flags_after_local_state=f'{((cleared&0xFFFFFFF4)|4):08X}',product=product,frames=frames,ordinary_division=product//1000,scope='Static source calculation, not original/native/emulator/live call')
cases=[calc('ordinary-record-control',1000,0,0),calc('below-one-frame',16,0,0),calc('first-one-frame',17,0,0),calc('max-u16-record',65535,0,0),calc('return-one-record-zero',1000,1,0),calc('return-one-override-wins',1000,1,(17<<22)|0x800),calc('return-one-highbits-no-flag-control',1000,1,17<<22),calc('max-high10-override',65535,0,0xFFFFFFFF),calc('zero-payload-override-consumed',1000,0,0x800)]
assert [c['frames'] for c in cases]==[60,0,1,3932,0,1,0,61,0] and all(c['frames']==c['ordinary_division'] for c in cases)
detector=calc('labelled-shift21-source-model-detector',65535,0,0xFFFFFFFF,21);assert detector['selected_ms']==2047 and detector['frames']==122
R=W/'retained';R.mkdir(exist_ok=False);(R/'source.bin').write_bytes(code);(R/'changed-shift-source.bin').write_bytes(mut);(R/'getter-context.bin').write_bytes(reader.img_rd(image,ss,0x181C90,20));(R/'shipping-reader.py').write_bytes(rp.read_bytes())
fp=Path('Database/FFXII TZA/_types/fields.tsv');fields=fp.read_bytes();rows=[line for line in fields.decode().splitlines() if line.split('\t')[:2] in [['Widget','0x070'],['Widget','0x07C']]];assert len(rows)==2
(R/'field-preimages.json').write_text(json.dumps(dict(source_path=fp.as_posix(),source_sha256=sha(fields),rows=rows),indent=2)+'\n')
for name,p in [('contract.md','Database/FFXII TZA/16-UI/Widget-Object-Model/CONTRACT-widget-object.md'),('producer.py','Database/FFXII TZA/_index/candidates/mapscreen-child-widget/child_widget.py')]: (R/name).write_bytes(Path(p).read_bytes())
dll=Path(capstone._cs._name);tools=dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll=dict(path=str(dll),bytes=dll.stat().st_size,sha256=sha(dll.read_bytes())))
result=dict(method='A original67B selection/conversion source+bounded rational domain proof, zero original/native/emulator/live runs',reference=dict(exe_sha256=sha(image),entry=hex(ENTRY),end_exclusive=hex(END),body_sha256=sha(code),reader_sha256=sha(rp.read_bytes())),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins],cases=cases,domain_proof=dict(max_record_ms=65535,max_override_ms=1023,max_product=maximum,magic=C,shift=SHIFT,magic_excess_times1000=56,max_error_numerator=error.numerator,max_error_denominator=error.denominator,minimum_nonzero_remainder_gap='20/1000 = 1/50 because product is a multiple of60',scope='ceil reciprocal cannot decrease quotient and maxpositiveerror<gap; exact floor for selected bounded product, no allu32 claim'),detector=dict(source_changed='Private SHR EDI22->21; source/host calculations only',raw_hex=bytes(mut).hex(),original_binding_rejected=rejected,calculation=detector),tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),limits='Completed181C90 return/ABIpreserved EDI/stable record+widget assumed. Gettercontext calls1EBA40 thenreads+280: not executed, no actual mode meaning/state/binding. Start-arm selected delay only, not fieldwide range (otherwriters reset/subtract), wholewidget/caller/scheduling/cadence/presentation/flag lifetime guarantee.',cleanup='Read-only image/peer consumer preimages and disposable host calculations; PC/game/save/config untouched')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('Derived UI record/packed override selection and rational bounded /1000 proof; failed overflow hypothesis not executed; independentcheck required.',flush=True)
