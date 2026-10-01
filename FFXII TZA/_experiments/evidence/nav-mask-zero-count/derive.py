import builtins,contextlib,hashlib,importlib.util,io,json,struct,subprocess,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest();ROOT=Path.cwd().resolve()
REF=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';CHECK=ROOT/'Database/FFXII TZA/_index/candidates/nav-conversion-consumers/conv_check.py';PAGE=ROOT/'Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-corridor-query-family.md'
BASE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def section_offset(img,va):
 pe=struct.unpack_from('<I',img,60)[0];n=struct.unpack_from('<H',img,pe+6)[0];sz=struct.unpack_from('<H',img,pe+20)[0]
 for vs,rva,rs,ro in [struct.unpack_from('<IIII',img,pe+24+sz+40*j+8) for j in range(n)]:
  if 0x120000+rva<=va<0x120000+rva+rs:return va-0x120000-rva+ro
 raise AssertionError(hex(va))
def child(case):
 raw=REF.read_bytes();assert sha(raw)==BASE;original=raw;off=section_offset(raw,0x391320);assert raw[off:off+2].hex()=='eb09'
 if case=='negative-path-jump-removed':x=bytearray(raw);x[off:off+2]=b'\x90\x90';raw=bytes(x)
 else:assert case=='canonical-baseline'
 checker=(W/'retained/conv_check.py').read_bytes();page=(W/'retained/contract.md').read_bytes();realopen=builtins.open;reads=[]
 def supplied(file,mode='r',*args,**kwargs):
  p=Path(file).resolve()
  if p==REF:assert mode=='rb';reads.append(dict(path=str(p),supplied='disposable image bytes'));return io.BytesIO(raw)
  if p==PAGE:assert mode=='r';reads.append(dict(path=str(p),supplied='retained canonical contract'));return io.StringIO(page.decode())
  raise AssertionError('Unexpected checker read '+str(p))
 out=io.StringIO();rc=None
 with contextlib.redirect_stdout(out):
  builtins.open=supplied
  try:exec(compile(checker,str(CHECK),'exec'),dict(__file__=str(CHECK),__name__='__main__'))
  except SystemExit as e:rc=e.code
  finally:builtins.open=realopen
 assert rc is not None and len(reads)==2
 print(json.dumps(dict(case=case,method='Actual unchanged Python checker, controlled file-read intervention; no original FF12 execution',input_sha256=sha(raw),baseline_sha256=sha(original),checker_sha256=sha(checker),page_sha256=sha(page),patch=None if case=='canonical-baseline' else dict(va='0x391320',file_offset=off,before='eb09',after='9090'),checker_exit=rc,stdout=out.getvalue(),reads=reads,cleanup='open restored, private bytes only, child exits')))
if '--child' in sys.argv:child(sys.argv[-1]);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,detail=team.board_status(team.BOARD);assert ok,detail;b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-NAV-MASK-ZERO-COUNT');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'result.json').exists(),'Do not replay a settled discriminator'
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(sp);sp.loader.exec_module(reader)
img,ss=reader.load_image();assert sha(img)==BASE and sha(REF.read_bytes())==BASE
pe=struct.unpack_from('<I',img,60)[0];rv,n=struct.unpack_from('<II',img,pe+24+112+3*8);pd=reader.img_rd(img,ss,0x120000+rv,n)
row=next((a+0x120000,z+0x120000,u+0x120000) for a,z,u in struct.iter_unpack('<III',pd) if a+0x120000==0x3912E0);assert row[1]-row[0]==292
code=reader.img_rd(img,ss,row[0],292);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def obligations(raw):
 ii={i.address:i for i in cs.disasm(raw,0x3912E0)};assert sum(i.size for i in ii.values())==292
 for pc,hexcode in [(0x39131A,'85f6'),(0x39131C,'7904'),(0x39131E,'33f6'),(0x391320,'eb09'),(0x391322,'418d43ff'),(0x391328,'0f4ff0'),(0x391338,'eb08'),(0x391348,'eb09'),(0x391359,'eb08'),(0x391391,'4963c8'),(0x391394,'803c0100')]:assert ii[pc].bytes.hex()==hexcode,(hex(pc),ii[pc].mnemonic)
 for pc,dest in [(0x391320,0x39132B),(0x391338,0x391342),(0x391348,0x391353),(0x391359,0x391363)]:assert ii[pc].operands[0].imm==dest
 assert ii[0x391363].mnemonic=='cmp' and ii[0x391365].mnemonic=='jg' and ii[0x391374].mnemonic=='cmp' and ii[0x391376].mnemonic=='jg'
 return ii
