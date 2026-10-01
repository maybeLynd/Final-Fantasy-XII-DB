import ast,hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
import capstone,unicorn
ROOT=Path.cwd();HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
path=ROOT/'Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py'
driver=path.read_bytes();old=subprocess.check_output(['git','show','0d068c953:Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py'])
same_newlines=driver.replace(b'\r\n',b'\n')==old.replace(b'\r\n',b'\n')
same_ast=ast.dump(ast.parse(driver))==ast.dump(ast.parse(old))
(HERE/'driver-qualification.json').write_text(json.dumps({'initial_probe':'STOPPED_BEFORE_IMPORT; byte guard noticed Git LF versus working-copy CRLF',
 'current_bytes':len(driver),'current_sha256':sha(driver),'accepted_git_bytes':len(old),'accepted_git_sha256':sha(old),
 'normalized_equal':same_newlines,'AST_equal':same_ast,'prior_new_native_results':0,
 'limits':'Only CRLF/LF equivalence allowed. Other source changes fail; peer source untouched.'},indent=2)+'\n')
assert same_newlines and same_ast,'producer source changed beyond newlines: requalify, never overwrite'
spec=importlib.util.spec_from_file_location('retained_exp140_license_clear_probe',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,secs=m.load_image();assert sha(raw)==m.SHA
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
code=[]
for a,n in [(m.BUILDER,287),(m.PREREQ,170)]:
 b=m.img_rd(raw,secs,a,n);ins=list(md.disasm(b,a));assert sum(i.size for i in ins)==n
 code.append({'entry':hex(a),'bytes':n,'hex':b.hex(),'sha256':sha(b),'instructions':[{'address':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
class Probe(m.World):
 def __init__(self,case,raw,secs):
  self.events=[];self.steps_seen=0;self.boundary_stop=False
  super().__init__(case,raw,secs)
 def on_code(self,uc,a,n,extra):
  self.steps_seen+=1
  if a in (m.BUILDER,0x2F8FE0,0x2F8FFC,0x2F8FFF,0x2F90A3,m.MSET):
   event={'pc':hex(a),'sequence':self.steps_seen,'rsp':hex(uc.reg_read(m.UC_X86_REG_RSP))}
   if a==m.MSET:
    event.update(dst=hex(uc.reg_read(m.UC_X86_REG_RCX)),value=uc.reg_read(m.UC_X86_REG_RDX)&255,byte_count=uc.reg_read(m.UC_X86_REG_R8))
    assert uc.reg_read(m.UC_X86_REG_RSP)&15==8,'invalid callback-entry ABI'
   self.events.append(event)
   if a==m.MSET and event['byte_count']>46:
    self.boundary_stop=True;uc.emu_stop();return
  super().on_code(uc,a,n,extra)
out=m.REC+0x300;results=[]
for count in (0,8,0xFFFFFFF9,0xFFFFFFF8):
 case={'nrows':count,'nrecs':[],'steps':[(m.BUILDER,1,0x10,out)],'watch':[(out-16,78)]}
 w=Probe(case,raw,secs)
 before=bytes([0xC3])*16+bytes([0xA5])*46+bytes([0x3C])*16;w.gm.w(out-16,before)
 # Correct Win64 function-entry alignment: return address already on stack.
 rsp=m.STACK+0x80008;assert rsp&15==8
 w.gm.w(rsp,m.qw(m.RETQ))
 for reg,val in [(m.UC_X86_REG_RSP,rsp),(m.UC_X86_REG_RCX,1),(m.UC_X86_REG_RDX,0x10),(m.UC_X86_REG_R8,out),(m.UC_X86_REG_R9,0)]:w.uc.reg_write(reg,val)
 error=None
 try:w.uc.emu_start(m.BUILDER,m.RETQ,timeout=2_000_000,count=6000)
 except m.UcError as e:error=str(e)
 after=w.gm.r(out-16,78);end=w.uc.reg_read(m.UC_X86_REG_RIP)
 record={'descriptor_count_u32':hex(count),'input_fixture':case,'initial_rsp':hex(rsp),'before_hex':before.hex(),'after_hex':after.hex(),
 'events':w.events,'instruction_callbacks':w.steps_seen,'end':hex(end),'rax':hex(w.uc.reg_read(m.UC_X86_REG_RAX)),
 'planned_boundary_stop':w.boundary_stop,'faults':w.faults,'error':error,'scripted_bridge_trace':w.trace}
 results.append(record)
 (HERE/'raw-results.json').write_text(json.dumps(results,indent=2)+'\n')
 assert error is None and not w.faults and w.steps_seen>0
 args=[e for e in w.events if e['pc']==hex(m.MSET)];assert len(args)==1
 assert args[0]['dst']==hex(out) and args[0]['value']==0 and args[0]['byte_count']==((count+7)&0xFFFFFFFF)>>3
 if count==0xFFFFFFF8:
  assert w.boundary_stop and end==m.MSET and after==before and not w.trace
 else:
  assert not w.boundary_stop and end==m.RETQ and w.uc.reg_read(m.UC_X86_REG_RAX)==0
  expected=bytearray(before)
  if count==8:expected[16]=0
  assert after==bytes(expected)
 print('ORIGINAL',hex(count),'clear_arg',args[0]['byte_count'],'BOUNDARY_STOP' if w.boundary_stop else 'RETURN','callbacks',w.steps_seen,flush=True)
sources={'method':'B original-code/controlled guest state, plus A code ordering; no live game',
 'exe_sha256':sha(raw),'driver_path':path.relative_to(ROOT).as_posix(),'driver_sha256':sha(driver),'driver_git_sha256':sha(old),'driver_commit':'0d068c953',
 'python_version':sys.version,'python_binary_sha256':sha(Path(sys.executable).read_bytes()),'unicorn_version':unicorn.__version__,'capstone_version':capstone.__version__,
 'scripted_boundary':'Original memset IAT thunk points at retained scripted bridge. Sizes<=46 only; oversized argument captured at entry and stopped before bridge.',
 'abi':'RCX=kind1, DX=requirement10; R8=supplied output; initialized mapped descriptor/node/stat/stack fixtures, RSP entry and callback mod16=8; no omitted real initialization claim.',
 'probe_budget':{'cases':4,'per_case_microseconds':2_000_000,'per_case_instructions':6000,'max_bridge_bytes':46},'code':code}
(HERE/'source.json').write_text(json.dumps(sources,indent=2)+'\n');(HERE/'retained-driver.txt').write_bytes(driver)
print('FOUR BOUNDARIES QUALIFIED; no large clear/native CRT/live result',flush=True)
