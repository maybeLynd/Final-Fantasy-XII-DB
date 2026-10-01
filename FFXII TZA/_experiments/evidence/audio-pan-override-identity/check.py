"""Method A: qualify bank/header identity for the known voice frpan override."""
import argparse,hashlib,json,struct,sys
from pathlib import Path
import capstone
E=Path(__file__).resolve().parent;R=E.parents[4]
sys.path.insert(0,str(R/'Database/Tools/analysis-kit/gfz-scripts'))
from disasm_fn import Image
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda b:hashlib.sha256(b).hexdigest()
def analyze():
 im=Image(R/'Database/Tools/work/exe/FFXII_TZA.exe');assert sha(im.d)==SHA and im.base==0x120000
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
 bodies=[];by={}
 for a,n in [(0x7B2470,121),(0x7BD8D0,28),(0x7E2A70,30),(0x7E2E80,33),(0x7CF540,18),(0x7CF580,11),(0x7E29C0,52),(0x7E2AD0,230),(0x7CFF90,20),(0x7D07A0,20),(0x7D09B0,37)]:
  raw=im.read(a,n);ins=list(md.disasm(raw,a));assert sum(i.size for i in ins)==n
  by.update({i.address:i for i in ins})
  bodies.append(dict(address=f'{a:08X}',size=n,sha256=sha(raw),raw=raw.hex(),instructions=[dict(address=f'{i.address:08X}',bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]))
 anchors={0x7BD8D4:('mov','rax, qword ptr [rcx + 0x20]'),0x7BD8E2:('call','0x7b2470'),
  0x7B247C:('cmp','r11b, 1'),0x7B24C9:('cmp','qword ptr [rax + 0x10], r11'),
  0x7E2A79:('mov','rdx, qword ptr [rcx + 0x50]'),0x7E2A80:('call','0x7cf540'),
  0x7E2E89:('mov','rdx, qword ptr [rcx + 0x88]'),0x7E2E93:('call','0x7cf540'),
  0x7CF547:('mov','qword ptr [rcx + 8], rdx'),0x7CF54E:('mov','rax, rcx'),
  0x7CF587:('mov','qword ptr [rcx], rax'),
  0x7E29D5:('mov','qword ptr [rbx + 0x50], 0'),0x7E29DD:('mov','qword ptr [rbx], rax'),
  0x7E2AF9:('cmp','r9d, 1'),0x7E2B03:('call','0x7cff90'),
  0x7E2B30:('cmp','r9d, 2'),0x7E2B3A:('call','0x7d07a0'),
  0x7E2B41:('mov','rax, qword ptr [rbx + 0x20]'),0x7E2B4B:('mov','qword ptr [rdi + 0x50], rax'),
  0x7D09B3:('mov','qword ptr [rcx + 0x10], rax'),0x7D09D1:('mov','dword ptr [rcx + 0x48], edx')}
 for a,want in anchors.items():assert (by[a].mnemonic,by[a].op_str)==want
 def rip(a):
  i=by[a];op=next(o for o in i.operands if o.type==capstone.x86.X86_OP_MEM and o.mem.base==capstone.x86.X86_REG_RIP)
  return i.address+i.size+op.mem.disp
 assert rip(0x7CF540)==0x1CB6E30 and rip(0x7CF580)==0x1CB6E30 and rip(0x7E29CE)==0x1CB83F8
 vtables=[]
 for vt,want,slot in [(0x1CB6E30,'.?AVAudioBinaryFile@Sd@SQEX@@',None),(0x1CB83F8,'.?AVOnMemoryBank@Driver@Sd@SQEX@@',0x7E2A70),(0x1CB84E8,'.?AVStreamingBank@Driver@Sd@SQEX@@',0x7E2E80)]:
  col=im.qword(vt-8);raw=im.read(col,24);sig,off,cd,td,ch,self_rva=struct.unpack('<6I',raw)
  assert sig==1 and off==0 and im.base+self_rva==col
  name=im.cstring(im.base+td+16,192);assert name==want
  if slot:assert im.qword(vt+0x38)==slot
  vtables.append(dict(address=f'{vt:08X}',locator=f'{col:08X}',locator_raw=raw.hex(),type_descriptor=f'{im.base+td:08X}',name=name,slot7=f'{slot:08X}' if slot else None,slot7_raw=im.read(vt+56,8).hex() if slot else None))
 constants=[]
 for a,value in [(0x7CFF9A,b'sabf'),(0x7D07AA,b'mabf')]:
  addr=rip(a);assert im.read(addr,4)==value;constants.append(dict(instruction=f'{a:08X}',address=f'{addr:08X}',raw=value.hex()))
 previous=E.parent/'audio-pan-caller-boundary/observation.json';caller=json.loads(previous.read_text())
 assert caller['executable_sha256']==SHA and im.read(0x7EDE90,1123).hex()==caller['body']['raw']
 return dict(method='A: exact original code/RTTI/file-magic identity; no isolated or live execution',executable_sha256=SHA,capstone=capstone.__version__,bodies=bodies,anchors_checked=len(anchors),vtables=vtables,magic_constants=constants,prior_caller_sha256=sha(previous.read_bytes()),limits=['OnMemoryBank initializer binds the magic-checked source file directly; actual live instance/handle/vtable remains unobserved.','StreamingBank getter payload pointer is qualified but its initializer/backing contents are not traced in this package.','Header +0A equals1 is one identified conditional consumer, not a universal interpretation of all350 authored values.','The wrapper destructor only resets a vtable pointer; no payload release is established.'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();r=analyze()
 if a.write:
  with (E/'observation.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
 else:assert r==json.loads((E/'observation.json').read_text())
 print('Verified bank vtable/RTTI identity, wrapper payload and OnMemoryBank source-file binding. The known frpan comparison can read file header +0A; live binding and broader meaning remain open.')
