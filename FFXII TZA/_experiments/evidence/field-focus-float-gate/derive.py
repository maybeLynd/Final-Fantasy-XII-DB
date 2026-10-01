import ast,hashlib,importlib.util,json,os,subprocess,sys,tempfile
from pathlib import Path
import capstone
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
assert team.board_status(team.BOARD)[0]
b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-FIELD-FOCUS-FLOAT-GATE');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'result.json').exists(),'Do not replay a settled source discriminator'
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(sp);sp.loader.exec_module(reader)
image,sections=reader.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
code=reader.img_rd(image,sections,0x22AB68,32)
def obligation(raw):
 ii={i.address:i for i in cs.disasm(raw,0x22AB68)}
 assert sum(i.size for i in ii.values())==32 and len(ii)==9
 for pc,hexcode in [(0x22AB68,'e833d81200'),(0x22AB6D,'85c0'),(0x22AB6F,'7417'),(0x22AB71,'f30f1005479fe301'),(0x22AB79,'0f2ec7'),(0x22AB7C,'7a12'),(0x22AB7E,'7510'),(0x22AB80,'418bcf'),(0x22AB83,'e8385c0200')]:assert ii[pc].bytes.hex()==hexcode,(hex(pc),ii[pc].mnemonic)
 assert ii[0x22AB6F].operands[0].imm==0x22AB88
 assert ii[0x22AB7C].operands[0].imm==ii[0x22AB7E].operands[0].imm==0x22AB90
 assert ii[0x22AB83].operands[0].imm==0x2507C0
 mem=ii[0x22AB71].operands[1].mem;assert ii[0x22AB71].address+ii[0x22AB71].size+mem.disp==0x2064AC0
 assert [ii[0x22AB79].reg_name(o.reg) for o in ii[0x22AB79].operands]==['xmm0','xmm7']
 return ii
ii=obligation(code);mut=bytearray(code);mut[20:22]=bytes.fromhex('9090') # actual JP atAB7C is removed, private bytes only
try:obligation(bytes(mut))
except AssertionError:rejected=True
else:raise AssertionError('Missing-parity source mutant accepted')
zero=reader.img_rd(image,sections,0x22A9EF,3);assert zero.hex()=='0f57ff'
helper=reader.img_rd(image,sections,0x3583A0,14);assert helper.hex()=='0fb705ebfbf601c1e80383e001c3'
view=Path('Database/FFXII TZA/_index/candidates/gg1-static-order/gg1_order.py');vb=view.read_bytes()
tree=ast.parse(vb);assign=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='CACHE' for x in n.targets));cache=Path(ast.literal_eval(assign.value.args[1]));cb=cache.read_bytes()
lines=cb.decode().splitlines(keepends=True);hits=[n for n,x in enumerate(lines) if x.startswith('0022AB7C ')];assert len(hits)==1
before=lines[hits[0]];assert '0022A770' in before and 'jp 0x22ab90' in before
after=before.replace('jp 0x22ab90','nop');lines[hits[0]]=after;mutcb=''.join(lines).encode();assert cb!=mutcb
controls=[]
with tempfile.TemporaryDirectory(prefix='astra-field-float-') as td:
 for name,data in [('original',cb),('parity-branch-omitted-view',mutcb)]:
  p=Path(td)/'cache.txt';p.write_bytes(data);env=os.environ.copy();env['Y1P_CACHE']=str(p)
  out=subprocess.run([sys.executable,str(view)],env=env,capture_output=True,text=True)
  assert out.returncode==0 and 'PASS O5' in out.stdout and 'FAILS 0' in out.stdout,(name,out.stdout,out.stderr)
  controls.append(dict(name=name,cache_sha256=sha(data),exit=out.returncode,stdout=out.stdout,stderr=out.stderr,scope='Actual unmodified peer Python checker on disposable derived view; not FF12 code execution'))
R=W/'retained';R.mkdir(exist_ok=False)
for n,data in [('gate.bin',code),('zero.bin',zero),('bit3-helper.bin',helper),('shipping-reader.py',rp.read_bytes()),('gg1_order.py',vb),('gg1-readme.md',view.with_name('README.md').read_bytes()),('input-contract.md',Path('Database/FFXII TZA/15-Input/CONTRACT-input-subsystem.md').read_bytes())]: (R/n).write_bytes(data)
(R/'cache-mutation.json').write_text(json.dumps(dict(original_cache_path=str(cache),original_cache_bytes=len(cb),original_cache_sha256=sha(cb),mutant_cache_sha256=sha(mutcb),before=before,after=after,limits='Full cache identity retained, only exact edited line retained; reproduction requires original matching cache. It is a derived view, not the shipping source.'),indent=2)+'\n')
domains=[dict(relation=k,zf=int(v[0]),pf=int(v[1]),cf=int(v[2]),send=v[0]=='1' and v[1]=='0',send_if_parity_guard_removed=v[0]=='1') for k,v in json.loads((W/'architecture.json').read_text())['completed_flags_zf_pf_cf'].items()]
cases=[]
for bits in (0,0x80000000,0x3F800000,0xBF800000,0x7F800000,0xFF800000,0x7FC00001,0x7F800001,1,0x80000001):
 exp=bits&0x7F800000;mant=bits&0x7FFFFF;nan=exp==0x7F800000 and mant!=0;sub=exp==0 and mant!=0;zero_bits=(bits&0x7FFFFFFF)==0
 cases.append(dict(bits=f'{bits:08X}',relation_without_daz='unordered' if nan else 'equal' if zero_bits else 'less' if bits>>31 else 'greater',admitted_daz0_completed=zero_bits,admitted_daz1_completed=zero_bits or sub,exception_or_domain_limit='SNaN needs completed comparison (invalid mask/handler not established)' if nan and not bits&0x400000 else 'DAZ/denormal exception state conditional, not observed' if sub else 'Completed comparison, xmm7 zero and prior bit3 gate passes; no normal reachability claim'))
result=dict(method='A exact shipping gate plus ISA conditional interpretation and Python checker intervention; zero FF12/emulator/native/live tests',reference=dict(exe_sha256=sha(image),image_base='0x120000',reader_sha256=sha(rp.read_bytes()),gate_entry='0x22ab68',gate_end_exclusive='0x22ab88',gate_sha256=sha(code),zero_sha256=sha(zero),helper_sha256=sha(helper)),tools=dict(python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_module_sha256=sha(Path(capstone.__file__).read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),architecture_sha256=sha((W/'architecture.json').read_bytes()),anchors=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii.values()],domains=domains,cases=cases,producer_controls=controls,source_mutation=dict(change='JP AB7C two bytes7A12 replaced with9090 in private bytes',source_obligation_rejected=rejected),result='NaN-admission hypothesis refuted by explicit JP then JNE: send requires completed comparison PF0/ZF1. Existing O5 conclusion is supported but checker omits both branch obligations. Exact-zero-bit reading also needs DAZ/domain qualification; DAZ1 admits subnormal inputs as effective zero.',limits='Conditional source/ISA, no actual FF12 MXCSR, accumulator occurrence, native exception behavior, normal dispatch timing, full-frame/callee execution or all51 reader ordering. xmm7 zero at comparison is the stated boundary; zeroing instruction retained, no whole-frame initialization/callee-preservation proof newly made.',cleanup='Disposable cache copies removed, shipping image/peer files read-only; no game/PC/save/config/instruments touched; published prior inputs immutable, independent review/consumer agreement pending')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('NaN hypothesis REFUTED; actual peer O5 unchanged PASS with parity removed from derived view; source obligation rejects. DAZ qualified, source-only.')
