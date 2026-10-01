"""Method A only: original voice caller boundaries, not executed voice effects."""
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
 raw=im.read(0x7EDE90,1123);md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
 ins=list(md.disasm(raw,0x7EDE90));assert ins[0].address==0x7EDE90 and ins[-1].mnemonic=='ret' and sum(i.size for i in ins)==1123
 by={i.address:(i.mnemonic,i.op_str) for i in ins}
 checks={
  0x7EDED7:('movaps','xmm9, xmm2'),0x7EDF45:('xorps','xmm8, xmm8'),
  0x7EDF13:('cmp','byte ptr [rcx + 0x50], 4'),0x7EDF4E:('jne','0x7ee11a'),
  0x7EDF8D:('movzx','edi, byte ptr [rcx + 0x50]'),0x7EDF93:('xor','dil, dil'),
  0x7EDF96:('cmp','byte ptr [rcx], 0xf'),0x7EDFA3:('movss','xmm7, dword ptr [rcx + 0x54]'),
  0x7EE015:('call','qword ptr [r8 + 0x38]'),0x7EE019:('mov','rcx, qword ptr [rax + 8]'),
  0x7EE01D:('movzx','ebx, word ptr [rcx + 0xa]'),0x7EE02B:('cmp','bx, 1'),
  0x7EE02F:('jne','0x7ee035'),0x7EE031:('movaps','xmm9, xmm8'),
  0x7EE035:('test','dil, dil'),0x7EE038:('je','0x7ee11a'),
  0x7EE03E:('cmp','dil, 1'),0x7EE042:('jne','0x7ee1d9'),
  0x7EE04E:('call','qword ptr [rax + 0x108]'),0x7EE05F:('movaps','xmm8, xmm0'),
  0x7EE063:('mulss','xmm8, xmm7'),0x7EE07E:('minss','xmm8, xmm6'),
  0x7EE0A5:('movss','dword ptr [rsp + 0x48], xmm8'),0x7EE159:('movss','dword ptr [rsp + 0x48], xmm8'),
  0x7EE0C6:('movaps','xmm1, xmm9'),0x7EE17A:('movaps','xmm1, xmm9'),
  0x7EE0D9:('call','0x7b8430'),0x7EE18D:('call','0x7b8430'),
  0x7EE0EA:('mov','ebx, r14d'),0x7EE0FD:('add','ebx, r15d'),
  0x7EE100:('mov','dword ptr [rbp + rcx*4 - 0x80], eax'),
  0x7EE1FB:('mov','rax, qword ptr [rcx]'),0x7EE1FE:('lea','rdx, [rbp - 0x80]'),
  0x7EE202:('call','qword ptr [rax + 0x40]'),
  0x7EE266:('mov','edx, esi'),0x7EE263:('mov','r8d, ebx'),0x7EE271:('call','0x121880'),
 }
 for address,want in checks.items():assert by[address]==want,(hex(address),by[address],want)
 # Tool-resolve the min bound; do not infer a float from an address or label.
 md.detail=True;i=next(i for i in md.disasm(raw,0x7EDE90) if i.address==0x7EDF99)
 target=i.address+i.size+i.operands[1].mem.disp
 assert target==0x1CEBBA8 and im.read(target,4)==struct.pack('<f',1.0)
 return dict(method='A: original caller code and existing callee ABI; no execution',executable_sha256=SHA,capstone=capstone.__version__,body=dict(address='007EDE90',size=len(raw),sha256=sha(raw),raw=raw.hex(),instructions=[dict(address=f'{i.address:08X}',bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]),anchors_checked=len(checks),min_bound=dict(address=f'{target:08X}',raw=im.read(target,4).hex(),value=1.0),limits=['No actual object instance, virtual implementation, caller execution or sound output observed.','Unnamed metadata word is identified by access path, not assigned a guessed semantic type.','Normal ABI preservation of XMM6-XMM15 is required across intervening native calls.','Matrix construction, dispatch attempt and device playback are different boundaries.'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();r=analyze()
 if a.write:
  with (E/'observation.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
 else:assert r==json.loads((E/'observation.json').read_text())
 print('Verified complete original voice caller, scalar overrides, mixer arguments and output-major matrix placement. No execution or live cue claim.')