ii=obligations(code);mut=bytearray(code);mut[0x40:0x42]=b'\x90\x90'
try:obligations(bytes(mut))
except AssertionError:rejected=True
else:raise AssertionError('Source obligation did not reject missing negative-path bypass')
R=W/'retained';R.mkdir(exist_ok=False);head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for n,p in [('conv_check.py',CHECK),('consumer-README.md',CHECK.with_name('README.md')),('contract.md',PAGE)]:
 rel=p.relative_to(ROOT).as_posix();data=subprocess.check_output(['git','show',head+':'+rel]);(R/n).write_bytes(data)
for n,data in [('body.bin',code),('shipping-reader.py',rp.read_bytes())]:(R/n).write_bytes(data)
controls=[]
for case in ('canonical-baseline','negative-path-jump-removed'):
 p=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',case],capture_output=True,text=True,timeout=30);assert p.returncode==0 and not p.stderr,(case,p.stdout,p.stderr)
 c=json.loads(p.stdout);controls.append(c);assert c['checker_exit']==0 and 'PASS  X3' in c['stdout'] and 'FAILS 0' in c['stdout'],c
def clamp(i,c):return 0 if i<0 else min(i,c-1)
cases=[dict(input=i,count=c,original_conditional=clamp(i,c),naive_min_max=min(max(i,0),c-1),opposite_order_max_min=max(min(i,c-1),0)) for c in (0,1,13) for i in (-2147483648,-1,0,1,20)]
rect=[]
for name,c,coords in [('positive-grid-control',1,(0,0,0,0)),('empty-nonnegative',0,(0,0,0,0)),('empty-negative',0,(-1,-1,-1,-1)),('empty-mixed-skips',0,(-1,-1,0,0))]:
 x0,y0,x1,y1=[clamp(i,c) for i in coords];enter=y0<=y1 and x0<=x1;index=x0+y0*c if enter else None
 rect.append(dict(name=name,cols=c,rows=c,inputs=coords,clamped=[x0,y0,x1,y1],rectangle_loop_enters=enter,first_signed_cell_index=index,first_cell_read_relative_to_validity_base=index,limits='Conditional original source paths after memset returns, stable globals/readable state; no native execution, output OR/fault/actual occurrence claim'))
assert rect[1]['first_signed_cell_index']==-1 and rect[2]['first_signed_cell_index']==0 and not rect[3]['rectangle_loop_enters']
result=dict(method='A original292B CFG/operand proof, conditional calculations and actual Python checker read intervention; zero FF12/emulator/native/live executions',reference=dict(exe_sha256=BASE,reader_sha256=sha(rp.read_bytes()),body_sha256=sha(code),pe_function=[hex(x) for x in row],canonical_consumer_head=head),tools=dict(python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll_sha256=sha(Path(capstone._cs._name).read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii.values()],cases=cases,rectangles=rect,producer_controls=controls,source_mutation_rejected=rejected,result='Negative input always0: bypass-upper hypothesis confirmed, naive lower-then-upper refuted. Nonnegative input is signedmin(i,count-1); zero count gives-1. [0,count-1] guarantee requires positive dimensions. No dimension-zero exit before loops; empty all-nonnegative visits validitybase-1, all-negative visitsbase0 under stated conditional boundaries.',limits='No actual dimension-zero occurrence/original builder/allmalformed safety, native memset behavior/fault/normalcaller/inputconversion or lifetime guarantee. Full source firstbyte read is distinct from later validity-gated record OR/output. Exact toolDLL recorded at derivation, not native instrument qualification.',cleanup='Child read supplies restored; immutable reference unchanged, no peer/PC/game/process/save/config writes; existing published inputs preserved; independent review/consumer agreement pending')
assert sha(REF.read_bytes())==BASE
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('Piecewise clamp source settled: negative->0, nonnegativecount0->-1; empty ranges distinguish. Actual unchanged X3 stillPASS after bypass removal, source obligation rejects; no FF12 execution.',flush=True)
