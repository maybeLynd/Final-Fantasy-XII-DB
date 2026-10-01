import datetime,hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
ok,detail=team.board_status(team.BOARD);assert ok,detail;b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-WIDGET-TRANSITION-DURATION-DOMAIN');assert t['status']=='ACTIVE' and t['agent']=='ASTRA';assert not (W/'result.json').exists()
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(sp);sp.loader.exec_module(reader);image,ss=reader.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ENTRY,END=0x2468A0,0x246A0C;code=reader.img_rd(image,ss,ENTRY,END-ENTRY);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,ENTRY));assert len(code)==364 and sum(i.size for i in ins)==364
def bind(raw):
 ii={i.address:i for i in cs.disasm(raw,ENTRY)}
 expected={0x2468A0:'4053',0x2468A2:'4883ec40',0x2468C9:'4885c9',0x2468CC:'7456',0x2468CE:'f681800000000e',0x2468D5:'754d',0x2468E0:'7557',0x2468EC:'754b',0x246971:'6b4c24703c',0x246995:'b8d34d6210',0x24699A:'f7e9',0x2469A6:'c1fa06',0x2469A9:'8bc2',0x2469AB:'c1e81f',0x2469AE:'03d0',0x2469B0:'899390000000'}
 for p,v in expected.items():assert ii[p].bytes.hex()==v,(hex(p),'original transition source')
 assert ii[0x246971].operands[1].size==4 and ii[0x246971].operands[1].mem.disp==0x70
 assert ii[0x2468E0].operands[0].imm==ii[0x2468EC].operands[0].imm==0x246939
bind(code)
mut=bytearray(code);mut[0x24699A-ENTRY+1]=0xE1;rejected=None
try:bind(bytes(mut))
except AssertionError as e:rejected=str(e)
assert rejected
signed=lambda x:x-(1<<32) if x&(1<<31) else x
def calc(name,msbits,unsigned=False):
 low=(msbits*60)&0xFFFFFFFF;s=signed(low);full=((low if unsigned else s)*0x10624DD3)&0xFFFFFFFFFFFFFFFF;high=(full>>32)&0xFFFFFFFF
 shifted=(signed(high)>>6)&0xFFFFFFFF;sign=shifted>>31;answer=(shifted+sign)&0xFFFFFFFF
 trunc=(abs(s)//1000)*(-1 if s<0 else 1)
 return dict(name=name,input_dword_bits=f'{msbits:08X}',input_signed=signed(msbits),low32_product_bits=f'{low:08X}',product_signed=s,full_product_bits=f'{full:016X}',high32_product_bits=f'{high:08X}',shifted_bits=f'{shifted:08X}',sign_adjustment=sign,stored_bits=f'{answer:08X}',stored_signed=signed(answer),signed_division_trunc0=trunc,scope='Original-source/host integer calculation, not original/native/emulator/live execution')
cases=[calc('ordinary1000-control',1000),calc('positive17-control',17),calc('negative17-truncation',(-17)&0xFFFFFFFF),calc('last-positive-no-product-overflow',35791394),calc('first-positive-product-sign-overflow',35791395)]
assert [c['stored_signed'] for c in cases]==[60,1,-1,2147483,-2147483] and all(c['stored_signed']==c['signed_division_trunc0'] for c in cases)
detector=calc('labelled-signed-to-unsigned-multiply-model',(-17)&0xFFFFFFFF,True);assert detector['stored_bits']!=cases[2]['stored_bits']
# General mathematical projection is separate from bounded source calculations.
predictions=dict(negative17_floor=-2,positive_overflow_unbounded_trunc0=(35791395*60)//1000)
R=W/'retained';R.mkdir(exist_ok=False);(R/'source.bin').write_bytes(code);(R/'changed-multiply-source.bin').write_bytes(mut);(R/'shipping-reader.py').write_bytes(rp.read_bytes())
fields=Path('Database/FFXII TZA/_types/fields.tsv').read_bytes();rows=[line for line in fields.decode().splitlines() if line.split('\t')[:2] in [['Widget','0x070'],['Widget','0x090']]];assert len(rows)==2
(R/'field-preimages.json').write_text(json.dumps(dict(source_path='Database/FFXII TZA/_types/fields.tsv',source_sha256=sha(fields),rows=rows),indent=2)+'\n')
for name,p in [('contract.md','Database/FFXII TZA/16-UI/Widget-Object-Model/CONTRACT-widget-object.md'),('peer-producer.py','Database/FFXII TZA/_index/candidates/mapscreen-child-widget/child_widget.py')]: (R/name).write_bytes(Path(p).read_bytes())
P=Path('Database/FFXII TZA/_experiments/evidence/widget-timed-duration-selection');m=json.loads((P/'manifest.json').read_text());assert m['members']
for x in m['members']:
 data=(P/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
(R/'prior37-manifest.json').write_bytes((P/'manifest.json').read_bytes());(R/'prior37-source.bin').write_bytes((P/'retained/source.bin').read_bytes())
dll=Path(capstone._cs._name);tools=dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll=dict(path=str(dll),bytes=dll.stat().st_size,sha256=sha(dll.read_bytes())))
result=dict(method='A complete starter364B and exact selected signed integer calculations; zero original/native/emulator/live tests',reference=dict(exe_sha256=sha(image),entry=hex(ENTRY),end_exclusive=hex(END),body_sha256=sha(code),reader_sha256=sha(rp.read_bytes()),prior37_manifest_sha256=sha((P/'manifest.json').read_bytes())),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins],cases=cases,host_predictions=predictions,detector=dict(source_change='Private signedIMUL->unsignedMUL at24699A, same subsequent SAR/sign correction in source model; not original execution',raw_hex=bytes(mut).hex(),original_binding_rejected=rejected,calculation=detector),input_path=dict(entry_rsp_to_local_rsp_delta=-0x48,local_duration_offset=0x70,entry_duration_offset=0x28,argument_width=4,selected_branch='widget nonnull, flags+80 bits1..3 clear, requestedpair differscurrent signed16-expanded pair',limits='Source selectedpath has no duration clamp before246971; fullcallee/caller domain and otherstartervariants not certified'),tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),limits='Source selectedpath/cases only, no actual negative/large caller or fullUI transition/nativeCPU/live/presentation. Otherstartervariants need their own reads. +70 boundedunsigned37 unchanged. uint32 storage width does not imply unsigned division; input ABI word interpreted bitwise, original Cdeclaredsignedness not inferred.',cleanup='Read-only image/currentpeerpreimages and host calculations only, PC/game/save/config untouched')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('Derived signed low32-product transition domain versus37boundedunsigned; negative17/firstpositiveoverflow/control, source predicate rejects unsignedMUL; no native/original/live runs.',flush=True)
