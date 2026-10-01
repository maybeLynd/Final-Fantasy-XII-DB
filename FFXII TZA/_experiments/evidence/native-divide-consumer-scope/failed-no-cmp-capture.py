"""A exact immutable peer Z producer-fragment controls; never a full default/native run."""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,json,subprocess,types
from pathlib import Path
import capstone
from capstone.x86_const import X86_REG_XMM7,X86_REG_EBP,X86_REG_RBP
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
assert (W/'check.py').is_file();compile((W/'check.py').read_bytes(),str(W/'check.py'),'exec')
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NATIVE-DIVIDE-CONSUMER-SCOPE');assert t['agent']=='ASTRA' and t['status']=='ACTIVE';assert not R.exists();R.mkdir()
files=[];commit='141188dea'
for n in ['divide.py','README.md','divide.out']:
 p='Database/FFXII TZA/_index/candidates/script-divide-opus/'+n;b=subprocess.check_output(['git','show',commit+':'+p]);(R/n).write_bytes(b);files.append(dict(path=p,commit=commit,copy=n,sha256=sha(b)))
s=(R/'divide.py').read_text();assert s.count('# Z\n')==s.count('# M\n')==1;fragment=s[s.index('# Z\n'):s.index('# M\n')];(R/'exact-Z-fragment.py').write_text(fragment)
for n in ['shipping-reader.py','reg_tracking.py']:
 p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')/n;b=p.read_bytes();c='8db582868ae4a72bae3f9e76c1d709844e9d9d93';assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()]);(R/n).write_bytes(b);files.append(dict(path=p.as_posix(),commit=c,copy=n,sha256=sha(b)))
rd=types.ModuleType('reader');rd.__file__=str((R/'shipping-reader.py').resolve());exec(compile((R/'shipping-reader.py').read_bytes(),rd.__file__,'exec'),rd.__dict__);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'actual reviewed register policy','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ranges=[(0x25e4c0,0x25e550),(0x25e550,0x261ddb)];inputs=[];independent=[];chosen=None
for lo,hi in ranges:
 b=rd.img_rd(image,ss,lo,hi-lo);copy='claimed-scan-'+hex(lo)[2:]+'.bin';(R/copy).write_bytes(b);ii=list(cs.disasm(b,lo));assert sum(i.size for i in ii)==len(b)
 inputs.append(dict(lo=hex(lo),hi=hex(hi),bytes=len(b),copy=copy,sha256=sha(b)))
 for i in ii:
  wr=sorted(roles.written(i));independent.append(dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=wr))
  if chosen is None and i.address<0x25e550 and i.mnemonic=='cmp' and not any(r in wr for r in ['xmm7','rbp','ebp']):chosen=i.address
assert chosen is not None
restore=next(cs.disasm(rd.img_rd(image,ss,0x261dbc,15),0x261dbc));cutoff=restore.address+restore.size
class InputBytes:
 def __getitem__(self,sl):assert isinstance(sl,slice);return rd.img_rd(image,ss,sl.start,sl.stop-sl.start)
def run(mode):
 engine=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);logs=[];errors=[];checks=[]
 class Insn:
  def __init__(self,i):self.i=i
  def __getattr__(self,n):return getattr(self.i,n)
  def regs_access(self):
   if mode=='analysis-error' and self.i.address==chosen:
    errors.append(dict(pc=hex(chosen),kind='Private required register-analysis exception'));raise RuntimeError('Private required register-analysis failure')
   try:return self.i.regs_access()
   except Exception as e:errors.append(dict(pc=hex(self.i.address),kind=type(e).__name__,text=str(e)));raise
 class Decoder:
  @property
  def detail(self):return engine.detail
  @detail.setter
  def detail(self,v):engine.detail=v
  def disasm(self,b,pc):
   supplied=len(b);selected=b
   if mode=='decode-short' and pc==0x25e550 and len(b)>cutoff-pc:selected=b[:cutoff-pc]
   ii=list(engine.disasm(selected,pc));logs.append(dict(pc=hex(pc),supplied_bytes=supplied,decoded_bytes=sum(i.size for i in ii),input_sha256=sha(b),private_selected_bytes=len(selected)))
   return iter([Insn(i) for i in ii])
 proxy=Decoder()
 def dis(lo,hi):return [(i.address,i.mnemonic,i.op_str) for i in proxy.disasm(rd.img_rd(image,ss,lo,hi-lo),lo)]
 def check(tag,ok,text):checks.append(dict(tag=tag,ok=bool(ok),text=text))
 g=dict(cs=proxy,d=InputBytes(),off=lambda v:v,dis=dis,check=check,X86_REG_XMM7=X86_REG_XMM7,X86_REG_EBP=X86_REG_EBP,X86_REG_RBP=X86_REG_RBP)
 exec(compile(fragment,'exact immutable OPUS Z fragment','exec'),g)
 assert len(checks)==1 and checks[0]['tag']=='Z'
 return dict(mode=mode,source_check=checks[0],scan_calls=logs,required_analysis_errors=errors,wx=[hex(x) for x in g['wx']],we=[dict(pc=hex(pc),mnemonic=m) for pc,m in g['we']],limits='Python execution of exact Z fragment with input bridge/private decoder controls, not peer full default, not shipping instructions/native/game execution')
arms=[run(m) for m in ['baseline','analysis-error','decode-short']];assert all(a['source_check']['ok'] for a in arms)
assert not arms[0]['required_analysis_errors'] and all(x['supplied_bytes']==x['decoded_bytes'] for x in arms[0]['scan_calls'])
assert len(arms[1]['required_analysis_errors'])==1 and arms[2]['scan_calls'][1]['decoded_bytes']<arms[2]['scan_calls'][1]['supplied_bytes']
providers=[dict(path=str(Path(capstone.__file__).resolve()),sha256=sha(Path(capstone.__file__).read_bytes()))]+[dict(path=str(p),sha256=sha(p.read_bytes())) for p in sorted(Path(capstone.__file__).resolve().parent.rglob('*.dll'))]
preflight=dict(pefile_available=importlib.util.find_spec('pefile') is not None,full_peer_default_run=False,reason='Exact Z fragment only; full default requires upstream PE loader/U and must not be represented as passed')
raw=dict(method='A exact source producer-fragment prerequisite controls plus original shipping-byte independent shared-adapter scan; no shipping-code execution',reference=dict(exe_sha256=sha(image),files=files,fragment_sha256=sha((R/'exact-Z-fragment.py').read_bytes()),ranges=inputs,range_scope='Literal declared producer inputs, NOT function ownership/reachability proof',private_error_pc=hex(chosen),private_cutoff=hex(cutoff)),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,provider_files=providers),preflight=preflight,independent_shared_adapter=independent,arms=arms,driver_sha256=sha(Path(__file__).read_bytes()),limits='Exact immutable Z fragment accepts injected required-analysis failure and shortened decode while downstream Z stays true. Baseline independent scan covers given ranges with no error; do not retract valid source arithmetic or current baseline writer observations. Not full peer default/actual decoder failure/whole function semantics/native initialization/callback preservation/exception delivery/no-catch/lifetime/OS outcome. Metadata handler catalogue distinct from semantic routing. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE84 concrete exact Z-fragment prerequisite controls',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
